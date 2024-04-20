import anthropic
from ..nlp.llm import LLModel, LLMMessage
from ..constants import CLAUDE_API_KEY


class LLMClaude(LLModel):
    def __init__(self) -> None:
        self._client = anthropic.Anthropic(api_key = CLAUDE_API_KEY)
        self._max_tokens = 1024
        self._model = "claude-3-haiku-20240307"
        
    def query(self, messages: list[LLMMessage]):
        msgs = [{
            'role': m.role,
            'content': m.content
        } for m in messages]
        
        message = self._client.messages.create(
            model=self._model,
            max_tokens=self._max_tokens,
            messages=msgs
        )
        print(message.content)
        return message.content[0].text