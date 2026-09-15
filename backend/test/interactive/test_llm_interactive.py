"""
LLM 交互式测试

用法: python -m test.interactive.test_llm_interactive [--provider deepseek] [--context simple] [--max-messages 20]
"""
import asyncio
import argparse
from app.llm import get_llm_client, get_context_manager


async def chat_loop(provider: str, context_strategy: str | None, max_messages: int):
    """交互式聊天循环"""
    client = get_llm_client(provider)
    
    # 创建上下文管理器（如果指定了策略）
    context = None
    if context_strategy:
        context = get_context_manager(context_strategy, max_messages=max_messages)
        print(f"=== LLM 交互式测试 (provider: {provider}, context: {context_strategy}, max_messages: {max_messages}) ===")
    else:
        print(f"=== LLM 交互式测试 (provider: {provider}, 无上下文) ===")
    
    print("输入消息开始对话，输入 q 退出，输入 clear 清空上下文\n")

    while True:
        user_input = input("你: ").strip()

        if not user_input:
            continue

        if user_input.lower() == "q":
            print("再见！")
            break
        
        if user_input.lower() == "clear":
            if context:
                context.clear()
                print("[上下文已清空]\n")
            else:
                print("[无上下文管理器]\n")
            continue

        try:
            if context:
                # 使用上下文的多轮对话
                response = await client.chat(user_input, context=context)
                print(f"AI: {response}\n")
                print(f"[上下文消息数: {context.message_count}]\n")
            else:
                # 单轮对话（流式）
                print("AI: ", end="", flush=True)
                async for token in client.chat_stream(user_input):
                    print(token, end="", flush=True)
                print("\n")
        except Exception as e:
            print(f"错误: {e}\n")


def main():
    parser = argparse.ArgumentParser(description="LLM 交互式测试")
    parser.add_argument(
        "--provider",
        type=str,
        default="deepseek",
        help="模型提供商 (默认: deepseek)",
    )
    parser.add_argument(
        "--context",
        type=str,
        default=None,
        choices=["simple", "summary"],
        help="上下文策略 (simple: 滑动窗口, summary: 摘要压缩)",
    )
    parser.add_argument(
        "--max-messages",
        type=int,
        default=20,
        help="最大消息数量 (默认: 20)",
    )
    args = parser.parse_args()
    asyncio.run(chat_loop(args.provider, args.context, args.max_messages))


if __name__ == "__main__":
    main()
