from abc import ABC, abstractmethod


class BaseLLMProvider(ABC):
    provider_name = ""

    @abstractmethod
    def generate(self, prompt: str, system_prompt: str = "") -> str:
        raise NotImplementedError
