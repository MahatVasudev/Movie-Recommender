from django.urls import path
from .views import my_profile_view, watchlist, personal_stats

app_name = 'profiles'

urlpatterns = [
    path('my_profile', my_profile_view, name="profile"),
    path('watchlist', watchlist, name="watchlist"),
    path('personal_stats', personal_stats, name="pers_stats")
]