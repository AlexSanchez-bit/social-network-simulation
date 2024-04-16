from openai import OpenAI
import constants

client = OpenAI(base_url=constants.OPENAI_BASE_URL, api_key=constants.OPENAI_API_KEY)

user_input = "I need create a simulation with 10 persons that they are friends in a social network. Also, i need simulate this interactions 55 times."

SYSTEM_PROMPT = """
    You're an helpful AI agent expert in social networks simulations. You're very good extracting information from a text.
"""

EXTRACTOR_PROMPT = """
    According to the follow text between <content></content> tags, extract all information given below:
    - Number of persons in the social network for the simulation.
    - Number of iterations of the simulation.

    Extract only the information mentioned above. Do not invent values that don't exist.
    Reply the information in json format with the follow fields: number_persons, number_iterations. Don't reply anything else.
    If some of this values don't exits, don't include it in the json.
    
    <content>
    {user_input}
    </content>
    
    Json: 
"""




completion = client.chat.completions.create(
    model="local-model",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": EXTRACTOR_PROMPT.format(user_input=user_input)
         }
    ],
    temperature=0.4
)


print(completion.choices[0].message)