"""
LLM 模块配置

独立的配置管理，只关注大模型相关设置
"""

from pydantic_settings import BaseSettings


class LLMSettings(BaseSettings):
    """LLM 配置"""

    # OpenAI
    OPENAI_API_KEY: str = ""
    OPENAI_BASE_URL: str = "https://api.openai.com/v1"
    OPENAI_MODEL: str = "gpt-4o"

    # DeepSeek
    DEEPSEEK_API_KEY: str = ""
    DEEPSEEK_BASE_URL: str = "https://api.deepseek.com/v1"
    DEEPSEEK_MODEL: str = "deepseek-chat"

    # 默认提供商
    DEFAULT_LLM_PROVIDER: str = "openai"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# 全局单例
llm_settings = LLMSettings()
