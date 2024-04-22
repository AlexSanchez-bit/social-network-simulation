# Proyecto IA - Simulacion

> Informe detallado [aquí](./doc/informe.pdf)

## Integrantes

| **Nombre**                  | **Grupo** | **Github**                                             |
|-----------------------------|-----------|--------------------------------------------------------|
| Carlos Manuel González Peña |   C411    | [@cmglezpdev](https://github.com/cmglezpdev)           |
| Alez Sanchez Saez           |   C412    | [@AlexSanchez-bit](https://github.com/AlexSanchez-bit) |
| Jorge Alberto Aspiolea      |   C412    | [@aspio28](https://github.com/aspio28)                 |

## Descripción

El proyecto consiste en realizar una simulación de las interacciones en una red social teniendo un conjunto de caracteristicas generales de la misma, para poder hacer un análisis de la difusión de la información en dicha red, y un análisis estadístico de cómo se comportan las personas respecto a varios temas en concreto, para luego poder construir un tipo de publicación basado en algunas reglas, que permitan al post tener el mayor crecimiento posible en la red acorde a algunos objetivos concretos especificados previamente. 

Este trabajo nos da la posibilidad de poder hacer análisis sobre grupos y comunidades con ciertos intereses en común y sus integrantes interactúan entre ellos. Estos análisis nos pueden dar una base sobre que acciones podemos tomar para tener la mejor repercusión en dichas comunidades, y que satisfaga lo más posible nuestros intereses y objetivos.

## Instrucciones

### Variables de entorno

Crea un fichero `.env` en la raiz del proyecto y añade las siguentes variables de entorno:

```bash
OPENAI_BASE_URL="http://localhost:1234/v1"
OPENAI_API_KEY="no-needed"
CLAUDE_API_KEY="sk-ant-api..."
VOYAGE_API_KEY="pa-..."
```

Las variables de __OPENAI__ son para los _LLM_ que usen la libreria de `openai` para interactuar con ellos, ya sea los propios modelos de __OpenAI__, o modelos de código abierto ejecutados en tu máquina con alguna aplicación que genera un servidor web local que usan la interfas de openai para interactuar con el modelo. Un ejemplo de aplicación es [LMStudio](lmstudio.ai/) donde puedes descargar modelos Open Source de [HuggingFace](huggingface.co/models).

También, si no quieres usar un modelo de OpenAI, puedes usar [Claude](claude.ai/), un LLM de [Anthropic](anthropic.com/). En la variable de entorno `CLAUDE_API_KEY` iría la api_key proporcionada por la misma.

Poro último `VOYAGE_API_KEY` es una api_key de [Voyage AI](www.voyageai.com), una plataforma con varios modelos especializados en hallar la representación en `embeddings` de oraciones.

## Ejecución

Primero hay q instalar las dependencias, esto mediante los comandos:

``` bash
python -m venv snsim # create virtual environment

#activate environment
source snsim/bin/activate #in macOS y Linux
# or in Windows
# snsim\Scripts\activate

#install dependencies
pip install -r requirements.txt
```

Para ejecutar el proyecto primero, desde la raiz del proyecto, debes ejecutar el comando:

```bash
python builder.py
```
Este comando construye la representación en `embeddings` de todos los temas que se usarán para las simulaciones y la matriz de correlación entre dichos temas. No es necesario generar estos datos ya que están incluidos en el proyecto en la carpeta `data`.

Para ejecutar el proyecto entonces se ejecuta el comando:

```bash
streamlit run ./ui.py
```

Este comando levantará una aplicación contruida con __streamlit__ desde donde podrás interactuar con el __LLM__ mediante lenguage naturar, realiazar las simulaciones y automáticamente obtener un análisis de la misma.

## Contribuidores

[![Contribuidores](https://contrib.rocks/image?repo=AlexSanchez-bit/social-network-simulation)](https://github.com/AlexSanchez-bit/social-network-simulation/graphs/contributors)
