from openai import OpenAI
import constants

client = OpenAI(base_url=constants.OPENAI_BASE_URL, api_key=constants.OPENAI_API_KEY)

user_input = "I need create a simulation with 10 persons that they are friends in a social network. Also, i need simulate this interactions 55 times."

completion = client.chat.completions.create(
    model="local-model",
    messages=[
        {"role": "system", "content": "You're an expert in social networks simulations and you're very good extracting information realated from a text."},
        {"role": "user", "content": f"""
            Given a text of an user between <content></content> tag, extract all information given below:
            - Number of persons in the social network for the simulation.
            - Number of iterations of the simulation.

            Extract only the information mentioned above. Do not invent values that don't exist.
            Extract the information in format json with the follow fields: number_persons, number_iterations.
            If some of this values don't exits, simply don't include this field in the json.
            
            <content>
            {user_input}
            </content>
         """
         }
    ],
    temperature=0.4
)



print(completion.choices[0].message)