import matplotlib.pyplot as plt
import numpy as np
# from sklearn.cluster import MeanShift


# Calcular la cantidad relativa de likes, dislikes y compartidos por post
def show_data_analisis(posts, usuarios_red_social, total_shares):
    likes_relativos = [len(post["likes"])  for post in posts]
    dislikes_relativos = [len(post["dislikes"])  for post in posts]
    compartidos_relativos = [post["shared"]  for post in posts]

    fig1, axs1 = plt.subplots()
    axs1.bar(range(len(posts)), likes_relativos, color="b")
    axs1.set_title("Likes Relativos por Post")
    axs1.set_ylabel("Likes Relativos")

    fig2, axs2 = plt.subplots()
    axs2.bar(range(len(posts)), dislikes_relativos, color="r")
    axs2.set_title("Dislikes Relativos por Post")
    axs2.set_ylabel("Dislikes Relativos")

    fig3, axs3 = plt.subplots()
    axs3.bar(range(len(posts)), compartidos_relativos, color="g")
    axs3.set_title("Compartidos Relativos por Post")
    axs3.set_ylabel("Compartidos Relativos")

    return fig1, fig2, fig3


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
                f"shares {round(scores[2],1)}",
            ]
        )

        # Establecer el rango de valores del eje radial
        ax.set_ylim(0, 1)

        # Añadir un título
        ax.set_title(f"Crecimiento de {all_characteristics[characteristics[i]]}")

    # Ajustar el diseño para evitar superposiciones
    plt.tight_layout()

    # Devolver la figura en lugar de mostrarla
    return fig
    

def user_opinions(M, all_characteristics, characteristics):
    mean_opinions = np.mean(M, axis=0)
    # Crear una nueva figura para las gráficas
    fig, ax = plt.subplots(figsize=(10, 5))
    # Iterar sobre las columnas de la matriz
    ax.plot(range(len(characteristics)), [mean_opinions[i] for i in characteristics], label=f'Promedio de opiniones', marker='o')  # Graficar la columna j vs los índices de fila

    # Configurar las etiquetas de los ejes y el título
    ax.set_xlabel(f"Características: {','.join(all_characteristics[x] for x in characteristics )}")
    ax.set_ylabel('Relevancia de la Característica')
    ax.set_title('opinión de los agentes respecto a las características')

    # Agregar leyenda
    ax.legend()

    # Devolver la figura en lugar de mostrarla
    return fig

