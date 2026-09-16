"""本地 Embedding 服务实现 - 基于 sentence-transformers"""

from typing import List
from app.llm.embeddings.base import BaseEmbeddingService


class LocalEmbeddingService(BaseEmbeddingService):
    """本地 Embedding 服务
    
    使用 sentence-transformers 在本地运行模型，无需调用远程 API。
    首次加载模型时会从 HuggingFace 下载，之后使用本地缓存。
    """
    
    # 默认模型：all-MiniLM-L6-v2，384维，轻量高效
    DEFAULT_MODEL = "all-MiniLM-L6-v2"
    
    def __init__(self, model_name: str = DEFAULT_MODEL):
        """初始化
        
        Args:
            model_name: 模型名称（HuggingFace 模型 ID 或本地路径）
        """
        self._model_name = model_name
        self._model = None
        self._dimension: int | None = None
    
    def _ensure_model(self) -> None:
        """延迟加载模型（首次调用时才加载）"""
        if self._model is None:
            from sentence_transformers import SentenceTransformer
            self._model = SentenceTransformer(self._model_name)
            self._dimension = self._model.get_sentence_embedding_dimension()
    
    async def embed_text(self, text: str) -> List[float]:
        """将文本转换为向量"""
        self._ensure_model()
        embedding = self._model.encode(text, normalize_embeddings=True)
        return embedding.tolist()
    
    async def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """批量转换文本为向量"""
        self._ensure_model()
        embeddings = self._model.encode(texts, normalize_embeddings=True)
        return embeddings.tolist()
    
    @property
    def dimension(self) -> int:
        """向量维度"""
        if self._dimension is None:
            self._ensure_model()
        return self._dimension
