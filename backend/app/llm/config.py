"""
LLM 模块配置

独立的配置管理，只关注大模型相关设置
读取本目录下的 .env 文件，与主项目配置完全隔离
"""

from pathlib import Path
from pydantic_settings import BaseSettings

# LLM 模块根目录
_LLM_DIR = Path(__file__).resolve().parent


class LLMSettings(BaseSettings):
    """LLM 配置"""

    # OpenAI
    OPENAI_API_KEY: str = ""
    OPENAI_BASE_URL: str = "https://api.openai.com/v1"
    OPENAI_MODEL: str = "gpt-4o"

    # DeepSeek
    DEEPSEEK_API_KEY: str = ""
    DEEPSEEK_BASE_URL: str = "https://api.deepseek.com/v1"
    DEEPSEEK_MODEL: str = "deepseek-flash"

    # 默认提供商
    DEFAULT_LLM_PROVIDER: str = "openai"

    # 上下文管理配置
    CONTEXT_STRATEGY: str = "hybrid"  # simple / summary / hybrid
    CONTEXT_RECENT_COUNT: int = 10  # 滑动窗口保留的最近消息数量
    CONTEXT_RELEVANT_COUNT: int = 5  # 向量检索返回的相关消息数量
    CONTEXT_EMBEDDING_PROVIDER: str = "local"  # openai / local
    CONTEXT_VECTOR_STORE_BACKEND: str = "qdrant"  # memory / qdrant
    LOCAL_EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"  # 本地 embedding 模型

    # Qdrant 配置
    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333
    QDRANT_COLLECTION: str = "conversation_messages"

    class Config:
        env_file = str(_LLM_DIR / ".env")
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "forbid"


# 全局单例
llm_settings = LLMSettings()
