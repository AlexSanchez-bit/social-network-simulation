from src.tools.SocialAgent import (
    SocialModel,
    posts,
    performed_an_action,
)
import numpy as np
from src.tools.DataAnalisys import (
    show_data_analisis,
    stadistics_per_characteristic,
    user_opinions
)

from src.tools.load_characteristics import load_characteristics

import sys

characteristics =None
def run_simulations(number_agents=10,number_posts=100,simulations_count=1,selectes_characteristics=[0,1,2,3,4,5],postgen_mean=None,user_afinity_means=None):
    global performed_an_action
    global characteristics
    global posts
    #loading characteristics from topic file
    if characteristics is None:
        characteristics = load_characteristics()
    #setting up the logs on a file 
    log_file = open('logs.txt','w')
    sys.stdout=log_file
    
    if postgen_mean is None:
        postgen_mean = [0.5 for _ in characteristics]
    if user_afinity_means is None:
        user_afinity_means= [0 for _ in characteristics]
    
    #the number of agents on the simulation
    N = number_agents
    posts_number=number_posts
    #saving the historical data
    history = []
    #change population on each simulation run
    change_population_each = False
    #variable for the simulation model
    model = None

    #array for the time in which the agents lost interest on the posts
    atention_time = []
    collected_opinions=[]

    for j in range(posts_number):
        post_features = np.clip(np.random.normal(loc=postgen_mean,size=len(characteristics)),0,1)
        posts.append(
              {"features": post_features, "likes": [], "dislikes": [], "shared": 0,'author':None}
        )
    for i in range(0, simulations_count):
        # generate more posts
        if i == 0 or change_population_each:
            model = SocialModel(N,characteristics,affinity_means=user_afinity_means)
        # Ejecutar la simulación
        horas = 0
        while horas < 1:
            print(f"----------------------horas{horas}----------------------------")
            for _ in range(0,np.random.randint(0,len(posts))):
                sender_id = np.random.randint(0, N)
                post_id = np.random.randint(0, len(posts))
                print(f"sistema: enviando el post {post_id} a el usuario {sender_id}")
                post = posts[post_id]  # Características aleatorias del post
                model.schedule.agents[sender_id].react_to_post(post_id)

            performed_an_action = False
            print(f"------------horas{horas}----------------")
            model.step()
            horas += 1

        print("=====================Fin de la simulacion====================")

        # saving data
        history.append(posts)
        performed_an_action = True
        atention_time.append(horas)
        current_opinions=np.array([agent.beliefs['affinity'] for agent in  model.schedule.agents])
        opinions_means = np.mean(current_opinions, axis=1)
        collected_opinions.append(opinions_means)


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
        posts, N, characteristics,selectes_characteristics, total_likes, total_dislikes, total_shares
    )
    user_opinions(np.array(collected_opinions),characteristics,selectes_characteristics)
    

    return (
        lambda x=None: show_data_analisis(posts, N, total_shares),
        lambda x=None: stadistics_per_characteristic(
            posts, N, characteristics,selectes_characteristics, total_likes, total_dislikes, total_shares
        ),
        lambda x=None: user_opinions(np.array(collected_opinions),characteristics,selectes_characteristics)
    )