"""上下文管理器抽象基类"""

from abc import ABC, abstractmethod
from typing import Literal

MessageRole = Literal["user", "assistant", "system"]


class BaseContextManager(ABC):
    """上下文管理器抽象基类
    
    负责管理对话历史，支持不同的压缩策略
    """
    
    @abstractmethod
    def add_message(self, role: MessageRole, content: str) -> None:
        """添加消息到上下文
        
        Args:
            role: 消息角色 (user/assistant/system)
            content: 消息内容
        """
        ...
    
    @abstractmethod
    def get_messages(self) -> list[dict[str, str]]:
        """获取消息列表（可能经过压缩）
        
        Returns:
            消息列表，格式: [{"role": "user", "content": "..."}, ...]
        """
        ...
    
    @abstractmethod
    def clear(self) -> None:
        """清空上下文"""
        ...
    
    @property
    @abstractmethod
    def message_count(self) -> int:
        """当前消息数量"""
        ...
