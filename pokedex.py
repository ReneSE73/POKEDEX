# Este código obtiene información de un Pokémon desde la API de PokeAPI y muestra sus detalles, incluyendo una imagen, peso, tamaño, movimientos, habilidades y tipos.
# Requiere las librerías requests, pandas, matplotlib y PIL para funcionar correctamente.
# Asegúrate de tenerlas instaladas en tu entorno de Python.
# Puedes instalar las librerías necesarias con: pip install requests pandas matplotlib pillow

import requests # Importa la librería requests para realizar solicitudes HTTP
import json # Importa la librería json para manejar datos en formato JSON
import pandas as pd # Importa pandas para manejar datos en forma de DataFrame
import matplotlib.pyplot as plt # Importa matplotlib para crear gráficos y visualizaciones
from matplotlib.offsetbox import OffsetImage, AnnotationBbox # Importa OffsetImage y AnnotationBbox para manejar imágenes en los gráficos
import matplotlib.patches as patches # Importa patches para crear formas en los gráficos
from PIL import Image # Importa Image de PIL para manejar imágenes
from io import BytesIO # Importa BytesIO para manejar datos binarios en memoria



def obten_pokemon(pokemon):
    """
    Obtiene información de un Pokémon desde la API de PokeAPI asignando el nombre o clave de un pokemon muestra sus detalles.
    
    """
    url = "https://pokeapi.co/api/v2/pokemon/" + pokemon
    respuesta = requests.get(url)
    
    if respuesta.status_code != 200:
        print("Ha ocurrido un error. Intenta nuevamente")
        print(f"Error: {respuesta.status_code}")
        return None

    datos = respuesta.json()

    mostrar_informacion(datos)

def mostrar_informacion(datos):
    """Muestra la información del Pokémon obtenido, incluyendo su imagen, peso, tamaño, movimientos, habilidades y tipos."""
    try:
        url_imagen = datos['sprites']['other']['official-artwork']['front_default'] # obtiene la URL de la imagen del Pokémon
        if not url_imagen:
            url_imagen = datos['sprites']['front_default'] # obtiene la URL de la imagen del Pokémon si no hay otra disponible
        
        respuesta_imagen = requests.get(url_imagen)
        imagen = Image.open(BytesIO(respuesta_imagen.content))
        
        peso = datos['weight'] # obtiene el peso del Pokémon
        tamano = datos['height']  # obtiene el tamaño del Pokémon
        movimientos = [movimiento['move']['name'] for movimiento in datos['moves'][:15]]    # obtiene los primeros 15 movimientos del Pokémon 
        habilidades = [habilidad['ability']['name'] for habilidad in datos['abilities']] # obtiene las habilidades del Pokémon
        tipos = [tipo['type']['name'] for tipo in datos['types']] # obtiene los tipos del Pokémon

    except Exception as e:
         print(f"No se pudo obtener la imagen del Pokémon. Error: {e}")    # Manejo de excepciones para errores al obtener la imagen
         return None

    pokemonlist = [datos['name'].capitalize(), url_imagen ,peso, tamano, movimientos, habilidades, tipos] # crea una lista con la información del Pokémon

    s = pd.Series(pokemonlist, index=['Nombre', 'URLImagen', 'Peso', 'Tamaño', 'Movimientos', 'Habilidades', 'Tipos']) # crea una Serie de pandas con la información del Pokémon

    df= pd.DataFrame([s]).to_json('pokedex/pokemon.json', index=False)# guarda la información del Pokémon en un archivo JSON

    fg, ax = plt.subplots(figsize=(7, 5)) # crea una figura y un eje para el gráfico
    imagenbox = OffsetImage(imagen, zoom=0.3) # crea un objeto OffsetImage con la imagen del Pokémon
    ab = AnnotationBbox(imagenbox, (0.2, 0.5), frameon=False) # crea un objeto AnnotationBbox para colocar la imagen en el gráfico
    ax.add_artist(ab) # añade la imagen al eje del gráfico

    # Dibuja un rectángulo alrededor de la imagen
    ax.text(0.6, 0.1, f"Nombre: {datos['name'].capitalize()}\n"
                     f"Peso: {datos['weight']/10:.1f} kg\n"
                     f"Tamaño: {datos['height']/10:.1f} m\n"
                     f"Movimientos: {'\n '.join(movimientos)}\n"
                     f"Habilidades: {', '.join(habilidades)}\n"
                     f"Tipos: {', '.join(tipos)}",
    )
    # Desactivsa los ejes y muestra el título
    ax.axis('off')
    plt.title(f"Información de {datos['name'].capitalize()}", fontsize=20, fontweight='bold') # establece el título del gráfico

    #muestra el gráfico
    plt.show()

# Verifica si el script se está ejecutando directamente

if __name__ == "__main__":
    while True: # Bucle para solicitar al usuario que ingrese el nombre del Pokémon
        
        pokemon = input("Ingresa el nombre del Pokémon: ") # Solicita al usuario que ingrese el nombre del Pokémon
        pokemon = pokemon.lower().strip() # Convierte el nombre del Pokémon a minúsculas y elimina espacios en blanco al inicio y al final
        if not pokemon:
            print("No se ha ingresado un Pokémon. Intenta nuevamente.")
        elif not pokemon.isalpha():
            print("El nombre del Pokémon debe contener solo letras. Intenta nuevamente.")
            exit()

        obten_pokemon(pokemon)
        continuar = input("¿Deseas buscar otro Pokémon? (s/n): ").lower().strip()
        if continuar != 's':
            print("Gracias por usar el programa. ¡Hasta luego!")
            break
    # Fin del bucle
   