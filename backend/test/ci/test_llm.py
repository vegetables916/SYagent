"""LLM 模块测试"""
import pytest
from unittest.mock import AsyncMock, patch
from app.llm import get_llm_client, register_provider
from app.llm.base import BaseLLMClient


class TestLLMFactory:
    """测试工厂模式"""
    
    def test_get_default_client(self):
        """测试获取默认客户端"""
        client = get_llm_client()
        assert client is not None
        assert isinstance(client, BaseLLMClient)
    
    def test_get_openai_client(self):
        """测试获取 OpenAI 客户端"""
        client = get_llm_client("openai")
        assert client.provider == "openai"
    
    def test_get_deepseek_client(self):
        """测试获取 DeepSeek 客户端"""
        client = get_llm_client("deepseek")
        assert client.provider == "deepseek"
    
    def test_unknown_provider_raises_error(self):
        """测试未知提供商抛出异常"""
        with pytest.raises(ValueError, match="未知的模型提供商"):
            get_llm_client("unknown_provider")
    
    def test_register_custom_provider(self):
        """测试动态注册自定义提供商"""
        class CustomClient(BaseLLMClient):
            @property
            def provider(self) -> str:
                return "custom"
            
            def _create_client(self):
                return None
        
        register_provider("custom", CustomClient)
        client = get_llm_client("custom")
        assert client.provider == "custom"


class TestLLMChat:
    """测试聊天功能"""
    
    @pytest.mark.asyncio
    async def test_chat_without_system_prompt(self):
        """测试不带系统提示词的聊天"""
        client = get_llm_client("openai")
        
        # Mock 实际的 API 调用 - 直接设置 _client 属性
        mock_client = AsyncMock()
        mock_response = AsyncMock()
        mock_response.content = "测试回复"
        mock_client.ainvoke = AsyncMock(return_value=mock_response)
        client._client = mock_client
        
        result = await client.chat("你好")
        
        assert result == "测试回复"
        mock_client.ainvoke.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_chat_with_system_prompt(self):
        """测试带系统提示词的聊天"""
        client = get_llm_client("openai")
        
        # Mock 实际的 API 调用 - 直接设置 _client 属性
        mock_client = AsyncMock()
        mock_response = AsyncMock()
        mock_response.content = "我是助手"
        mock_client.ainvoke = AsyncMock(return_value=mock_response)
        client._client = mock_client
        
        result = await client.chat("你是谁", system_prompt="你是一个助手")
        
        assert result == "我是助手"
        # 验证调用时传入了系统提示词
        call_args = mock_client.ainvoke.call_args[0][0]
        assert len(call_args) == 2  # SystemMessage + HumanMessage
