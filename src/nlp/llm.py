import abc

class LLMMessage:
    role: str
    content: str
    
    def __init__(self, role, content) -> None:
        self.role = role
        self.content = content 
        

class LLModel(abc.ABC):
    
    @abc.abstractmethod
    def query(self, messages: list[LLMMessage]):
        raise NotImplementedError()
    
