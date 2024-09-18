from django.core.management.base import BaseCommand
from movie.models import Movie
import json
import os
import numpy as np

class Command(BaseCommand):
    help = 'Modify path of images'

    def handle(self, *args, **kwargs):
  
        items = Movie.objects.all()
        item = items[10]
        print(item.emb)
        
        
