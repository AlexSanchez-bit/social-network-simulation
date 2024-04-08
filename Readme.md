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


# Obteniendo el mejor post

## Datos de la simulación

En la simulacion existen $n$ características que describen los diferentes temas de los que puede tratar un post, como `tecnología`, `ciencia`, `medio ambiente`, `política`, etc. Cada post en la red social tiene un vector $v$ de $n$ dimensiones con valores $v_i \in [0, 1]$ que indica que tan relevante es el tema $i$ en el post.
También, de la simulación se extrae para cada característica, tres indicadores importantes. Para una publicación con tema $i$ se extrae:

- Porcentaje de la red que le da likes a una publicación donde el tema $i$ sea relevante.
- Porcentaje de la red que le da dislikes a una publicación donde el tema $i$ sea relevante.
- Porcentaje de la red que comparte una publicación donde el tema $i$ sea relevante.

Por tanto, podemos crear una matrix $C{n,3}$ donde $C_{i,j}$ indica que porcentaje de la red tuvo la reacción $j$ en posts donde el tema $i$ es relevante.

## Función objetivo

El objectivo es entonces encontrar el vector $v$ tal que tenga la mejor combinación de relevancias por cada característica y nos dé el mayor crecimiento en la red. Como el impacto de una post de un tema $i$ se mide por los 3 índices expuestos anteriormente (`likes`, `dislikes`, `shared`), entonces necesitamos un valor que indique cuan relevante es este índice para un post. Sea $\alpha, \beta, \lambda \in [-1, 1]$ los respectivos indices de relevancia, en donde $-1$ afecta muy negativamente al post y $1$ afecta muy positivamente al post.

Por otro lado para medir el impacto de una publicación en la red esta se podría calcular como:
$$
I(v) = \alpha g_1(v) + \beta g_2(v) + \lambda g_3(v)
$$
donde $g_1(v), g_1(v)$ y $g_1(v)$ indican cuanto afectan los indices de crecimiento respectivamente entre todos los temas.

La forma de calcular las 3 funciones son la misma, solo que se separan en funciones diferentes para mejor comprensión. Para esto hacemos uso de la función exponencial para recompenzar las a los valores mas grandes de $x$. Entonces podemos definir la función $g_1(v)$ que indica cuanto ... como:

$$
g_1(v) = v_1 \alpha e ^ {\sum_{i=1}^{n} C_{i,1}} 
$$

Entonces la función en su totalidad la podemos expresar como:
$$
I(v) = \alpha g_1(v) + \beta g_2(v) + \lambda g_3(v) = v_1 \alpha e ^ {\sum_{i=1}^{n} C_{i,1}} + v_2 \beta e ^ {\sum_{i=1}^{n} C_{i,2}} + v_3 \lambda e ^ {\sum_{i=1}^{n} C_{i,3}}
$$

Si definimos el vector $z = [\alpha, \beta, \lambda]$ entonces la función quedaría:
$$
I(v) = \sum_{j=1}^{3} z_j v_i  e ^ {\sum_{i=1}^{n} C_{i,j}}
$$

Ahora bien, como queremos hallar el vector $x$ tal que maximize el impacto en la red entonces tenemos que optimizar la funcion $I$ para calcular el máximo:
$$
\max I(v) = \max \sum_{j=1}^{3} z_j v_i e ^ {\sum_{i=1}^{n} C_{i,j}}
$$

## Contribuidores

[![Contribuidores](https://contrib.rocks/image?repo=AlexSanchez-bit/social-network-simulation)](https://github.com/AlexSanchez-bit/social-network-simulation/graphs/contributors)