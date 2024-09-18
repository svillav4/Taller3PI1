from django.core.management.base import BaseCommand
from movie.models import Movie
import os
import numpy as np

from openai import OpenAI

from dotenv import load_dotenv, find_dotenv

def get_embedding(text, client, model="text-embedding-3-small"):
   text = text.replace("\n", " ")
   return client.embeddings.create(input = [text], model=model).data[0].embedding

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

class Command(BaseCommand):
    help = 'Modify path of images'

    def handle(self, *args, **kwargs):

        #Se lee del archivo .env la api key de openai
        _ = load_dotenv('../api_keys.env')
        client = OpenAI(
        # This is the default and can be omitted
            api_key=os.environ.get('openai_apikey'),
        )
        
        items = Movie.objects.all()

        req = "película de la segunda guerra mundial"
        emb_req = get_embedding(req, client)

        sim = []
        for i in range(len(items)):
            emb = items[i].emb
            emb = list(np.frombuffer(emb))
            sim.append(cosine_similarity(emb,emb_req))
        sim = np.array(sim)
        print(sim)
        idx = np.argmax(sim)
        idx = int(idx)
        print(items[idx].title)
