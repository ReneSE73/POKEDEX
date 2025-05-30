#importacion de librerias

import requests  # Para hacer solicitudes HTTP
import pandas as pd # Para manejar datos en forma de DataFrame
import matplotlib.pyplot as plt # Para crear gráficos y visualizaciones
from matplotlib.offsetbox import OffsetImage, AnnotationBbox # Para manejar imágenes en los gráficos
import matplotlib.patches as patches # Para manejar parches en los gráficos
from PIL import Image # Para manejar imágenes
from io import BytesIO # Para manejar datos en memoria como si fueran archivos



# Solicitud al usuario para ingresar el nombre del Pokémon
pokemon = input("Ingresa el nombre del Pokémon: ").lower()
url = "https://pokeapi.co/api/v2/pokemon/" + pokemon


# Realizar la solicitud a la API de Pokémon y verificar el estado de la respuesta
respuesta = requests.get(url)
if respuesta.status_code != 200:
    print("Ha ocurrido un error. Intenta nuevamente")
    print(f"Error: {respuesta.status_code}")
    exit()

# Procesar la respuesta JSON para extraer información del Pokémon
datos = respuesta.json()

# Verificar si el Pokémon existe
try:
    url_imagen = datos['sprites']['other']['official-artwork']['front_default']

    # Verificar si la URL de la imagen es válida
    if not url_imagen:
        url_imagen = datos['sprites']['front_default']
    
    respuesta_imagen = requests.get(url_imagen)
    
    # Obtener la imagen del Pokémon y Caracteriticas
    imagen = Image.open(BytesIO(respuesta_imagen.content))
    peso = datos['weight']
    tamano = datos['height']
    movimientos = [movimiento['move']['name'] for movimiento in datos['moves'][:10]] 
    habilidades = [habilidad['ability']['name'] for habilidad in datos['abilities']]
    tipos = [tipo['type']['name'] for tipo in datos['types']]

# Manejo de excepciones para errores al obtener la imagen
except:
     print("No se pudo obtener la imagen del Pokémon.")    
     exit()

# Crear una lista con la información del Pokémon
pokemonlist = [datos['name'].capitalize(), url_imagen ,peso, tamano, movimientos, habilidades, tipos]

# Crear un objeto Series de pandas con la información del Pokémon
s = pd.Series(pokemonlist, index=['Nombre', 'URLImagen', 'Peso', 'Tamaño', 'Movimientos', 'Habilidades', 'Tipos'])

# Guardar la información del Pokémon en un archivo JSON
df= pd.DataFrame([s]).to_json('pokedex/pokemon.json', index=False)

# Dibujar la imagen del Pokémon y mostrar la información en un gráfico
fg, ax = plt.subplots(figsize=(7, 5))
imagenbox = OffsetImage(imagen, zoom=0.5)
ab = AnnotationBbox(imagenbox, (0.3, 0.7), frameon=False)
ax.add_artist(ab)

# Agrega información del Pokémon al gráfico
ax.text(0.6, 0.7, f"Nombre: {datos['name'].capitalize()}\n"
                 f"Peso: {datos['weight']/10:.1f} kg\n"
                 f"Tamaño: {datos['height']/10:.1f} m\n"
                 f"Movimientos: {', '.join(movimientos)}\n"
                 f"Habilidades: {', '.join(habilidades)}\n"
                 f"Tipos: {', '.join(tipos)}",
)
# Desactivar los ejes del gráfico
ax.axis('off')
# Añadir un título al gráfico
plt.title(f"Información de {datos['name'].capitalize()}", fontsize=16)
plt.show()



