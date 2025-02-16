from django.contrib import admin
from .models import (
    Movies,
    Genre_Utility,
    Movies_description
)
# Register your models here.

admin.site.register(Movies)
admin.site.register(Genre_Utility)
admin.site.register(Movies_description)
