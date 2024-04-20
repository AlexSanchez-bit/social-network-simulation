import abc
import json
from ..nlp.llm import LLModel, LLMMessage

SYSTEM_PROMPT = "You're a helpful AI assisting me in managing a social network simulation."


class LLMJsonObjects(abc.ABC):
    def from_string(self, obj: str) -> bool:
        raise NotImplementedError()
class UserGloalsImportance(LLMJsonObjects):
    likes: float
    dislikes: float
    shares: float

    def from_string(self, str_obj: str) -> bool:
        try:
            data_dict = json.loads(str_obj)
            self.likes = data_dict['likes']
            self.dislikes = data_dict['dislikes']
            self.shares = data_dict['shares']
            
            return True
        except Exception as e:
            print(e)
            return False

    def __str__(self) -> str:
        return "({likes}, {dislikes}, {shares})".format(likes=self.likes, dislikes=self.dislikes, shares=self.shares)
class TopicRelevance(LLMJsonObjects):
    topic: str
    relevance: float
    
    def __init__(self, topic: str, relevance: float) -> None:
        assert 0 <= relevance <= 1, "The topic relevance must be between [0, 1]"
        self.topic = topic
        self.relevance = relevance
        
    def __str__(self) -> str:
        return "({topic}, {relevance})".format(topic=self.topic, relevance=self.relevance)


def extract_user_goals(user_prompt: str, llm: LLModel, temp=0.4, lang='en') -> UserGloalsImportance:
    assert len(map(lambda x: x.strip(), user_prompt.split(' '))) < 500, "Your prompt must be less than 500 words"

    PROMPTS = {
        "en": """
            Your goal is to extract from a text outlining a user's objectives with the simulation,
            three numbers between 0 and 1 representing the importance he attributes to the likes, dislikes, and shares of a post within the social network.
            To do this, carefully evaluate the user's motivations, goals, and feelings. All values must be different to zero. Extract this data based solely on the information.
            Return the result as a JSON with the properties: "likes", "dislikes" and "shares". Don't reply anything more.

            --------------------------------------------------------------------------------------------   
            {user_prompt}
            --------------------------------------------------------------------------------------------
            Result:
        """,
        "es": """
            Tu objetivo es extraer de un texto que plasma los objetivos de un usuario con la simulación, 
            tres números entre 0 y 1 que representan la importancia que él le atribuye a los likes, dislikes y shares de una publicación dentro de la red social.
            Para esto evalúa detenidamente las motivaciones del usuario, sus objetivos y sentimientos. Todos los valores deben ser diferentes de cero. Extrae estos datos basándote solo en la información de texto.
            Devuélve el resultado en formato JSON con las propiedades "likes", "dislikes" y "shares". No respondas mas nada.
            
            --------------------------------------------------------------------------------------------   
            {user_prompt}
            --------------------------------------------------------------------------------------------
            Resultado:
        """
    }
    
    try:
        prompt = PROMPTS[lang]
    except KeyError:
        print(f'{lang} is not a valid language. Expect: [es, en]')
        return None
    
    messages = [
        LLMMessage('system', SYSTEM_PROMPT),
        LLMMessage('user', prompt.format(user_prompt=user_prompt))
    ]

    result = llm.query(messages)
    data = UserGloalsImportance()
    ok = data.from_string(result)
    
    if ok:
        return data
    else:
        return None



def extract_number_agents(user_prompt: str, llm: LLModel, temp=0.4, lang='en') -> int:
    assert len(map(lambda x: x.strip(), user_prompt.split(' '))) < 500, "Your prompt must be less than 500 words"
    PROMPTS = {
        'en': """
            Your goal is extract from the user text within <context> tags, the number of peoples that belongs to the social network.
            Use just the given context and return just the number as the answer. If you don't know the answer, just return 0.
            <context>
            {user_prompt}
            <context>
            Answer:
        """,
        'es': """
            Tu objetivo es extraer del texto del usuario el número de personas que pertenencen a la red social.
            Usa solo el contexto proporcionado y devuelve solo el número como respuesta. Si no sabes la respuesta devuelve 0.
            Aquí está el texto:
            <context>
            {user_prompt}
            <context>
            Respuesta:
        """
    }
    
    try:
        prompt = PROMPTS[lang]
    except KeyError:
        print(f'{lang} is not a valid language. Expect: [es, en]')
        return None
    
    messages = [
        LLMMessage('system', SYSTEM_PROMPT),
        LLMMessage('user', prompt.format(user_prompt=user_prompt))
    ]

    result = llm.query(messages)
    return result
    

def extract_topics(user_prompt, llm: LLModel, temp=0.4, lang='en') -> list[TopicRelevance]:
    PROMPTS = {
        'en': """
            Analize the following description of a community in a social network and extract the topocs that are interestings in the network, and some others derivates 
            that maybe are interestings. Use just the information given within the <context> tags. Return the topics as an array, without any additional commentary.
        """,
        'es': """
            Analiza la siguiente descripción de una comunidad de una red social y:
            1. extrae los temas los temas relevantes para dicha red y algunos que pudieran interesar también.
            2. por cada tema extraído, devuelve un número entre 0 y 1 que indique el porcentaje de la comunidad que le puede interesar ese tema.
            
            Usolo la información proporcionada entre las etiquetas <context>. Devuelve los temas en forma de array y cada tema tenga las llaves name y relevance. No retornes ningún otro comentario.
            
            <context>
            {user_prompt}
            <context>
            Respuesta:
        """
    }
    
    try:
        prompt = PROMPTS[lang]
    except KeyError:
        print(f'{lang} is not a valid language. Expect: [es, en]')
        return None
    
    messages = [
        LLMMessage('system', SYSTEM_PROMPT),
        LLMMessage('user', prompt.format(user_prompt=user_prompt))
    ]

    result = llm.query(messages)
    parsed = json.loads(result)
    try:
        return [
            TopicRelevance(t['topic'], t['relevance'])
            for t in parsed
        ]
    except:
        return None
