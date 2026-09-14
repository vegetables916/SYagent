"""
LLM 基础客户端 - 抽象基类

定义统一的 LLM 接口，所有模型提供商必须实现该接口
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

if TYPE_CHECKING:
    from app.llm.context.base import BaseContextManager


class BaseLLMClient(ABC):
    """LLM 客户端抽象基类"""

    @property
    @abstractmethod
    def provider(self) -> str:
        """模型提供商名称"""
        ...

    @abstractmethod
    def _create_client(self) -> BaseChatModel:
        """
        创建具体的 LangChain 模型客户端（内部使用）
        
        警告：此方法不应被直接调用，请使用 `client` 属性获取单例客户端。
        直接调用此方法会破坏单例模式。
        """
        ...

    @property
    def client(self) -> BaseChatModel:
        """获取模型客户端（懒加载单例）"""
        if not hasattr(self, "_client") or self._client is None:
            self._client = self._create_client()
        return self._client

    async def chat(
        self,
        message: str,
        system_prompt: str | None = None,
        context: "BaseContextManager | None" = None,
    ) -> str:
        """
        发送聊天消息

        Args:
            message: 用户消息
            system_prompt: 系统提示词（可选）
            context: 上下文管理器（可选，用于多轮对话）

        Returns:
            模型回复内容
        """
        # 如果有上下文，添加到 context
        if context:
            context.add_message("user", message)
            messages = []
            if system_prompt:
                messages.append(SystemMessage(content=system_prompt))
            # 从 context 获取历史消息
            for msg in context.get_messages():
                if msg["role"] == "user":
                    messages.append(HumanMessage(content=msg["content"]))
                elif msg["role"] == "assistant":
                    messages.append(AIMessage(content=msg["content"]))
        else:
            messages = []
            if system_prompt:
                messages.append(SystemMessage(content=system_prompt))
            messages.append(HumanMessage(content=message))

        response = await self.client.ainvoke(messages)
        
        # 如果有上下文，保存 AI 回复
        if context:
            context.add_message("assistant", response.content)
        
        return response.content

    async def chat_stream(self, message: str, system_prompt: str | None = None):
        """
        流式发送聊天消息

        Args:
            message: 用户消息
            system_prompt: 系统提示词（可选）

        Yields:
            模型回复的每个 token
        """
        messages = []
        if system_prompt:
            messages.append(SystemMessage(content=system_prompt))
        messages.append(HumanMessage(content=message))

        async for chunk in self.client.astream(messages):
            if chunk.content:
                yield chunk.content

    async def chat_batch(self, messages_list: list[str], system_prompt: str | None = None) -> list[str]:
        """
        批量发送聊天消息

        Args:
            messages_list: 用户消息列表
            system_prompt: 系统提示词（可选）

        Returns:
            模型回复内容列表

        Raises:
            NotImplementedError: 待实现
        """
        raise NotImplementedError("批量处理功能待实现")
