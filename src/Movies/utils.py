from .models import Movies, Movies_description
import pandas as pd 
from pandas.core.common import flatten
from plotly.io import to_html
import plotly.graph_objects as go
import plotly.express as px 
import joblib
from Profile.models import WatchList 
import heapq
from collections import defaultdict
from operator import itemgetter
import spacy
from random import shuffle, choice
import os

def create_color(set1):
    ...
    
HEIGHT = 600
WIDTH = 1000


def listify(x, y):
    x, y = list(flatten(x)), list(flatten(y))
    return x,y

def generate_graph_bar(x, y):
    
    trace = px.bar(y = x,
                   x = y,text=x,height=HEIGHT,width=WIDTH,color_continuous_scale=px.colors.sequential.Plasma, orientation="h")
    trace.update_layout(paper_bgcolor="rgb(0, 31, 63)", plot_bgcolor="rgb(0, 31, 63)", font_color= "white", )
    Fig = go.Figure(data=trace)
    Fig.update_yaxes(showticklabels=False)
    Fig.update_traces(textposition='inside',marker_color="white")
    htt = to_html(Fig,include_plotlyjs=True)
    
    return htt


def popular_graph():
    movies = Movies.objects.all()
    top_n_popular = movies.order_by("-popularity")
    x = top_n_popular.values_list('new_title')[:10]
    y = top_n_popular.values_list('popularity')[:10]
    x, y = listify(x,y)
    # trace = go.Bar(x=x,
    #                y=y,hoverinfo='x+y',
    #                text=y,textposition='outside')    
    return generate_graph_bar(x, y)

def critically_acclaimed_graph():
    movies = Movies.objects.all()
    top_n_critt = movies.order_by("-critical_score")
    x = top_n_critt.values_list('new_title')[:10]
    y = top_n_critt.values_list('critical_score')[:10]
    x, y = listify(x,y)
    
    return generate_graph_bar(x, y) 

def movies_voted_graph():
    movies = Movies.objects.all()
    top_n_voted = movies.order_by("-vote_count")
    x = top_n_voted.values_list('new_title')[:10]
    y = top_n_voted.values_list('vote_count')[:10]
    x, y = listify(x,y)
    
    return generate_graph_bar(x,y)    

def create_pages(data, n=25, page=1):
    
    num_pages = max(round(len(data)/n),1)
    def show_pages(page=1):
        previous_page = (page-1)*n
        current_page = page*n 
        return data[previous_page:current_page]
    
    return num_pages, show_pages(page)

def str_to_list(string:str):
    text = str(string)
    text = text.replace("[","").replace("]","").strip()
    text = [str(i).replace("'",'').strip() for i in text.split(',')]
    return text

illegal_words = ["xx", "''", '"', "'", '','XG']

def original_N(lang, model):
    if lang == "" or lang == '' or lang == "'" or lang == '"' or lang == "''" or lang == "xx":
        return ""
    
    elif isinstance(lang, list):
        result = []
        for i in lang:
            if i in illegal_words:
                continue
            else:
                if i == "cn":
                    result.append("Chinese")
                else:
                    result.append(model(i))
                
    else:
        if lang == "cn":
            result = "Chinese"
        else:
            result = model(lang) 
            
    return result
    
def sublanguages(langs: str):
    subs = str_to_list(langs)
    subs:list = [original_language(i) for i in subs]
    return subs 



Knn_model = joblib.load(os.getcwd() + r"/ML models/knn_sim.joblib")

def collab_recomms(request, n = 20, sample_size=20000, seed=None):
    candidates = defaultdict(float)
    data = WatchList.objects.exclude(uid=request.user).order_by("?")[:sample_size]
    k_neighbours = heapq.nlargest(n, data.values("m_id","rating"), key= lambda t:t["rating"])
    for item_dict in k_neighbours:
        try:
            similarities = Knn_model[item_dict['m_id']]
            for innerId, score in enumerate(similarities):
                candidates[innerId] += score * (item_dict['rating']/5)
        except:
            continue
    recommendations = []
    for itemId, rating_sum in sorted(candidates.items(), key=itemgetter(1),reverse=True):
 
        try:
            recommendations.append(Movies.objects.get(id=itemId))
            if len(recommendations) >=10:
                break
        except:
            continue 

    return recommendations

