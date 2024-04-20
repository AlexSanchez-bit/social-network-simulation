from openai import OpenAI
from ..nlp.llm import LLModel, LLMMessage
from ..constants import OPENAI_API_KEY, OPENAI_BASE_URL


class LLMOpenAI(LLModel):
    def __init__(self) -> None:
        self._client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL)
        self._model = "local-model"
        self._temp = 0.4
        
    def query(self, messages: list[LLMMessage]):
        msgs = [{
            'role': m.role,
            'content': m.content
        } for m in messages]
        
        completion = self._client.chat.completions.create(
            model=self._model,
            messages=msgs,
            temperature=self._temp
        )
        print(completion.choices[0].message)
        return completion.choices[0].message.content
