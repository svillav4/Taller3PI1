from django.urls import path
from .views import recommendations_view, search_recommendations

app_name = 'recommendation'

urlpatterns = [
    path('', recommendations_view, name='recommendations'),
    path('search/', search_recommendations, name='search_recommendations')
]
