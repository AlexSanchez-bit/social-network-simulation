import anthropic
from ..nlp.llm import LLModel, LLMMessage
from ..constants import CLAUDE_API_KEY


class LLMClaude(LLModel):
    def __init__(self) -> None:
        self._client = anthropic.Anthropic(api_key = CLAUDE_API_KEY)
        self._max_tokens = 1024
        self._model = "claude-3-haiku-20240307"
        
    def query(self, messages: list[LLMMessage]):
        num_sys_msgs = len(list(filter(lambda m: m.role == 'system', messages))) 
        assert num_sys_msgs <= 1, "Claude only accept a message with the system role"
        assert num_sys_msgs == 0 or (num_sys_msgs == 1 and messages[0].role == 'system'), "The message with system rol must be the first message"
        
        sys_msg = messages[0].content if messages[0].role == 'system' else None
        msgs = [{
            'role': m.role,
            'content': m.content
        } for m in messages if m.role != 'system']
                        
        message = self._client.messages.create(
            model=self._model,
            max_tokens=self._max_tokens,
            system=sys_msg,
            messages=msgs
        )

        return message.content[0].text