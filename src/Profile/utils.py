from django.shortcuts import render
from .models import Profile, WatchList
from .forms import ProfileForm
from django.contrib.auth.decorators import login_required
from Movies.models import Movies, Genre_Utility, Movies_description
from pandas.core.common import flatten
from Movies.utils import listify, generate_graph_bar, WIDTH, HEIGHT
from pycountry_convert import country_alpha2_to_country_name
from iso639 import Lang
import plotly.graph_objects as go
import plotly.express as px 
import pandas as pd 
from plotly.io import to_html

def generate_graph_pie(df,x, y):
    trace = px.pie(df,names=x,values=y,hole = 0.5,width=WIDTH, height = HEIGHT)
    trace.update_layout(paper_bgcolor="rgb(0, 31, 63)", plot_bgcolor="rgb(0, 31, 63)", font_color= "white", )
    Fig = go.Figure(data=trace)
    Fig.update_traces(textposition='inside', textinfo='percent+label')
    return to_html(Fig,include_plotlyjs=True)

def generate_graph_line(df, x, y):
    trace = px.line(df, x = x, y = y, height = HEIGHT, width= WIDTH)
    trace.update_layout(paper_bgcolor="rgb(0, 31, 63)", plot_bgcolor="rgb(0, 31, 63)", font_color= "white", )    
    Fig = go.Figure(data=trace)
    
    return to_html(Fig, include_plotlyjs=True)
    
    
    
def data_favorite_movies(user):
    movies = WatchList.objects.filter(uid=user).order_by("-rating")
    movies_name = movies.values_list("m_id_id")[:10]
    
    movies_rating = movies.values_list("rating")[:10]
    x, y = listify(movies_name, movies_rating)
    x = [Movies.objects.get(id = i).new_title for i in x]
    
    return generate_graph_bar(x, y)

def data_most_viewed_genre(user):
    movies = WatchList.objects.filter(uid=user)
    movie = movies.values_list("m_id_id")
    data = {"genre":[]}
    for i in list(flatten(movie)):
        genre = Genre_Utility.objects.filter(movie_id_id= i)
        genre = [i.genre for i in flatten(genre)]
        data['genre'].extend(genre)
    
    data = pd.DataFrame(data)    
    
    genres = data.value_counts("genre").reset_index()
    
    return generate_graph_pie(genres,"genre","count")
    
def data_added_watchlist_timeseries(user):
    movies = WatchList.objects.filter(uid=user)
    timestamp = movies.values_list("timestamp")
    data = pd.DataFrame({"date": list(flatten(timestamp))})
    data["date"] = pd.to_datetime(data["date"])
    data["date"] = data["date"].dt.date
    data = data.value_counts("date").reset_index()
    data = data.sort_values("date",ascending=True)
    return generate_graph_line(data, "date","count")
    
def data_most_viewed_languages(user):
    movies = WatchList.objects.filter(uid=user)
    movie = movies.values_list("m_id_id")
    # print([Movies_description.objects.get(m_id_id= i).original_language if i!= "cn" else "cn" for i in flatten(movie)])
    
    lang = []
    for i in flatten(movie):
        z =  Movies_description.objects.get(m_id_id = i).original_language
        if z == "cn":
            lang.append("Chinese")
        else:
            lang.append(Lang(z).name)
            
    data = pd.DataFrame({"lang":lang})
    data = data.value_counts("lang").reset_index()
    data = data.sort_values("count",ascending=True)
    return generate_graph_pie(data, "lang", "count") 

def data_most_viewed_age_rating(user):
    movies = WatchList.objects.filter(uid = user)
    movie = movies.values_list("m_id_id")
    print(movie)
    age_rating = [Movies.objects.get(id = i).age_rating for i in flatten(list(movie))]
    print(age_rating)
    data = pd.DataFrame({"age_rating": age_rating})
    data = data.value_counts("age_rating").reset_index()
    
    return generate_graph_pie(data, "age_rating","count")
    
    
    