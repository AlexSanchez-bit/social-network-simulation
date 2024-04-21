import matplotlib.pyplot as plt
import numpy as np
# from sklearn.cluster import MeanShift


# Calcular la cantidad relativa de likes, dislikes y compartidos por post
def show_data_analisis(posts, usuarios_red_social, total_shares):
    likes_relativos = [len(post["likes"])  for post in posts]
    dislikes_relativos = [len(post["dislikes"])  for post in posts]
    compartidos_relativos = [post["shared"]  for post in posts]

    # Crear una sola ventana con tres gráficas
    fig, axs = plt.subplots(3)

    # Graficar likes relativos
    axs[0].bar(range(len(posts)), likes_relativos, color="b")
    axs[0].set_title("Likes Relativos por Post")
    axs[0].set_ylabel("Likes Relativos")

    # Graficar dislikes relativos
    axs[1].bar(range(len(posts)), dislikes_relativos, color="r")
    axs[1].set_title("Dislikes Relativos por Post")
    axs[1].set_ylabel("Dislikes Relativos")

    # Graficar compartidos relativos
    axs[2].bar(range(len(posts)), compartidos_relativos, color="g")
    axs[2].set_title("Compartidos Relativos por Post")
    axs[2].set_ylabel("Compartidos Relativos")

    # Ajustar el espacio entre subgráficas para evitar solapamientos
    plt.tight_layout()

    # Mostrar el gráfico
    plt.show()


def stadistics_per_characteristic(
    posts, users_in_network,all_characteristics, characteristics, total_likes, total_dislikes, total_shares
):
    # Número de características
    individual_scores = []

    for characteristic_index in characteristics:
        likes_sum = 0
        dislikes_sum = 0
        shared_sum = 0

        for post in posts:
            if post["features"][characteristic_index] > 0.7:
                likes_sum += len(post["likes"])
                dislikes_sum += len(post["dislikes"])
                shared_sum += post["shared"]
        total_dislikes = max(total_dislikes, 1)
        total_likes = max(total_likes, 1)
        individual_scores.append(
            [
                likes_sum / total_likes,
                dislikes_sum / total_dislikes,
                shared_sum / max(total_shares, 1),
            ]
        )

    # Crear la figura y los ejes polar
    fig, axs = plt.subplots(
        1, len(characteristics), subplot_kw=dict(polar=True), figsize=(15, 6)
    )

    # Iterar sobre cada subgráfico y dibujar el mismo gráfico en cada uno
    for i, ax in enumerate(axs):
        # Ángulos para cada característica
        angulos = np.linspace(
            0, 2 * np.pi, 3, endpoint=False
        ).tolist()

        # Agregar el primer ángulo al final para cerrar el polígono
        angulos += [angulos[0]]

        scores = individual_scores[i]

        # Puntajes para cerrar el polígono (agrega el ultimo al inicio)
        scores += [scores[0]]
        # Dibujar el polígono
        ax.fill(angulos, scores, color="blue", alpha=0.25)

        # Dibujar cada característica como una línea desde el centro
        ax.plot(angulos, scores, color="red", linewidth=2)

        # Marcar cada punto con el nombre de la característica
        ax.set_xticks(angulos[:-1])
        ax.set_xticklabels(
            [
                f"likes:{round(scores[0],1)}",
                f"dislikes: {round(scores[1],1)}",
                f"veces compartido {round(scores[2],1)}",
            ]
        )

        # Establecer el rango de valores del eje radial
        ax.set_ylim(0, 1)

        # Añadir un título
        ax.set_title(f"Crecimiento de {all_characteristics[characteristics[i]]}")

    # Ajustar el diseño para evitar superposiciones
    plt.tight_layout()

    # Mostrar la gráfica
    plt.show()
    
def user_opinions(M,all_characteristics,characteristics):
    # Crear una nueva figura para las gráficas
    plt.figure(figsize=(10, 5))
    n,m = M.shape 
    # Iterar sobre las columnas de la matriz
    for i in range(n):
        mean_values=[]
        for j in characteristics:
            mean_values.append(M[i,j])
        plt.plot(range(len(characteristics)),mean_values, label=f'avance de las opiniones en la iteracion{i} ')  # Graficar la columna j vs los índices de fila

    # Configurar las etiquetas de los ejes y el título
    plt.xlabel(f"Características: {','.join(all_characteristics[x] for x in characteristics )}")
    plt.ylabel('Relevancia de la Característica')
    plt.title('opinión de los agentes respecto a las características')

    # Agregar leyenda
    plt.legend()

    # Mostrar la gráfica
    plt.show()

