# # from src import nlp

# # negative_prompt = "I would like to get the best possible growth in blackness for the most people. I want to reach as many people as possible but in a negative way."
# # positive_prompt = "I want to reach as many people as possible"
# # many_likes_prompt = "I want to have the greatest acceptance in the community, some may not like it, but only if there are few of them."

# # x = nlp.extract_user_goals(negative_prompt)
# # y = nlp.extract_user_goals(positive_prompt)
# # # z = nlp.extract_user_goals(many_likes_prompt)

# # print(x)
# # print(y)
# # # print(z)



# from src.nlp.llm import LLMMessage
# from src.tools.llm_claude import LLMClaude

# llm = LLMClaude()
# message = LLMMessage('user', 'Tell me something about you')

# x = llm.query(messages=[message])

# print(x)
from SocialAgent import (
    SocialModel,
    posts,
    performed_an_action,
    characteristics,
)
import numpy as np
from DataAnalisys import (
    show_data_analisis,
    stadistics_per_characteristic,
    user_opinions
)


if __name__ == "__main__":
    # Crear un modelo con 10 agentes
    N = 1000
    simulations_count=1

    history = []

    change_population_each = False

    model = None

    atention_time = []

    for i in range(0, simulations_count):
        # generate more posts
        for j in range(1000):
            post_features = np.random.random(5)  # Características aleatorias del post
            posts.append(
                {"features": post_features, "likes": [], "dislikes": [], "shared": 0}
            )

        if i == 0 or change_population_each:
            model = SocialModel(N)
        # sending initial posts to agents
        for k in range(0, 3001):
            sender_id = np.random.randint(0, N)
            post_id = np.random.randint(0, len(posts))
            print(f"sistema: enviando el post {post_id} a el usuario {sender_id}")
            post = posts[post_id]  # Características aleatorias del post
            model.schedule.agents[sender_id].react_to_post(post_id)

        # Ejecutar la simulación
        horas = 0
        while performed_an_action:
            performed_an_action = False
            print(f"------------horas{horas}----------------")
            model.step()
            horas += 1

        print("=====================Fin de la simulacion====================")

        # saving data
        history.append(posts)
        performed_an_action = True
        atention_time.append(horas)

    total_shares = 0
    total_likes = 0
    total_dislikes = 0

    for p, post in enumerate(posts):
        total_likes += len(post["likes"])
        total_dislikes += len(post["dislikes"])
        total_shares += post["shared"]
    print(total_dislikes, total_likes, total_shares)
    show_data_analisis(posts, N, total_shares)
    stadistics_per_characteristic(
        posts, N, characteristics, total_likes, total_dislikes, total_shares
    )
    collected_opinions =np.array([agent.beliefs['affinity'] for agent in  model.schedule.agents])
    user_opinions(collected_opinions,characteristics)
    print(np.mean(np.array(atention_time)))

    # show_users_groups([agent.beliefs["afinity"] for agent in model.schedule.agents])
    # for i,post in enumerate(posts):
    #     print('post' , i , post['likes']  ,post['dislikes'] ,post['shared'])
