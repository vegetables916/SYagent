"""Qdrant 向量存储 - 基于 Qdrant 向量数据库实现"""

import uuid
import numpy as np
from typing import List, Optional
from dataclasses import dataclass, field
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue,
    Range,
)

from app.llm.context.vector_store import MessageWithVector


class QdrantVectorStore:
    """基于 Qdrant 的向量存储
    
    使用 Qdrant 向量数据库替代内存存储，支持：
    - 持久化存储
    - 高效向量检索
    - 元数据过滤
    """
    
    def __init__(
        self,
        host: str = "localhost",
        port: int = 6333,
        collection_name: str = "conversation_messages",
        vector_size: int = 1536,  # OpenAI text-embedding-3-small 维度
    ):
        """初始化 Qdrant 向量存储
        
        Args:
            host: Qdrant 服务地址
            port: Qdrant HTTP 端口
            collection_name: 集合名称
            vector_size: 向量维度
        """
        self._client = QdrantClient(host=host, port=port)
        self._collection_name = collection_name
        self._vector_size = vector_size
        self._index_counter = 0
        
        # 确保 collection 存在
        self._ensure_collection()
    
    def _ensure_collection(self) -> None:
        """确保 collection 存在，不存在则创建"""
        collections = self._client.get_collections().collections
        collection_names = [c.name for c in collections]
        
        if self._collection_name not in collection_names:
            self._client.create_collection(
                collection_name=self._collection_name,
                vectors_config=VectorParams(
                    size=self._vector_size,
                    distance=Distance.COSINE,
                ),
            )
    
    def add(self, role: str, content: str, vector: np.ndarray) -> None:
        """添加消息到 Qdrant
        
        Args:
            role: 消息角色
            content: 消息内容
            vector: 消息向量
        """
        # 生成唯一 ID
        point_id = str(uuid.uuid4())
        
        # 构建 payload（元数据）
        payload = {
            "role": role,
            "content": content,
            "index": self._index_counter,
        }
        
        # 插入点
        self._client.upsert(
            collection_name=self._collection_name,
            points=[
                PointStruct(
                    id=point_id,
                    vector=vector.tolist(),
                    payload=payload,
                )
            ],
        )
        
        self._index_counter += 1
    
    def search(
        self,
        query_vector: np.ndarray,
        top_k: int = 5,
    ) -> List[MessageWithVector]:
        """搜索最相似的消息
        
        Args:
            query_vector: 查询向量
            top_k: 返回最相似的 K 条消息
        
        Returns:
            按相似度排序的消息列表
        """
        # 检查是否有数据
        if self.size == 0:
            return []
        
        # 执行搜索
        results = self._client.search(
            collection_name=self._collection_name,
            query_vector=query_vector.tolist(),
            limit=top_k,
        )
        
        # 转换为 MessageWithVector
        messages = []
        for hit in results:
            payload = hit.payload
            messages.append(
                MessageWithVector(
                    role=payload["role"],
                    content=payload["content"],
                    vector=np.array(hit.vector),
                    index=payload["index"],
                )
            )
        
        return messages
    
    def get_recent(self, k: int) -> List[MessageWithVector]:
        """获取最近的 K 条消息（按 index 降序）
        
        Args:
            k: 获取的消息数量
        
        Returns:
            按 index 降序排列的消息列表
        """
        # 滚动查询所有点
        all_points = []
        offset = None
        
        while True:
            result = self._client.scroll(
                collection_name=self._collection_name,
                limit=100,
                offset=offset,
                with_vectors=False,
            )
            
            points, next_offset = result
            all_points.extend(points)
            
            if next_offset is None:
                break
            offset = next_offset
        
        # 按 index 排序
        sorted_points = sorted(
            all_points,
            key=lambda p: p.payload["index"],
        )
        
        # 取最后 K 条
        recent_points = sorted_points[-k:] if k < len(sorted_points) else sorted_points
        
        # 转换为 MessageWithVector
        messages = []
        for point in recent_points:
            payload = point.payload
            messages.append(
                MessageWithVector(
                    role=payload["role"],
                    content=payload["content"],
                    vector=np.array(point.vector) if point.vector else np.array([]),
                    index=payload["index"],
                )
            )
        
        return messages
    
    def get_all(self) -> List[MessageWithVector]:
        """获取所有消息"""
        return self.get_recent(k=999999)
    
    def clear(self) -> None:
        """清空存储（删除 collection 并重建）"""
        try:
            self._client.delete_collection(self._collection_name)
        except Exception:
            pass
        self._ensure_collection()
        self._index_counter = 0
    
    @property
    def size(self) -> int:
        """存储的消息数量"""
        try:
            info = self._client.get_collection(self._collection_name)
            return info.points_count
        except Exception:
            return 0
