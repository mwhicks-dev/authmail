from abc import ABC, abstractmethod

class IResponseGenerator(ABC):

    @abstractmethod
    def generate_response(self) -> str:
        pass