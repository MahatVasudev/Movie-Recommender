from django.urls import path 
import asyncio
from .views import (
    home_view,
    detail_view,
    show_graphs,
    index,
    homepage,
    add_watchlist,
)

app_name = 'movies'

urlpatterns = [
    path('',homepage,name="home"),
    path('stats',show_graphs,name='graph'),
    path('movies',home_view, name='movies'),
    path('movies/<pk>',detail_view, name='detail'),
    path('search',index, name='search-movies'),
    path('description', add_watchlist, name="description"),
]
