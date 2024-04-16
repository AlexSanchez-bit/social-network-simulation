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
)


if __name__ == "__main__":
    # Crear un modelo con 10 agentes
    N = 50

    history = []

    change_population_each = False

    model = None

    atention_time = []

    for i in range(0, 8):
        # generate more posts
        for j in range(1000):
            post_features = np.random.random(5)  # Características aleatorias del post
            posts.append(
                {"features": post_features, "likes": [], "dislikes": [], "shared": 0}
            )

        print(i)
        if i == 0 or change_population_each:
            model = SocialModel(N)
            print("model created")
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
    print(np.mean(np.array(atention_time)))

    # show_users_groups([agent.beliefs["afinity"] for agent in model.schedule.agents])
    # for i,post in enumerate(posts):
    #     print('post' , i , post['likes']  ,post['dislikes'] ,post['shared'])
