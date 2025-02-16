from django import forms
from .models import GENRE_CHOICES


AGE_CHOICES = [
    ('R', 'R rated'),

]
class MoviesSearchForms(forms.Form):
    age_rating = forms.ChoiceField(choices=AGE_CHOICES)
    
class Add_or_Remove_WatchList(forms.Form):
    add_or_remove = forms.BooleanField(required=False)
    