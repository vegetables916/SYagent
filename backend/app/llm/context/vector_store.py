"""向量存储 - 用于存储和检索对话历史"""

import numpy as np
from typing import List, Tuple
from dataclasses import dataclass, field


@dataclass
class MessageWithVector:
    """带向量的消息"""
    role: str
    content: str
    vector: np.ndarray = field(repr=False)
    index: int = 0  # 消息序号，用于保持顺序


class VectorStore:
    """简单的向量存储，基于 NumPy 实现"""
    
    def __init__(self):
        self._messages: List[MessageWithVector] = []
        self._index_counter = 0
    
    def add(self, role: str, content: str, vector: np.ndarray) -> None:
        """添加消息到存储"""
        msg = MessageWithVector(
            role=role,
            content=content,
            vector=vector,
            index=self._index_counter
        )
        self._messages.append(msg)
        self._index_counter += 1
    
    def search(self, query_vector: np.ndarray, top_k: int = 5) -> List[MessageWithVector]:
        """
        搜索最相似的消息
        
        Args:
            query_vector: 查询向量
            top_k: 返回最相似的 K 条消息
        
        Returns:
            按相似度排序的消息列表
        """
        if not self._messages:
            return []
        
        # 计算余弦相似度
        similarities = []
        for msg in self._messages:
            similarity = self._cosine_similarity(query_vector, msg.vector)
            similarities.append((similarity, msg))
        
        # 按相似度降序排序
        similarities.sort(key=lambda x: x[0], reverse=True)
        
        # 返回 top_k
        return [msg for _, msg in similarities[:top_k]]
    
    def get_recent(self, k: int) -> List[MessageWithVector]:
        """获取最近的 K 条消息（按时间顺序）"""
        # 按 index 排序，取最后 K 条
        sorted_msgs = sorted(self._messages, key=lambda m: m.index)
        return sorted_msgs[-k:] if k < len(sorted_msgs) else sorted_msgs
    
    def get_all(self) -> List[MessageWithVector]:
        """获取所有消息"""
        return self._messages.copy()
    
    def clear(self) -> None:
        """清空存储"""
        self._messages.clear()
        self._index_counter = 0
    
    @property
    def size(self) -> int:
        """存储的消息数量"""
        return len(self._messages)
    
    @staticmethod
    def _cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
        """计算余弦相似度"""
        dot_product = np.dot(a, b)
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        
        if norm_a == 0 or norm_b == 0:
            return 0.0
        
        return float(dot_product / (norm_a * norm_b))
