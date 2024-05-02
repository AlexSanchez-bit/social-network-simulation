from mesa import Agent, Model
from mesa.time import RandomActivation
import numpy as np
import random
import skfuzzy as fuzz
from skfuzzy import control as ctrl


posts = []

total_shares = 0

performed_an_action = True


class SocialAgent(Agent):
    def __init__(
        self,
        unique_id,
        model,
        affinity_beliefs,
        trust_beliefs,
        like_probability,
        share_probability,
        afinity_weight=0.5,
        relevance_weight=0.5,
        others_impact=0.3,
        friend_definition=0.6,
        curiosity=0.4,
        extroversion=0.3,
        reaction_brobability=0.8,
        imitation_influence=0.4,
        group_conformity=0.3,
        low_success_definition=0,
        mid_success_definition =1,
        high_success_definition =5,
        remembered_posts=[],
        memory_strength=1,
        post_probability=1,
        user_type_rules=[]
    ):
        super().__init__(unique_id, model)
        self.post_probability=post_probability
        self.user_type_rules = user_type_rules
        self.beliefs = {
            "affinity": affinity_beliefs,
            "trust": trust_beliefs,
            "share_probability": abs(share_probability),
            "like_probability": like_probability,
            "others_impact": others_impact,
            "friend_definition": friend_definition,
            "extroversion": extroversion,
            "curiosity": curiosity,
            "reaction_brobability": reaction_brobability,
            "group_likes":[ 0.000001 for _ in affinity_beliefs]

        }
        self.desires = {
            "most_liked_post": [],
            "most_disliked_post": [],
            "most_liked_score": 0,
            "most_unliked_score": 1,
            "friends": {},
            "afinity": afinity_weight,
            "relevance": relevance_weight,
            "imitation_influence": imitation_influence,
            "group_conformity": group_conformity,
            "post_target": affinity_beliefs,
        }
        self.intentions = []
        self.id = unique_id
        self.model = model
        self.low_success_def = low_success_definition
        self.mid_success_def = mid_success_definition
        self.high_success_def = high_success_definition
        
        self.remembered_posts = remembered_posts
        self.memory_strength = memory_strength
        self.most_popular_publications=[]
        
    def decide_next_action_to_do(self):
        pass

    def calculate_like_score(self, post_id):
        # Calcular el nivel de gusto hacia un post en base a las creencias
        norm1 = np.linalg.norm(posts[post_id]["features"])
        norm2 = np.linalg.norm(self.beliefs["affinity"])

        affinity_score = np.dot(posts[post_id]["features"], self.beliefs["affinity"])/(norm1*norm2)
        post_relevance = 0
        friends=0

        for user in self.beliefs["trust"]:
            if (
                self.beliefs["trust"][user] > self.beliefs["friend_definition"]
                and user in posts[post_id]["likes"]
            ):
                post_relevance += 1
                friends+=1
            if (
                self.beliefs["trust"][user] > self.beliefs["friend_definition"]
                and user in posts[post_id]["dislikes"]
            ):
                post_relevance -= 1
                friends+=1
        post_relevance /= max(friends, 1)
        post_relevance *= self.desires["group_conformity"]

        return (
            self.desires["afinity"] * affinity_score
            + self.desires["relevance"] * post_relevance
        )

    def decide_to_share(self, like_score, post_id):
        # calculating the intentions to share this post
        share_meter = like_score + np.random.random() * self.beliefs["extroversion"]
        # if itsh highlt probably for me to share then take the desition for each user of my network
        for friend_id in self.beliefs["trust"]:
            # obtaining the user relevance for me
            friend_rate = self.beliefs["trust"][friend_id]
            # if i like the post and i have high friendship with the user , then share
            if (friend_rate * share_meter) > self.beliefs["share_probability"]:
                self.intentions.append(
                    ("share", (friend_rate + like_score) / 2, post_id, friend_id)
                )

    def update_relationship(self, sender_id, like_score):
        # Actualizar la relación con el agente que compartió el post
        if sender_id in self.beliefs["trust"]:
            # calculando la afinidad actual al usuario
            last_afinity = self.beliefs["trust"][sender_id]
            # calculating the past interactions effect
            positive_interactions = 0
            negative_interactions = 0  # to avoiding divide by 0 error
            if sender_id in self.desires["friends"]:

                positive_interactions = (
                    self.desires["friends"][sender_id]["positive_interactions"]
                    / self.desires["friends"][sender_id]["total_interactions"]
                )

                # calculating the negative interactions so far
                negative_interactions = (
                    self.desires["friends"][sender_id]["negative_interactions"]
                    / self.desires["friends"][sender_id]["total_interactions"]
                )

            else:
                self.desires["friends"][sender_id] = {
                    "positive_interactions": 0,
                    "negative_interactions": 0,
                    "total_interactions": 0,
                }
            # calculating the confidence change based on the confidence_change and previous afinity value

            confidence_change = (
               ( like_score
                + np.random.random()
                * self.beliefs["extroversion"]
                * positive_interactions)
                / negative_interactions
                if negative_interactions > 0
                else 1
            ) 
            # if the change was positive , the afinity increases the new afinty grows in scale otherwise it decrease
            self.beliefs["trust"][sender_id] = confidence_change
        else:
            self.beliefs["trust"][sender_id] = 0
            self.desires["friends"][sender_id] = {
                "positive_interactions": 0,
                "negative_interactions": 0,
                "total_interactions": 0,
            }
        # update the interactions
        if like_score > 0:
            self.desires["friends"][sender_id]["positive_interactions"] += 1
        else:
            self.desires["friends"][sender_id]["negative_interactions"] += 1

        self.desires["friends"][sender_id]["total_interactions"] += 1

    def react_to_post(self, post_id, sender_id=None):
        if sender_id is not None:
            friend_trust = self.beliefs["trust"].get(sender_id, 0)

            positive_interactions = 0
            negative_interactions = 0

            if sender_id in self.desires["friends"]:
                positive_interactions = (
                    self.desires["friends"][sender_id]["positive_interactions"]
                    / self.desires["friends"][sender_id]["total_interactions"]
                )
                # calculating the negative interactions so far
                negative_interactions = (
                    self.desires["friends"][sender_id]["negative_interactions"]
                    / self.desires["friends"][sender_id]["total_interactions"]
                )
                

            react_probability = (
                friend_trust
                + np.random.random() * self.beliefs["curiosity"]
                + np.random.random() * positive_interactions
                + np.random.random() * negative_interactions
            ) /4

            if react_probability <= self.beliefs["reaction_brobability"]:
                return
            self.remembered_posts.append(len(posts)-1)
            while len(self.remembered_posts) > self.memory_strength:
                self.remembered_posts.pop(0)

        if len(self.most_popular_publications) > self.memory_strength:
            for i, index in enumerate(self.most_popular_publications):
                        if len(posts[post_id]['likes']) > len(posts[index]['likes']) :
                            self.most_popular_publications[i] = post_id
                            break
        else:
            self.most_popular_publications.append(post_id)
        # Calcular el nivel de gusto hacia el post
        like_score = self.calculate_like_score(post_id)

        liked_scores_relation = 0

        norm2 = np.linalg.norm(posts[post_id]["features"])
        for features in (
            self.desires["most_liked_post"] + self.desires["most_disliked_post"]
        ):
            # if the post features have been seen make a penalization
            norm1 = np.linalg.norm(features)
            if np.dot(posts[post_id]["features"], features)/(norm2*norm1) > 0.8:
                liked_scores_relation += 1

        like_score = like_score / max(liked_scores_relation, 1)
        self.align_ideas_with_friends(post_id)
        # Actualizar desires según el nivel de gusto
        if like_score > self.desires["most_liked_score"]:
            self.desires["most_liked_post"].append(posts[post_id]["features"])
            self.desires["most_liked_score"] = like_score
        elif like_score < self.desires["most_unliked_score"]:
            self.desires["most_disliked_post"].append(posts[post_id]["features"])
            self.desires["most_unliked_score"] = like_score

        # Actualizar la relación con el agente que compartió el post
        if sender_id is not None:
            disliked_score = 0
            norm2 = np.linalg.norm(posts[post_id]["features"])
            for features in self.desires["most_disliked_post"]:
                # if the post features is something i dont like penalize the relation with the sender
                norm1 = np.linalg.norm(features)
                if np.dot(posts[post_id]["features"], features)/(norm1*norm2) > 0.9:
                    disliked_score += 1
            self.update_relationship(sender_id, like_score / max(disliked_score, 1))

        self.decide_to_share(like_score, post_id)

        # Agregar la acción a intentions
        if like_score>0 and like_score <= self.beliefs["like_probability"]:
            self.intentions.append(("like", like_score, post_id))
        elif like_score >= -1 * self.beliefs["like_probability"]:
            self.intentions.append(("dislike", -1*like_score, post_id))

    def align_ideas_with_friends(self, post_id):
        post = posts[post_id]
        friends_who_likes_posts = 0
        friends = 0
        for friend_id, trust in self.beliefs["trust"].items():
            if trust >= self.beliefs["others_impact"]:
                friends += 1
                if friend_id in posts[post_id]["likes"]:
                    friends_who_likes_posts += 1
                elif friend_id in posts[post_id]["dislikes"]:
                    friends_who_likes_posts -= 1

        if len(self.beliefs['group_likes']) > 0:
            self.beliefs['group_likes']= [(x + y) / 2 for x, y in zip(posts[post_id]["features"], self.beliefs['group_likes'])]
        else:
            self.beliefs['group_likes']=posts[post_id]["features"]
        # si sus amigos aceptan una idea entonces el tambien las acepta
        friends_impact = friends_who_likes_posts / max(friends, 1)
        if friends_impact >= self.desires["group_conformity"]:
            move_vector = self.beliefs["affinity"] - posts[post_id]["features"]
            move_vector = move_vector / (np.linalg.norm(
                move_vector
            )+0.000000001)  # normalizing the vector
            move_vector = (
                move_vector * self.beliefs["others_impact"]
            )  # changing the believes in the matter of the impact of the others
            self.beliefs["affinity"] += move_vector
        return friends_impact
    

    def post_content(self):
                print('posting popular')
                posts.append(
                    {"features": self.desires['post_target'], "likes": [], "dislikes": [], "shared": 0,'author':self.id}
                )
                self.react_to_post(len(posts)-1)
                self.remembered_posts.append(len(posts)-1)
                while len(self.remembered_posts) > self.memory_strength:
                    self.remembered_posts.pop(0)
                
    def check_post_grow(self):
        memory_posts = random.randint(0,min(len(self.remembered_posts),self.memory_strength))
        on_mind_posts= random.sample(self.remembered_posts,memory_posts) 
        
        likes_universe = np.arange(0, max(max([len(post['likes']) for post in posts]),self.high_success_def)+1, 1)
        dislikes_universe = np.arange(0, max(max([len(post['dislikes']) for post in posts]),self.high_success_def)+1, 1)
        shares_universe = np.arange(0, max(self.high_success_def,max([post['shared'] for post in posts]))+1, 1)

        relevance = ctrl.Consequent(np.arange(0,1,0.00001),'relevance')
        group_conform = ctrl.Antecedent(np.arange(0,1,0.00001),'group_conform')
        
        likes_fuzzy = ctrl.Antecedent(likes_universe,'likes')
        dislikes_fuzzy = ctrl.Antecedent(dislikes_universe,'dislikes')
        shares_fuzzy = ctrl.Antecedent(shares_universe,'shared')

        
        likes_fuzzy['low_success'] = fuzz.trimf(likes_universe, [0, 0, self.low_success_def])
        likes_fuzzy['mid_success'] = fuzz.trimf(likes_universe, [self.mid_success_def, self.mid_success_def, self.high_success_def])
        likes_fuzzy['high_success'] = fuzz.trimf(likes_universe, [self.mid_success_def, self.high_success_def, self.high_success_def])
        
        
        dislikes_fuzzy['low_success'] = fuzz.trimf(dislikes_universe, [0, self.low_success_def, self.mid_success_def])
        dislikes_fuzzy['mid_success'] = fuzz.trimf(dislikes_universe, [self.mid_success_def, self.mid_success_def, self.high_success_def])
        dislikes_fuzzy['high_success'] = fuzz.trimf(dislikes_universe, [self.mid_success_def, self.high_success_def, self.high_success_def])
        
        shares_fuzzy['low_success'] = fuzz.trimf(shares_universe, [0, self.low_success_def, self.mid_success_def])
        shares_fuzzy['mid_success'] = fuzz.trimf(shares_universe, [self.mid_success_def, self.mid_success_def, self.high_success_def])
        shares_fuzzy['high_success'] = fuzz.trimf(shares_universe, [self.mid_success_def, self.high_success_def, self.high_success_def])

        

        relevance['no_relevance'] = fuzz.trimf(relevance.universe, [0, 0, 0.5])
        relevance['low_relevance'] = fuzz.trimf(relevance.universe, [0, 0.5, 1])
        relevance['mid_relevance'] = fuzz.trimf(relevance.universe, [0.5, 1, 1])
        relevance['high_relevance'] = fuzz.trimf(relevance.universe, [0.5, 1, 1])
        
        group_conform['no_group_conform'] = fuzz.trimf(group_conform.universe, [0, 0, 0.5])
        group_conform['low_group_conform'] = fuzz.trimf(group_conform.universe, [0, 0.5, 1])
        group_conform['mid_group_conform'] = fuzz.trimf(group_conform.universe, [0.5, 1, 1])
        group_conform['high_group_conform'] = fuzz.trimf(group_conform.universe, [0.5, 1, 1])


        
        reglas = []

        # Regla 1: Si hay alto éxito con likes y bajo éxito en dislikes, entonces es relevante
        reglas.append(ctrl.Rule(likes_fuzzy['high_success'] & dislikes_fuzzy['low_success'], relevance['high_relevance']))
        reglas.append(ctrl.Rule(likes_fuzzy['low_success'] | dislikes_fuzzy['high_success'], relevance['no_relevance']))
        reglas.append(ctrl.Rule(~likes_fuzzy['high_success'] | ~dislikes_fuzzy['high_success'], relevance['low_relevance']))
        # Regla 2: Si es relevante y se conforma al grupo, entonces sigue siendo relevante
        reglas.append(ctrl.Rule(relevance['high_relevance'] & group_conform['high_group_conform'], relevance['high_relevance']))

        # Regla 3: Si es relevante pero no se conforma al grupo, entonces no es relevante
        # reglas.append(ctrl.Rule(relevance['high_relevance'] & group_conform['no_group_conform'], relevance['no_relevance']))

        control_system = ctrl.ControlSystem(reglas)

        system = ctrl.ControlSystemSimulation(control_system)

        max_relevance = 0
        best_post = -1 
        for post in on_mind_posts:
            system.input['likes'] = len(posts[post]['likes'])
            system.input['dislikes'] = len(posts[post]['dislikes'])
            print(
                len(posts[post]['likes']),
                 len(posts[post]['dislikes'])
            )
            # system.input['shared'] = posts[post]['shared']
            system.input['group_conform'] = np.cos((np.dot(self.beliefs['group_likes'],posts[post]['features']))/(np.linalg.norm(self.beliefs['group_likes'])*np.linalg.norm(posts[post]['features'])))
            
            system.compute()
            
            if system.output['relevance'] > max_relevance:
                best_post = post
        if best_post >=0: 
            self.desires['post_target'] =posts[best_post]['features']
        

    def step(self):
        global performed_an_action
        global posts
        global total_shares
        agent_intentions = self.intentions
        
        tiempo_hasta_proxima_publicacion = np.random.exponential(1/ 0.1)
        
        if tiempo_hasta_proxima_publicacion < self.beliefs['curiosity']:
            self.check_post_grow()
        if tiempo_hasta_proxima_publicacion < self.post_probability:
            self.post_content()
        # sorting agent intentions by liked score
        agent_intentions = list(
            sorted(agent_intentions, key=lambda x: x[1], reverse=True)
        )
        # calculating next action to perform
        if len(agent_intentions) > 0:
            if len(agent_intentions) > 1:
                take = np.random.randint(0, len(agent_intentions) - 1)
                next_actions_to_perform = agent_intentions[:take]
                # updating intentions
                self.intentions = agent_intentions[take:]
            else:
                next_actions_to_perform = [self.intentions.pop()]

            for action in next_actions_to_perform:
                performed_an_action = True
                comand = action[0]
                weight = action[1]
                pid = action[2]
                print(f"agente: {self.id}")
                if comand == "like":
                    if self.id not in posts[pid]["likes"]:
                        if self.id in posts[pid]["dislikes"]:
                            posts[pid]["dislikes"].remove(self.id)
                        posts[pid]["likes"].append(self.id)
                        print("\t\tun like para el post", pid)
                if comand == "dislike":
                    if self.id not in posts[pid]["dislikes"]:
                        if self.id in posts[pid]["likes"]:
                            posts[pid]["likes"].remove(self.id)
                        posts[pid]["dislikes"].append(self.id)
                        print("\t\tun dislike para el post", pid)
                if comand == "share":
                    u_id = action[3]
                    posts[pid]["shared"] += 1
                    print(
                        f"\t\tcompartiendo el post {pid} a {u_id}"
                    )
                    self.model.schedule.agents[u_id].react_to_post(pid, self.id)
                    total_shares += 1


