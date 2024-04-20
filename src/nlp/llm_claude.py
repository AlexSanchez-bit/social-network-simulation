import anthropic
from llm import LLModel, LLMMessage
from ..constants import CLAUDE_API_KEY


class LLMClaude(LLModel):
    def __init__(self) -> None:
        self._client = anthropic.Anthropic(api_key = CLAUDE_API_KEY)
        self._max_tokens = 1024
        self._model = "claude-3-haiku-20240307"
        
    def query(self, messages: list[LLMMessage]):
        message = self._client.messages.create(
            model=self._model,
            max_tokens=self._max_tokens,
            messages=messages
        )
        
        return message.content