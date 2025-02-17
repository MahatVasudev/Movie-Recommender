from django.shortcuts import render, redirect
import pandas as pd
from django.views.generic import ListView, DetailView
from .models import Movies, Movies_description, Genre_Utility
from django.shortcuts import reverse
import datetime
from django.contrib.auth.models import User

##################### utils

from .utils import (
    popular_graph,
    collab_recomms,
    recommend_through_genre,
    similarity,
    most_n_popular,
    most_n_critc_acclaimed,
    create_pages,
    original_N,
    str_to_list,
    recommend_through_genre,
    critically_acclaimed_graph,
    movies_voted_graph,
    recommend_recently_added_movies,
    recommend_language_movies,
)

################################
from pandas.core.common import flatten

from random import sample, shuffle
from django.core.serializers import serialize
from .forms import MoviesSearchForms, Add_or_Remove_WatchList
from django.contrib.auth.decorators import login_required
from Profile.models import WatchList
from django.db.models import Q
import json
from django.http import JsonResponse
import asyncio
from asgiref.sync import sync_to_async
from iso639 import Lang
from pycountry_convert import country_alpha2_to_country_name


# Create your views here.
def index(requests):
    title = None
    # filtered = MoviesSearchForms(requests.POST or None)
    # age_rating = requests.POST.get('genre')
    title = requests.GET["title"]
    multiple_q = Q(
        Q(original_title__icontains=title)
        | Q(title__icontains=title)
        | Q(new_title__icontains=title)
    )
    movies = Movies.objects.filter(multiple_q)

    current_page = requests.GET.get("page") if requests.GET.get("page") != None else 1
    tot_page, get_current = create_pages(movies, n=10, page=int(current_page))
    current_page, tot_page = int(current_page), int(tot_page)

    current_wave = []

    for i, j in enumerate(range(max(current_page - 3, 1), tot_page + 1), 1):
        if i <= 7 or j == tot_page:
            current_wave.append(j)

        elif i == 8:
            current_wave.append("...")
        else:
            continue

    context = {
        "title": title,
        "movies": get_current,
        "movies_length": len(movies),
        "max_pages": tot_page,
        "current_wave": current_wave,
        "current_page": current_page,
        "previous_page": current_page - 1,
        "next_page": current_page + 1,
    }
    return render(requests, "Movies/index.html", context=context)


def show_graphs(request):
    popularity_graph = popular_graph()
    critical_graph = critically_acclaimed_graph()
    most_voted = movies_voted_graph()
    movies_size = f"{Movies.objects.count()}"[:2] + "k+"
    watchlist_size = f"{WatchList.objects.count()}"[:3] + "k+"
    user_size = f"{User.objects.count()}"[:3] + "k+"
    title_list = [
        ("The Top 10 most popular movies in the dataset", popular_graph),
        (
            "The Top 10 most critically acclaimed movie in the data set",
            critically_acclaimed_graph,
        ),
        ("Top 10 most Voted movies", most_voted),
    ]

    context = {
        "movies_size": movies_size,
        "watchlist_size": watchlist_size,
        "user_size": user_size,
        "graphs": title_list,
    }

    return render(request, "Movies\stats.html", context)


def home_view(request):
    data = Movies.objects.all()
    # data_desc = Movies_description.objects.get(po)
    data_desc = Movies_description
    current_page = request.GET.get("page") if request.GET.get("page") != None else 1
    tot_page, get_current = create_pages(data, n=20, page=int(current_page))
    current_page, tot_page = int(current_page), int(tot_page)

    current_wave = []

    for i, j in enumerate(range(max(current_page - 3, 1), tot_page + 1), 1):
        if i <= 5 or j == tot_page:
            current_wave.append(j)

        elif i == 6:
            current_wave.append("...")
        else:
            continue

    context = {
        "object_list": get_current,
        "max_pages": tot_page,
        "current_wave": current_wave,
        "current_page": current_page,
        "previous_page": current_page - 1,
        "next_page": current_page + 1,
        "data_desc": Movies_description,
    }
    return render(request, "Movies\home.html", context)


