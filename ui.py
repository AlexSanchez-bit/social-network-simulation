import streamlit as st
import numpy as np
from src.tools.llm_claude import LLMClaude
from src.tools.prompts import extract_number_agents, extract_topics, extract_user_goals, build_post, TopicRelevance
from src.tools.topics import build_topics_relevances
from src.tools.meta import run_meta
from src.tools.load_characteristics import load_characteristics

from src.simulation import run_simulations

st.title('Metrics in your Community')
st.subheader("Learn to grow more in your network")

def process_input(prompt:str, words=50):
    if len(prompt.split()) < words:
        st.warning("The prompt must have atleast 50 words.")
        return

    llm = LLMClaude()
    number_agent = extract_number_agents(prompt, llm=llm)
    user_goals = extract_user_goals(prompt, llm=llm)
    user_topics = extract_topics(prompt, llm=llm)
    eq_topics, topics_relevance = build_topics_relevances(user_topics)

    x, y = st.columns(2)
    with x:
        st.write(f"__Number of people__: {number_agent}")
    with y:
        st.write(f"__User goals__: {user_goals}")
    
    v, w = st.columns(2)
    with v:
        st.write("__SN Topics__")
        st.write(user_topics)
    with w:
        st.write("__Our similar SN Topics__:")
        st.write([t['name'] for t in eq_topics])
    
    # tienes que pasarle un array con los indices que interesan y el otro con los pesos
    a, b, c = run_simulations(
        number_agents=number_agent,
        number_posts=30,
        simulations_count=10,
        selectes_characteristics=np.array([t['id'] for t in eq_topics]),
        postgen_mean=topics_relevance,
        user_afinity_means=topics_relevance
    )

    a1, a2, a3 = st.columns(3)
    f1, f2, f3 = a()
    with a1:
        st.pyplot(f1)
    with a2:
        st.pyplot(f2)
    with a3:
        st.pyplot(f3)
    
    f4, C = b()
    st.pyplot(f4)
    
    f5 = c()
    st.pyplot(f5)
    
    st.subheader("Best post that satisfies your goals")
    best_sol = run_meta(
        C, 
        rel=np.array([user_goals.likes, user_goals.dislikes, user_goals.shares]), 
        pp=np.array([t['id'] for t in eq_topics])
    )

    topics = load_characteristics()
    showing = [(topics[i], v) for [i,v] in best_sol]
    for [topc, v] in showing:
        st.write(f"Topic: {topc}, Pertenece: {v}")        

    st.write('### Example of a post')
    post = build_post(
        [TopicRelevance(tpc, v) for (tpc, v) in showing],
        llm=llm
    )
    st.write(post)

prompt = st.text_area(label="Describe your community, the number of people, what topics they talk about and what type of reach you want in your network.", height=200)
button = st.button('Execute')

if button:
    process_input(prompt)











st.write('#### Examples')
left, right = st.columns(2)
with left:
    card = st.container(border=True)
    card.caption("""
My community in discord has  around of 1000 people. Here, i share content about programming and software development mainly. Often i share content about artificial intelligence and the people like it so much. Also i make some posts about my career in the software development. Generally, people like AI content much more than personal growth content. I would like to be able to continue creating content in a smarter way to grow my community and reach the greatest number of people possible, and help them in their professional life.
""")
# Mi comunidad en discord tiene aproximadamente 1000 personas. Aquí comparto contenido sobre programación y desarrollo de software principalente.
# A veces comparto contenido sobre inteligencia artificial y a la gente le gusta mucho. Tambien hago algunas publicaciones hablando sobre mi trayectoria
# en el desarrollo de software. Generalmente a la gente le gusta mucho mas el contenido de AI que de crecimiento personal. Quisiera poder seguir creando contenido
# de una forma mas inteligente para hacer crecer mi comunidad y llegar al mayor número de personas posible y ayudarlos en su vida profesional.
    
with right:
    card = st.container(border=True)
    card.caption("""
I currently have 70 followers on twitter. I don't upload a lot of content but i would like to start publishing more content to growing my network. I really like the whole world of software development, building interesting applications for people. I also like a little of researching the field of Artificial Intelligence and how we can use it as a tool to create powerful applications. I also research and sometimes do things related to cryptocurrencies, blockchain, trading and more.  
""")
# Actualmente tengo 70 seguidores en twitter. No subo mucho contenido pero quisiera empezar a publicar mas contenido para hacer crecer mi red. Me gusta mucho todo 
# el mundo del desarrollo de software, construir aplicaciones interesantes para las personas. También me gusta un poco la investigación en el campo de la
# inteligencia artificial y como usarla como herramienta para crear aplicaciones poderosas. También investigo y a veces hago cosas relacionadas con  las criptomonedas,
# la blockchain, el trading y demás.

card = st.container(border=True)
card.caption("""
I'm a cryptocurrency hater. I am following several youtubers related to crypto world, and i would like them to lower their reach and earn less money with their videos. I want to act negatively towards their communities, even tell lies just for them to be affected. In total, they must have around 5000 people who support them, and i want most of them to stop following them.
""")
# Soy un hate de las criptomonedas. Estoy siguendo a varios creadores de contenido en youtube relacionados con las criptos y quisiera que bajen su alcance y ganen
# menos dinero con los videos de youtube. Quiero interactuar negativamente con sus comunidades, decir incluso mentiras solo para que se vean afectados. En total 
# deben tener al rededor de 5000 personas que los apoyan, y quiero q la mayoría los dejen de seguir.
