from mesa import Agent, Model
from mesa.time import RandomActivation
import numpy as np

characteristics = ['technology-themed','has-picture','has-video','funny-themed','serious-theme','likes_given','dislikes_given','times_shared']

class SocialAgent(Agent):
    def __init__(self, unique_id, model, affinity_beliefs, trust_beliefs,like_probability,share_probability):
        super().__init__(unique_id, model)
        self.beliefs = {'affinity': affinity_beliefs, 'trust': trust_beliefs,'share_probability':share_probability,'like_probability':like_probability}
        self.desires = {'liked_post': None, 'disliked_post': None,'friendship':{}}
        self.intentions = []
    

    def calculate_like_score(self, post_features):
        # Calcular el nivel de gusto hacia un post en base a las creencias
        affinity_score = np.dot(post_features, self.beliefs['affinity'])
        return affinity_score
    
    def decide_to_share(self,like_score,post_features,post_id):
            share_meter = like_score * np.random.random()
            if share_meter >= self.beliefs['share_probability']:
                for friend_id in self.beliefs['trust']:
                    friend_rate = self.beliefs['trust'][friend_id]
                    if (friend_rate + like_score)/2 >self.beliefs['share_probability']:
                        self.intentions.append(('share',post_features,like_score,post_id,friend_id))

    def update_relationship(self, sender_id, like_score):
        # Actualizar la relación con el agente que compartió el post
        if sender_id in self.beliefs['trust']:
            self.beliefs['trust'][sender_id] += like_score
        else:
            self.beliefs['trust'][sender_id] -= like_score

    def react_to_post(self, post_features,post_id, sender_id=None):
        # Calcular el nivel de gusto hacia el post
        like_score = self.calculate_like_score(post_features)
        
        # Actualizar desires según el nivel de gusto
        if like_score > self.beliefs['share_probability']:
            self.desires['liked_post'] = post_features
        elif like_score < -1*self.beliefs['share_probability']:
            self.desires['disliked_post'] = post_features
        
        # Actualizar la relación con el agente que compartió el post
        if sender_id is not None:
            self.update_relationship(sender_id, like_score)
        
        self.decide_to_share(like_score,post_features,post_id)
        
        # Agregar la acción a intentions
        if like_score > self.beliefs['like_probability']:
            self.intentions.append(('like',post_features ,like_score,post_id))
        elif like_score < -1*self.beliefs['like_probability']:
            self.intentions.append(('dislike', post_features,like_score,post_id))
        

class SocialModel(Model):
    def __init__(self, N):
        super().__init__()
        self.num_agents = N
        self.schedule = RandomActivation(self)

        affinity_beliefs = np.random.rand(5)  # Creencias de afinidad aleatorias
        trust = np.random.random(np.random.randint(N))
        trust_beliefs = {}  # Relaciones iniciales vacías
        for i,a in enumerate(trust):
            trust_beliefs[i]=a


        # Crear agentes con creencias y relaciones iniciales
        for i in range(self.num_agents):
            agent = SocialAgent(i, self, affinity_beliefs, trust_beliefs,np.random.random(),np.random.random())
            self.schedule.add(agent)

    def step(self):
        self.schedule.step()

# Ejemplo de uso
if __name__ == "__main__":
    # Crear un modelo con 10 agentes
    N = 100
    
    model = SocialModel(N)
    
    #simular el envio de 5 publicaciones aleatorias a los agentes
    posts = []
    
    #generate posts
    for i in range(10):
        post_features = np.random.rand(5) # Características aleatorias del post
        posts.append(post_features)

    for i in range(10):
        sender_id = np.random.randint(N)
        post_id = np.random.randint(len(posts))
        post_features = posts[post_id]  # Características aleatorias del post
        model.schedule.agents[sender_id].react_to_post(post_features,post_id)

    # Ejecutar la simulación
    for _ in range(0,3):
        model.step()
    # Obtener las intenciones de un agente
        for i in range(0,N):
            #getting agent intentions
            agent_intentions = model.schedule.agents[i].intentions
            #sorting agent intentions by liked score
            agent_intentions = sorted(agent_intentions,key=lambda x:x[2],reverse=True)
            #calculating next action to perform 
            next_actions_to_perform = agent_intentions[:3]
            #updating intentions
            model.schedule.agents[i].intentions = agent_intentions[3:]
            
            print(f'next actionst to perform by agent {i}',next_actions_to_perform)
            
            for action in next_actions_to_perform:
                comand   = action[0]
                if comand == 'like':
                    pid = action[3]
                    print('un like para',pid)
                if comand == 'dislike':
                    print('un dislike para',pid)
                if comand =='share':
                    pid,u_id = action[3:5]
                    print(f'compartiendo {pid} a {u_id}')
                    model.schedule.agents[u_id].react_to_post(posts[pid],u_id)