def detail_view(request, pk):
    print(request.user)
    add_remove = Add_or_Remove_WatchList(request.POST or None)
    print(request.POST)
    if request.POST:
        if add_remove.is_valid():
            if "rate" in request.POST.keys():
                if request.user.is_anonymous:
                    return redirect("login")
                else:
                    WatchList.objects.create(
                        uid=request.user,
                        m_id=Movies(id=pk),
                        rating=float(request.POST["rate"]),
                    )
            elif "remove_rate" in request.POST.keys():
                print(request.POST["remove_rate"])

                if request.POST["remove_rate"] == "on":
                    x = WatchList.objects.get(uid=request.user, m_id=Movies(id=pk))
                    print(x)
                    x.delete()
                    print("Deleted")
    obj = Movies.objects.get(pk=pk)
    date = obj.release_date
    year = obj.year
    imdb_id = obj.imdb_id
    runtime = obj.runtime
    hours_minutes = f"{int(runtime//60)}h {int(runtime%60)}m"
    obj_desc = Movies_description.objects.get(m_id=pk)
    orig_lang = original_N(obj_desc.original_language, model=Lang)
    orig_lang = orig_lang if isinstance(orig_lang, str) else orig_lang.name
    sub_languages = str_to_list(obj_desc.spoken_languages)
    sub_languages = original_N(sub_languages, model=Lang)
    language = []
    for i in sub_languages:
        if isinstance(i, str):
            language.append(i)
        else:
            language.append(i.name)
    production_countries = str_to_list(obj_desc.production_countries)
    production_countries = original_N(
        production_countries, model=country_alpha2_to_country_name
    )
    production_companies = str_to_list(obj_desc.production_companies)
    genres = Genre_Utility.objects.filter(movie_id=Movies(id=pk))
    watchlist = None
    rating = None
    try:
        rating = WatchList.objects.get(uid=request.user, m_id=Movies(id=pk)).rating
        print(rating)
    except:
        watchlist = True

    # in_watchlist =
    context = {
        "object": obj,
        "object_desc": obj_desc,
        "orig_lang": orig_lang,
        "sub_languages": language,
        "production_countries": production_countries,
        "production_companies": production_companies,
        "is_watchlist": watchlist,
        "rating": rating,
        "genres": genres,
        "date": date,
        "runtime": hours_minutes,
        "year": year,
        "imdb_id": imdb_id,
    }
    return render(request, "Movies/details.html", context)


@login_required
def homepage(request):
    collabrecomms = asyncio.to_thread(collab_recomms, request)
    title = None
    byplot = None
    movies = (
        WatchList.objects.filter(uid=request.user).filter(rating__gte=5).order_by("?")
    )
    top_n_pop = most_n_popular()
    top_n_crit = most_n_critc_acclaimed()
    genre = None
    if len(movies) == 0:
        lang = "en"
        language_movies = None
        genre = None
    if len(movies) > 0:
        movies = movies[0]
        title = movies.m_id.title
        byplot = asyncio.to_thread(similarity, movies.m_id, sample_size=100)
    if len(WatchList.objects.filter(uid=request.user)) > 0:
        genre = recommend_through_genre(requests=request)

        lang, language_movies = recommend_language_movies(request=request)
    recent_added_movies = recommend_recently_added_movies(request=request)
    data_list = [
        ("Recommendations for you", asyncio.run(collabrecomms)),
        (
            f'Movies Similar to "{title}"',
            asyncio.run(byplot) if byplot != None else None,
        ),
        ("Top 10 most popular movies", top_n_pop),
        ("Top 10 most critically acclaimed movies", top_n_crit),
        (f"Movies you might like", genre),
        (f"Trending Movies", recent_added_movies),
        (f"More {original_N(lang, model=Lang).name} Movies", language_movies),
    ]
    shuffle(data_list)
    context = {"recommendations": data_list}
    return render(request, "Movies/home_page.html", context=context)


def add_watchlist(request):
    context = {}

    return render(request, "Movies/add_watchlist.html", context)