class SocialModel(Model):
    def __init__(self, N,characteristics,users_relation=0.5,like_prob_mean=0.5,share_prob_mean=0.5,others_impact_mean=0.6,affinity_means=None):
        super().__init__()
        self.num_agents = N
        self.schedule = RandomActivation(self)
        
        if affinity_means is None:
            affinity_means = [0 for characteristic in characteristics]

        # creando los agentes
        for i in range(self.num_agents):
            affinity_beliefs = np.clip(np.random.normal(loc=affinity_means, scale=0.1, size=len(affinity_means)),-1,1)
            # relaciones aleatrias con los usuarios de la red
            trust = np.clip(np.random.normal(loc=users_relation, scale=0.1, size=np.random.randint(N)),-1,1)
            trust_beliefs = {}
            for i, a in enumerate(trust):
                trust_beliefs[i] = a
                agent = SocialAgent(
                    i,
                    self,
                    affinity_beliefs=affinity_beliefs,
                    trust_beliefs=trust_beliefs,
                    like_probability=np.clip(np.random.normal(loc=like_prob_mean,scale=0.1),0,1),
                    share_probability=np.clip(np.random.normal(loc=share_prob_mean,scale=0.1),0,1),
                    afinity_weight=np.clip(np.random.normal(loc=0.5,scale=0.1),0,1),
                    relevance_weight=np.clip(np.random.normal(loc=0.5,scale=0.1),0,1),
                    others_impact=np.clip(np.random.normal(loc=others_impact_mean,scale=0.1),0,1),
                    friend_definition=np.clip(np.random.normal(loc=0.5,scale=0.1),0,1),
                    curiosity=np.clip(np.random.normal(loc=0.5,scale=0.1),0,1),
                    extroversion=np.clip(np.random.normal(loc=0.5,scale=0.1),0,1),
                    reaction_brobability=np.clip(np.random.normal(loc=0.5,scale=0.1),0,1),
                    imitation_influence=np.clip(np.random.normal(loc=0.5,scale=0.1),0,1),
                    group_conformity=np.clip(np.random.normal(loc=0.5,scale=0.1),0,1),
                    memory_strength=np.random.randint(len(posts))
                )
                self.schedule.add(agent)

    def step(self):
        self.schedule.step()
