import abc
import json
from ..nlp.llm import LLModel, LLMMessage

SYSTEM_PROMPT = "You're a helpful AI assisting me in managing a social network simulation. You are an expect in community management and growth in social networks."


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
Based on the text with the goals of a user in the social network, it extracts three numbers that represent the relevance of likes, dislikes and shares for the user
achieve their objetives. The numbers will be in the [0, 1] range. Use only the context provided and don't add any other comments. Return the answer in JSON format 
with the keys: likes, dislikes and shares.
The user text:
<context>
{user_prompt}
<context>
Answer:         
""",
        "es": """
Basado en el texto con los objetivos de un usuario con la red social, extrae 3 números que representan la relevancia de los likes, dislikes y shares
para que el usuario obtenga su objetivo. Los números estarán en el rango [0,1]. Utiliza solo el contexto proporcionado y no añadas cualquier otro comentario.
Devuelve al respuesta en formato JSON con las llaves: likes, dislikes y shares.
El texto del usuario:
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
Your goal is extract from a user's text about their community on the social network the number of people who belong to the network.
Use just the given context and return just the number as the answer. If you don't know the answer, just return 0.
Here is the text:
<context>
{user_prompt}
<context>
Answer:
""",
        'es': """
Tu objetivo es extraer de un texto de un usuario sobre su comunidad en la red social el número de personas que pertenencen a la red.
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
Analyze the following description of a community on a social network and:
1. extract the topics relevant on the network and some others that may also be of interest. 
2. For each extracted topic, return a number at [0, 1] range that indicates the percentage of the community that may be interested in that topic.
Use only the information provided within the <context> tags, Return the topics as a array and each topic will be a object with the keys: name, relevance. Do not return any other comments.
<context>
{user_prompt}
<context>
Answer:
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
