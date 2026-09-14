"""摘要压缩上下文管理器"""

from app.llm.context.base import BaseContextManager, MessageRole


class SummaryContextManager(BaseContextManager):
    """摘要压缩上下文管理器
    
    当消息数量超过阈值时，使用 LLM 将历史消息压缩为摘要
    """
    
    def __init__(self, max_messages: int = 20, summary_threshold: int = 15):
        """初始化
        
        Args:
            max_messages: 最大消息数量
            summary_threshold: 触发摘要压缩的阈值
        """
        self._messages: list[dict[str, str]] = []
        self._summary: str = ""
        self._max_messages = max_messages
        self._summary_threshold = summary_threshold
    
    def add_message(self, role: MessageRole, content: str) -> None:
        """添加消息，超过阈值时触发压缩"""
        self._messages.append({"role": role, "content": content})
        
        # 检查是否需要压缩
        if len(self._messages) >= self._summary_threshold:
            self._compress()
    
    def _compress(self) -> None:
        """压缩历史消息为摘要（待实现）"""
        # TODO: 使用 LLM 生成摘要
        # 这里先简单截断，保留最近的消息
        if len(self._messages) > self._max_messages:
            # 保留最近一半的消息
            keep_count = self._max_messages // 2
            self._messages = self._messages[-keep_count:]
    
    def get_messages(self) -> list[dict[str, str]]:
        """获取消息列表（包含摘要）"""
        result = []
        
        # 如果有摘要，先添加
        if self._summary:
            result.append({
                "role": "system",
                "content": f"之前的对话摘要：{self._summary}"
            })
        
        result.extend(self._messages)
        return result
    
    def clear(self) -> None:
        """清空所有消息和摘要"""
        self._messages.clear()
        self._summary = ""
    
    @property
    def message_count(self) -> int:
        """当前消息数量"""
        return len(self._messages)