nlp = spacy.load("en_core_web_lg")

def similarity(m_id, sample_size = 10000, n = 10, seed=None):
    overview = Movies_description.objects.get(m_id=m_id).overview
    doc1 = nlp(overview)
    # w1 = set(ss for word in overview1 for ss in wordnet.synsets(word))
    samples = Movies_description.objects.exclude(m_id=m_id).order_by("?")[:sample_size]
    listin = []
    for i in samples:
        doc2 = nlp(i.overview)
        # w2 = set(ss for word in overview12 for ss in wordnet.synsets(word))
        sim = doc1.similarity(doc2)
        # sim = (wordnet.wup_similarity(s1,s2) for s1,s2, in product(w1,w2))
        listin.append([i.m_id, sim])
        
    listin = sorted(listin, key=itemgetter(1),reverse=True)
    listin = listin[:n]
    listin = [i[0] for i in listin]
    return listin
    
    
def most_n_critc_acclaimed(n = 10):
    movie = Movies.objects.order_by("-critical_score")[:10]

    return movie 

def most_n_popular(n = 10):
    movie = Movies.objects.order_by("-popularity")[:10]
    return movie 

genre_data = pd.read_csv(os.getcwd() + r"/extra data/genre_utility_matrix_with_movies.csv")

def recommend_through_genre(requests, sample_size = 20000,n=20):
    userdata = pd.DataFrame(WatchList.objects.filter(uid=requests.user).values())
    # print(userdata)
    dx = genre_data.loc[genre_data['id'].isin(userdata['m_id_id']),genre_data.columns != 'id'].T 
    dx = pd.DataFrame( dx * userdata['rating'].values).T 
    transformed_dx = pd.melt(dx, var_name="genre").groupby('genre')['value'].sum()
    # scaled = (transformed_dx - transformed_dx.mean())/ transformed_dx.std()
    # scaled = (transformed_dx)/ transformed_dx.sum()
    scaled = (transformed_dx - transformed_dx.min())/ (transformed_dx.max() - transformed_dx.min())
    norm_add_data = pd.DataFrame(scaled)
    norm_add_data = norm_add_data.reindex(['Music', 'Animation', 'Western', 'Adventure', 'Horror', 'Drama',
       'Mystery', 'Foreign', 'Documentary', 'Comedy', 'War', 'Science Fiction',
       'Romance', 'Thriller', 'History', 'TV Movie', 'Fantasy', 'Family',
       'Crime', 'Action'])  
    other_data = genre_data[~genre_data['id'].isin(userdata['m_id_id'])]
    # print(other_data)       
    other_data.loc[:, other_data.columns != 'id'] = pd.DataFrame(other_data.loc[:, other_data.columns != 'id'] * norm_add_data.values.T)
    # print(other_data.columns)
    other_data = other_data.sample(n =sample_size)
    other_data['score'] = other_data.drop("id", axis=1).sum(axis=1)
    # print(other_data)
    prediction = other_data.sort_values('score', ascending=False).head(n)
    prediction = [Movies.objects.get(id=int(i)) for i in prediction['id'].to_list()]
    
    return prediction

def recommend_recently_added_movies(request, n=10, sample=100):
    movies = WatchList.objects.all().order_by("-timestamp")[:sample].values("m_id_id",'timestamp')
    movie = pd.DataFrame(movies)
    print(movie.columns)
    movie_count = movie.value_counts("m_id_id").reset_index().sort_values("count",ascending=False).head(n)
    movies = [Movies.objects.get(id=i) for i in movie_count["m_id_id"].to_list()]
    
    return movies    
          
          
def recommend_language_movies(request, n=10):
    movies = WatchList.objects.filter(uid=request.user).values_list("m_id_id")
    languages = {Movies_description.objects.get(m_id=i).original_language for i in movies}
    language = choice(list(languages))
    excluded = Movies_description.objects.filter(original_language=language).exclude(m_id__in = movies).values_list("m_id_id")
    included = Movies.objects.filter(id__in=excluded).order_by("-critical_score")[:n]
    
    return language, included
    
    
    
        
    
def in_request(request, val):
    if val in request:
        return True 
    else:
        return False
    
