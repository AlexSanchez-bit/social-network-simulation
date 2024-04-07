# Proyecto IA - Simulacion

## Instrucciones

### Variables de entorno

Crea un fichero `.env` en la raiz del proyecto y añade las siguentes variables de entorno:

```bash
OPENAI_BASE_URL="http://localhost:1234/v1"
OPENAI_API_KEY="no-needed"
```


## Idea principal

> La idea principal de este proyecto es crear un simulador de redes sociales para analizar el alcance y crecimiento de los elementos de las publicaciones que se mueven en la red

### Ideas generales

- Representamos las publicaciones como vectores de caracteristicas , donde en cada posicion del vector hay un numero entre 0 y 1 que representa que tanto de esa caracteristica tiene el post
- Los Agentes de nuestra simulacion son agentes de razonamiento practico , que en sus believes guardan su relacion con el resto de usuarios de la red , en sus desires guardan la informacion de cuales han sido las caracteristicas que mas o menos le han gusstado y en sus intenciones las siguientes acciones a realizar y cuanto quieren hacerlas , basado en cuanto le gusto el post
- Tenemos la intencion de agregarles , reglas para compartir las publicaciones basadas en conocimiento , donde por cada usuario que tenga mayor que cierto grado de afinidad en la lista de conocidos se intente predecir sus gustos en base a las reacciones que ha tenido dada las publicaciones que se han compartido. __Esto funcionaria guardando en un grafo los usuarios y las caracteristicas conocidas en los gustos de ese usuario y este grafo se actualizara durante la simulacion__

- Luego de correr las simulaciones guardamos un indice de crecimiento de las caracteristicas individuales que definimos para los post , basados en los datos recolectados en la simulacion
- Usando metaheuristicas y estos datos generamos la publicacion (array de caracteristicas) mas optimas para la red y usando nlp devolvemos una descripcion de dicha publicacion al usuario de la simulacion

- la interfaz para interactuar y definir los parametros de la simulacion puede ser nlp

### Modelacion de los agentes:

- Cada agente guarda su relacion con el resto de agentes
- Cada agente guarda los post que mas le han gustado y los que menos
- Cada agente tiene una probabilidad de compartir un post a otro y una de darle like a un post
- Cada agente tiene sus gustos especificos

### Comportamiento de los agentes en la Simulacion

- En cada paso de la simulacion los agentes actualizan sus intentions para seleccionar la proxima accion a realizar
- Como simplificacion en la red no aparecen nuevos posts , solo los emitidos en un principios que llevan las caracteristicas que nos interesa medir
- Los agentes solo reaccionan a posts que les envian otros agentes o los que les envia el sistema al inicio de la simulacion
- Los agentes puden dar like a la publicacion que estan viendo , dar dislike o escoger no hacer nada
- Actualizan su relacion con el agente que les envio el post
- En base a la relacion que tienen con otros agentes pueden elegir compartir la publicacion con estos
- Recuerdan solo las publicaciones que han sido sus favoritas en el pasado o aquellas que no les han gustado nada en el pasado (como un humano)
- Si una publicacion tiene caracteristicas que el agente ha visto mucho , se penaliza dicha publicacion
- En cada paso de la simulacion se selecciona un numero aleatprio 'N' y se toman las N acciones que mas quiere hacer el agente en sus intentions y se ejecutan

### Modelos Matematicos

#### Para modelar la interaccion entre los agentes de la red Modelamos matematicamente sus interacciones

- Nos basamos en el Modelo de treshhold para simular como se propaga la informacion por internet cada agente tiene un umbral entre la afinidad con el resto de los agentes y cuanto le gusto el post para saber si compartir el post con otros agentes (inicialmente los valores de los umbrales son 0.5 y 0.5)
- Para la relacion entre los usuarios de la red utilizamos numeros entre 0 y 1 donde 0 significa que se conocen pero no son nada amigos y 1 que son amigos
- Se calcula la probabilidad de que comparta el post 'i' al usuario 'j' haciendo un promedio entre la relacion que se tiene con el usuario j y cuanto le gusto la publicacion i , si supera la probabilidad de compartir una publicacion que tiene el agente , entonces se agrega a las intentions del agente la accion de compartir la publicacion 'i' al usuario 'j' con peso lo que le gusto el post


## Contribuidores

[![Contribuidores](https://contrib.rocks/image?repo=AlexSanchez-bit/social-network-simulation)](https://github.com/AlexSanchez-bit/social-network-simulation/graphs/contributors)