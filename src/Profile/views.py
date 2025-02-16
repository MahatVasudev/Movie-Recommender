from django.shortcuts import render
from .models import Profile, WatchList
from Movies.models import Genre_Utility
from .forms import ProfileForm
from django.contrib.auth.decorators import login_required
from Movies.models import Movies
from pandas.core.common import flatten
import datetime as dt
from .utils import (
    data_favorite_movies, 
    data_most_viewed_genre,
    data_added_watchlist_timeseries,
    data_most_viewed_languages,
    data_most_viewed_age_rating
)

# Create your views here.

@login_required
def my_profile_view(request):
    profile = Profile.objects.get(user=request.user)
    form = ProfileForm(request.POST or None, request.FILES or None, instance=profile)
    confirm = False 
    
    if form.is_valid():
        form.save()
        confirm = True 
        
    context = {
        'user':profile,
        'form':form,
        'confirm':confirm
    }
    return render(request, 'Profile/main.html', context)

@login_required
def watchlist(request):
    my_watch = WatchList.objects.filter(uid=request.user)
    context = {
        'watchlist': my_watch
    }
    return render(request, "Profile\WatchList.html", context=context)

@login_required
def personal_stats(request):
    data = WatchList.objects.filter(uid=request.user)
    personal_data = data.values_list("m_id_id")
    data_count = data.count()
    last_added = data.order_by("-timestamp")[0].timestamp
    added_today = data.filter(timestamp__date=dt.datetime.today()).count()
    error_message = None
    print(list(personal_data) == [])
    if list(personal_data) == []:
        title_list = None
        error_message = "Add Movies to your WatchList to view your personal graphs"
    else:
        personal_data = list(flatten(list(personal_data)))
        print(personal_data)
        a = data_favorite_movies(request.user)
        b = data_most_viewed_genre(request.user)
        c= data_added_watchlist_timeseries(request.user)
        d = data_most_viewed_languages(request.user)
        e = data_most_viewed_age_rating(request.user)
        title_list = [
            ("Your top 10 most favorite movies",a),
            ("Your top watched genres",b),
            ("Frequency of adding movies to watchlist", c),
            ("Most viewed languages",d),
            ("Most viewed age rating",e)]
    context = {
        "err": error_message,
        "data": title_list,
        "data_count": data_count,
        "last_added":last_added,
        "added_today":added_today
    }
    
    return render(request, "Profile/personal_stats.html", context)