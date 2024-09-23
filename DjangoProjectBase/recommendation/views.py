import json
import os
import numpy as np
from dotenv import load_dotenv
from openai import OpenAI
from django.shortcuts import render


load_dotenv('api_keys.env')

# Inicializa el cliente de OpenAI con la clave de API
client = OpenAI(
    api_key=os.environ.get('openai_apikey'),
)

json_file_path = os.path.join(os.path.dirname(__file__), 'data', 'movie_descriptions_embeddings.json')

# Cargar las descripciones de películas y sus embeddings
with open(json_file_path, 'r') as file:
    file_content = file.read()
    movies = json.loads(file_content)

# Función para obtener embeddings de un texto
def get_embedding(text, model="text-embedding-3-small"):
    text = text.replace("\n", " ")
    return client.embeddings.create(input=[text], model=model).data[0].embedding

# Función para calcular la similitud coseno entre dos vectores
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Enlace con el html
def recommendations_view(request):
    return render(request, 'recommendations.html')

# Vista de las recomendaciones hechas
def search_recommendations(request):
    query = request.GET.get('query')
    recommended_movie = None
    movie_image = None
    movie_description = None
    
    if query:
        # Obtener el embedding del query
        emb = get_embedding(query)

        # Calcular la similitud con cada película en la base de datos
        sim = []
        for movie in movies:
            sim.append(cosine_similarity(emb, movie['embedding']))
        
        # Encontrar el índice de la película con mayor similitud
        sim = np.array(sim)
        idx = np.argmax(sim)

        # Obtener el título de la película recomendada
        recommended_movie = movies[idx]['title']
        movie_description = movies[idx]['description']
        # para poder obtener la direccion de la imagen habia que poner el titulo de la pelicula con un m_ al comienzo
        movie_image_filename = f"{recommended_movie}"
        movie_image = f"/media/movie/images/m_{movie_image_filename}.png"
        
    # Renderizar los resultados en el template
    return render(request, 'search_results.html', {
        'query': query,
        'recommended_movie': recommended_movie,
        'movie_image': movie_image,
        'movie_description': movie_description,
    })
