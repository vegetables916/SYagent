"""上下文管理器测试"""

import pytest
from app.llm.context import (
    SimpleContextManager,
    get_context_manager,
    register_context_strategy,
)


class TestSimpleContextManager:
    """简单上下文管理器测试"""
    
    def test_add_message(self):
        """测试添加消息"""
        ctx = SimpleContextManager(max_messages=10)
        ctx.add_message("user", "你好")
        ctx.add_message("assistant", "你好！有什么可以帮助你的？")
        
        assert ctx.message_count == 2
        messages = ctx.get_messages()
        assert messages[0]["role"] == "user"
        assert messages[0]["content"] == "你好"
        assert messages[1]["role"] == "assistant"
    
    def test_sliding_window(self):
        """测试滑动窗口机制"""
        ctx = SimpleContextManager(max_messages=4)
        
        # 添加 6 条消息
        for i in range(6):
            ctx.add_message("user", f"消息 {i}")
        
        # 应该只保留最后 4 条
        assert ctx.message_count == 4
        messages = ctx.get_messages()
        assert messages[0]["content"] == "消息 2"
        assert messages[3]["content"] == "消息 5"
    
    def test_clear(self):
        """测试清空上下文"""
        ctx = SimpleContextManager()
        ctx.add_message("user", "测试")
        assert ctx.message_count == 1
        
        ctx.clear()
        assert ctx.message_count == 0
        assert len(ctx.get_messages()) == 0


class TestContextFactory:
    """上下文管理器工厂测试"""
    
    def test_get_simple_context(self):
        """测试获取简单上下文管理器"""
        ctx = get_context_manager("simple", max_messages=5)
        assert isinstance(ctx, SimpleContextManager)
        assert ctx._max_messages == 5
    
    def test_unknown_strategy_raises_error(self):
        """测试未知策略抛出异常"""
        with pytest.raises(ValueError, match="未知的上下文策略"):
            get_context_manager("unknown_strategy")
    
    def test_register_custom_strategy(self):
        """测试注册自定义策略"""
        class CustomContext(SimpleContextManager):
            pass
        
        register_context_strategy("custom", CustomContext)
        ctx = get_context_manager("custom")
        assert isinstance(ctx, CustomContext)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
