"""Embedding 服务基类"""

from abc import ABC, abstractmethod
from typing import List


class BaseEmbeddingService(ABC):
    """Embedding 服务抽象基类"""
    
    @abstractmethod
    async def embed_text(self, text: str) -> List[float]:
        """将文本转换为向量"""
        pass
    
    @abstractmethod
    async def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """批量转换文本为向量"""
        pass
    
    @property
    @abstractmethod
    def dimension(self) -> int:
        """向量维度"""
        pass
