"""简单上下文管理器 - 滑动窗口策略"""

from app.llm.context.base import BaseContextManager, MessageRole


class SimpleContextManager(BaseContextManager):
    """简单上下文管理器
    
    使用滑动窗口策略，只保留最近 N 轮对话
    """
    
    def __init__(self, max_messages: int = 20):
        """初始化
        
        Args:
            max_messages: 最大消息数量（默认 20 条，即 10 轮对话）
        """
        self._messages: list[dict[str, str]] = []
        self._max_messages = max_messages
    
    def add_message(self, role: MessageRole, content: str) -> None:
        """添加消息，超出限制时移除最早的消息"""
        self._messages.append({"role": role, "content": content})
        
        # 滑动窗口：超出时移除最早的消息
        if len(self._messages) > self._max_messages:
            self._messages.pop(0)
    
    def get_messages(self) -> list[dict[str, str]]:
        """获取当前所有消息"""
        return self._messages.copy()
    
    def clear(self) -> None:
        """清空所有消息"""
        self._messages.clear()
    
    @property
    def message_count(self) -> int:
        """当前消息数量"""
        return len(self._messages)
