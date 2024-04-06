from mesa import Agent, Model
from mesa.time import RandomActivation
import numpy as np

characteristics = ['technology-themed','has-picture','has-video','funny-themed','serious-theme','likes_given','dislikes_given','times_shared']

posts=[]

class SocialAgent(Agent):
    def __init__(self, unique_id, model, affinity_beliefs, trust_beliefs,like_probability,share_probability):
        super().__init__(unique_id, model)
        self.beliefs = {'affinity': affinity_beliefs, 'trust': trust_beliefs,'share_probability':share_probability,'like_probability':like_probability}
        self.desires = {'most_liked_post': [], 'most_disliked_post': [],'most_liked_score':0,'most_unliked_score':0,'friendship':{},'afinity':0.5,'relevance':0.5}
        self.intentions = []
        self.id=unique_id
    

    def calculate_like_score(self, post_id):
        # Calcular el nivel de gusto hacia un post en base a las creencias
        affinity_score = np.dot(posts[post_id]['features'], self.beliefs['affinity'])
        post_relevance = (posts[post_id]['likes'] + posts[post_id]['dislikes'] + posts[post_id]['shared'])
        return self.desires['afinity']* affinity_score + self.desires['relevance'] * post_relevance
    
    def decide_to_share(self,like_score,post_id):
            share_meter = like_score * np.random.random()
            if share_meter >= self.beliefs['share_probability']:
                for friend_id in self.beliefs['trust']:
                    friend_rate = self.beliefs['trust'][friend_id]
                    if (friend_rate + like_score)/2 >self.beliefs['share_probability']:
                        self.intentions.append(('share',like_score,post_id,friend_id))

    def update_relationship(self, sender_id, like_score):
        # Actualizar la relación con el agente que compartió el post
        if sender_id in self.beliefs['trust']:
             last_afinity = self.beliefs['trust'][sender_id] 
             confidence_change = like_score * 0.5 
             new_afnity = min(max(last_afinity+confidence_change,0),1)
             self.beliefs['trust'][sender_id] =new_afnity
        else:
            self.beliefs['trust'][sender_id] =0

    def react_to_post(self, post_id, sender_id=None):
        # Calcular el nivel de gusto hacia el post
        post_features =posts[post_id]['features']
        like_score = self.calculate_like_score(post_id)
        
        liked_scores_relation = 0
        
        for features in  self.desires['most_liked_post']+self.desires['most_disliked_post']:
        # if the post features have been seen make a penalization
            if np.dot(posts[post_id]['features'],features) >0.8:
                liked_scores_relation+=1
        
        like_score = like_score/max(liked_scores_relation,1)

        # Actualizar desires según el nivel de gusto
        if like_score > self.desires['most_liked_score']:
            self.desires['most_liked_post'].append( posts[post_id]['features'])
            self.desires['most_liked_score'] = like_score
        elif like_score < self.desires['most_unliked_score']:
            self.desires['most_disliked_post'].append( posts[post_id]['features'])
            self.desires['most_unliked_score'] = like_score
        
        # Actualizar la relación con el agente que compartió el post
        if sender_id is not None:
            disliked_score = 0
            for features in  self.desires['most_disliked_post']:
            # if the post features is somethong i dont like penalize the relation with the sender
                if np.dot(posts[post_id]['features'],features) >0.9:
                    disliked_score+=1
            self.update_relationship(sender_id, like_score/max(disliked_score,1))
        
        self.decide_to_share(like_score,post_id)
        
        # Agregar la acción a intentions
        if like_score > self.beliefs['like_probability']:
            self.intentions.append(('like',like_score,post_id))
        elif like_score < -1*self.beliefs['like_probability']:
            self.intentions.append(('dislike',like_score,post_id))
            
    def step(self):
            agent_intentions = self.intentions
            #sorting agent intentions by liked score
            agent_intentions = list(sorted(agent_intentions,key=lambda x:x[1],reverse=True))
            #calculating next action to perform 
            if len(agent_intentions) >0 :
                if len(agent_intentions) >1:
                    take = np.random.randint(0,len(agent_intentions)-1)
                    next_actions_to_perform = agent_intentions[:take]
                    #updating intentions
                    self.intentions = agent_intentions[take:]
                else:
                    next_actions_to_perform =[self.intentions[0]]

                print('\tacciones del agente: ',self.id)

                for action in next_actions_to_perform:
                    comand   = action[0]
                    pid = action[2]
                    if comand == 'like':
                        posts[pid]['likes']+=1
                        print('\t\tun dislike para el post',pid)
                    if comand == 'dislike':
                        posts[pid]['dislikes']+=1
                        print('\t\tun dislike para el post',pid)
                    if comand =='share':
                        u_id = action[3]
                        print(f'\t\tcompartiendo el post {pid} a {u_id}')
                        self.react_to_post(pid,u_id)



        

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

    #generate posts
    for i in range(10):
        post_features = np.random.rand(5) # Características aleatorias del post
        posts.append({'features':post_features,'likes':0,'dislikes':0,'shared':0})

    for i in range(0,10):
        sender_id = np.random.randint(0,N)
        post_id = np.random.randint(0,len(posts))
        print(f'sistema: enviando el post{post_id} a el usuario {sender_id}')
        post = posts[post_id]  # Características aleatorias del post
        model.schedule.agents[sender_id].react_to_post(post_id)

    # Ejecutar la simulación
    for _ in range(0,1):
        model.step()