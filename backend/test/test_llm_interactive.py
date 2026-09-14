"""
LLM 交互式测试

用法: python test/test_llm_interactive.py [--provider deepseek]
"""
import asyncio
import argparse
from app.llm import get_llm_client


async def chat_loop(provider: str):
    """交互式聊天循环"""
    client = get_llm_client(provider)
    print(f"=== LLM 交互式测试 (provider: {provider}) ===")
    print("输入消息开始对话，输入 q 退出\n")

    while True:
        user_input = input("你: ").strip()

        if not user_input:
            continue

        if user_input.lower() == "q":
            print("再见！")
            break

        try:
            response = await client.chat(user_input)
            print(f"AI: {response}\n")
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
    args = parser.parse_args()
    asyncio.run(chat_loop(args.provider))


if __name__ == "__main__":
    main()
