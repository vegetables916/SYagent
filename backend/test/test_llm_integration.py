"""LLM 集成测试（需要真实 API Key）"""
import pytest
from app.llm import get_llm_client


class TestLLMIntegration:
    """集成测试 - 真实调用 API"""
    
    @pytest.mark.asyncio
    @pytest.mark.skip(reason="需要真实的 API Key，手动运行")
    async def test_openai_real_chat(self):
        """测试 OpenAI 真实对话"""
        client = get_llm_client("openai")
        result = await client.chat("你好，请用一句话介绍自己")
        print(f"OpenAI 回复: {result}")
        assert len(result) > 0
    
    @pytest.mark.asyncio
    @pytest.mark.skip(reason="需要真实的 API Key，手动运行")
    async def test_deepseek_real_chat(self):
        """测试 DeepSeek 真实对话"""
        client = get_llm_client("deepseek")
        result = await client.chat("你好，请用一句话介绍自己")
        print(f"DeepSeek 回复: {result}")
        assert len(result) > 0
    
    @pytest.mark.asyncio
    @pytest.mark.skip(reason="需要真实的 API Key，手动运行")
    async def test_chat_with_system_prompt(self):
        """测试带系统提示词的对话"""
        client = get_llm_client("openai")
        result = await client.chat(
            "我叫小明",
            system_prompt="你是一个友好的助手，记住用户的名字"
        )
        print(f"回复: {result}")
        assert len(result) > 0
