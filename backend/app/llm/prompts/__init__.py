"""Prompt 模板管理"""

from app.llm.prompts.chat import CHAT_SYSTEM_PROMPT
from app.llm.prompts.assistant import ASSISTANT_SYSTEM_PROMPT, get_assistant_prompt

__all__ = ["CHAT_SYSTEM_PROMPT", "ASSISTANT_SYSTEM_PROMPT", "get_assistant_prompt"]
