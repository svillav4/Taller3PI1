from django.core.management.base import BaseCommand
from movie.models import Movie
import json
import os
import numpy as np

class Command(BaseCommand):
    help = 'Load movies from movie_descriptions.json into the Movie model'

    def handle(self, *args, **kwargs):
        # Construct the full path to the JSON file
        #Recuerde que la consola está ubicada en la carpeta DjangoProjectBase.
        #El path del archivo movie_descriptions con respecto a DjangoProjectBase sería la carpeta anterior
        json_file_path = '../movie_descriptions.json' 
        
        # Load data from the JSON file
        with open(json_file_path, 'r') as file:
            movies = json.load(file)
        
        # Add products to the database
        cont = 0
        for movie in movies:
            movie_to_update = Movie.objects.filter(title = movie['title']).first() #Se asegura que la película no exista en la base de datos
            if not movie_to_update:
                print(f"{movie['title']} is not in the database")   
            else:           
                movie_to_update.description = movie["description"]
                movie_to_update.save()
                cont+=1
                    
        
        self.stdout.write(self.style.SUCCESS(f'Successfully added {cont} descriptions to the database'))