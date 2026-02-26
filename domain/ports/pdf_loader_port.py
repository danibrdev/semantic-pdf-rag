from abc import ABC, abstractmethod


class PDFLoaderPort(ABC):
    @abstractmethod
    def load(self, path: str) -> str:
        pass
