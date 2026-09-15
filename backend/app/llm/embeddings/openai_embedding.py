"""OpenAI Embedding 服务实现"""

from typing import List
from langchain_openai import OpenAIEmbeddings
from app.llm.embeddings.base import BaseEmbeddingService
from app.llm.config import llm_settings


class OpenAIEmbeddingService(BaseEmbeddingService):
    """OpenAI Embedding 服务"""
    
    def __init__(self, model: str = "text-embedding-3-small"):
        """
        初始化
        
        Args:
            model: Embedding 模型名称
        """
        self._model = model
        self._client = OpenAIEmbeddings(
            model=model,
            openai_api_key=llm_settings.OPENAI_API_KEY,
            openai_api_base=llm_settings.OPENAI_BASE_URL,
        )
    
    async def embed_text(self, text: str) -> List[float]:
        """将文本转换为向量"""
        vectors = await self._client.aembed_documents([text])
        return vectors[0]
    
    async def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """批量转换文本为向量"""
        return await self._client.aembed_documents(texts)
    
    @property
    def dimension(self) -> int:
        """向量维度"""
        # text-embedding-3-small 和 text-embedding-3-large 都是 1536 维
        return 1536
