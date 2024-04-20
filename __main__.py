# from src import nlp

# negative_prompt = "I would like to get the best possible growth in blackness for the most people. I want to reach as many people as possible but in a negative way."
# positive_prompt = "I want to reach as many people as possible"
# many_likes_prompt = "I want to have the greatest acceptance in the community, some may not like it, but only if there are few of them."

# x = nlp.extract_user_goals(negative_prompt)
# y = nlp.extract_user_goals(positive_prompt)
# # z = nlp.extract_user_goals(many_likes_prompt)

# print(x)
# print(y)
# # print(z)



from src.nlp.llm import LLMMessage
from src.nlp.llm_claude import LLMClaude

llm = LLMClaude()
message = LLMMessage('user', 'Tell me something about you')

x = llm.query(messages=message)

print(x)