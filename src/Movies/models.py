from django.db import models
from django.shortcuts import reverse
# Create your models here.
class Movies(models.Model):
    id = models.IntegerField(primary_key=True)
    original_title = models.CharField(max_length=200, default=None)
    title = models.CharField(max_length=200, default=None)
    new_title = models.CharField(max_length=200,default=None)
    imdb_id = models.TextField(blank=True,default=None)
    budget = models.BigIntegerField(default=0)
    revenue = models.BigIntegerField(default=0)
    year = models.IntegerField(default=0)
    runtime = models.FloatField(default=0,null=True)
    release_date = models.DateField(default=0)
    age_rating = models.CharField(max_length=10,default='Not Rated')
    vote_average = models.FloatField(default=0)
    vote_count = models.BigIntegerField(default=0)
    popularity = models.BigIntegerField(default=0)
    critical_score = models.BigIntegerField(default=0)     

    def __str__(self):
        return str(f"Movie: {self.new_title}")
    

    def get_absolute_url(self):
        return reverse("movies:detail", kwargs={"pk": self.pk})
    
    def get_poster(self):
        return Movies_description.objects.get(m_id=self.id).poster_link
    
class Movies_description(models.Model):
    m_id = models.OneToOneField(Movies, on_delete=models.CASCADE)
    overview = models.TextField(max_length=1000,blank=True, default=None)
    overview_cleaned = models.TextField(max_length=1000,blank=True,default=None) 
    original_language = models.TextField(max_length=1000,default=None)
    spoken_languages = models.TextField(max_length=1000,default=None)
    tagline = models.TextField(max_length=1000,default=None)
    production_companies = models.TextField(default="[]")
    production_countries = models.TextField(default="[]")
    poster_link = models.TextField(max_length=5000,default=None)

    def __str__(self):
        return f"{self.id} description"
    
    def get_posters(self):
        return self.poster_link
    
    
    
GENRE_CHOICES = (('Music','Music'), ('Animation','Animation'), ('Western','Western'), 
                 ('Adventure','Adventure'), ('Horror','Horror'), ('Drama','Drama'),
       ('Mystery','Mystery'), ('Foreign','Foreign'), ('Documentary','Documentary'), 
       ('Comedy','Comedy'), ('War','War'), ('Science Fiction','Science Fiction'),
       ('Romance','Romance'), ('Thriller','Thriller'), ('History','History'), 
       ('TV Movie','TV Movie'), ('Fantasy','Fantasy'), ('Family','Family'),
       ('Crime','Crime'), ('Action','Action'))

class Genre_Utility(models.Model):
    movie_id = models.ForeignKey(Movies,on_delete=models.CASCADE)
    genre = models.TextField(choices=GENRE_CHOICES,default=None)
