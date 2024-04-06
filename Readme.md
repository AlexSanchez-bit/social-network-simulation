# Proyecto IA - Simulacion

## Idea principal

### la idea principal de este proyecto es crear un simulador de redes sociales para analizar el alcance y crecimiento de los elementos de las publicaciones que se mueven en la red

### Ideas generales

- Representamos las publicaciones como vectores de caracteristicas , donde en cada posicion del vector hay un numero entre 0 y 1 que representa que tanto de esa caracteristica tiene el post
- Los Agentes de nuestra simulacion son agentes de razonamiento practico , que en sus believes guardan su relacion con el resto de usuarios de la red , en sus desires guardan la informacion de cuales han sido las caracteristicas que mas o menos le han gusstado y en sus intenciones las siguientes acciones a realizar y cuanto quieren hacerlas , basado en cuanto le gusto el post
- Tenemos la intencion de agregarles , reglas para compartir las publicaciones basadas en conocimiento , donde por cada usuario que tenga mayor que cierto grado de afinidad en la lista de conocidos se intente predecir sus gustos en base a las reacciones que ha tenido dada las publicaciones que se han compartido
  `esto funcionaria guardando en un grafo los usuarios y las caracteristicas conocidas en los gustos de ese usuario y este grafo se actualizara durante la simulacion`
- Luego de correr las simulaciones guardamos un indice de crecimiento de las caracteristicas individuales que definimos para los post , basados en los datos recolectados en la simulacion
- Usando metaheuristicas y estos datos generamos la publicacion (array de caracteristicas) mas optimas para la red y usando nlp devolvemos una descripcion de dicha publicacion al usuario de la simulacion

- la interfaz para interactuar y definir los parametros de la simulacion puede ser nlp
