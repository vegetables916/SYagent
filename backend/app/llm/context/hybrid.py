"""混合上下文管理器 - 滑动窗口 + 向量检索"""

import numpy as np
from typing import List
from app.llm.context.base import BaseContextManager, MessageRole
from app.llm.context.vector_store import VectorStore, MessageWithVector
from app.llm.embeddings import get_embedding_service


class HybridContextManager(BaseContextManager):
    """混合上下文管理器

    组合两种策略：
    1. 滑动窗口：保留最近 N 条消息（保证连贯性）
    2. 向量检索：根据当前查询检索语义相关的历史消息（保证相关性）

    获取消息时合并两者结果，去重后返回。

    注意：此类必须使用异步方法，同步方法会抛出异常
    """

    def __init__(
        self,
        recent_count: int = 10,
        relevant_count: int = 5,
        embedding_provider: str = "openai",
    ):
        """初始化

        Args:
            recent_count: 滑动窗口保留的最近消息数量
            relevant_count: 向量检索返回的相关消息数量
            embedding_provider: Embedding 服务提供商
        """
        self._recent_count = recent_count
        self._relevant_count = relevant_count
        self._vector_store = VectorStore()
        self._embedding_service = get_embedding_service(embedding_provider)

    def add_message(self, role: MessageRole, content: str) -> None:
        """同步添加消息 - 不支持，请使用 add_message_async"""
        raise NotImplementedError(
            "HybridContextManager 必须使用异步方法。"
            "请使用: await context.add_message_async(role, content)"
        )

    async def add_message_async(self, role: MessageRole, content: str) -> None:
        """异步添加消息并计算向量

        Args:
            role: 消息角色 (user/assistant/system)
            content: 消息内容
        """
        vector = np.array(await self._embedding_service.embed_text(content))
        self._vector_store.add(role, content, vector)

    def get_messages(self) -> list[dict[str, str]]:
        """同步获取消息 - 不支持，请使用 get_messages_async"""
        raise NotImplementedError(
            "HybridContextManager 必须使用异步方法。"
            "请使用: await context.get_messages_async(query)"
        )

    async def get_messages_async(self, query: str | None = None) -> list[dict[str, str]]:
        """异步获取消息列表（滑动窗口 + 向量检索）

        策略：
        1. 获取最近 N 条消息（保证连贯性）
        2. 如果有 query，检索语义相关的历史消息（保证相关性）
        3. 合并去重后按时间顺序返回

        Args:
            query: 当前查询，用于检索相关历史

        Returns:
            合并后的消息列表
        """
        # 1. 滑动窗口：获取最近的消息
        recent = self._vector_store.get_recent(self._recent_count)

        # 2. 向量检索：如果有 query，检索语义相关的消息
        relevant: List[MessageWithVector] = []
        if query:
            query_vector = np.array(await self._embedding_service.embed_text(query))
            relevant = self._vector_store.search(query_vector, self._relevant_count)

        # 3. 合并去重
        selected = {msg.index: msg for msg in recent}
        for msg in relevant:
            if msg.index not in selected:
                selected[msg.index] = msg

        # 4. 按时间顺序排序
        sorted_messages = sorted(selected.values(), key=lambda m: m.index)

        return [{"role": msg.role, "content": msg.content} for msg in sorted_messages]

    def clear(self) -> None:
        """清空存储"""
        self._vector_store.clear()

    @property
    def message_count(self) -> int:
        """当前消息数量"""
        return self._vector_store.size
