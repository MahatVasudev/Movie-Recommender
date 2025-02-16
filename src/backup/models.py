from django.db import models
from Movies.models import Movies
from django.contrib.auth.models import User
# Create your models here.
class Users(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    bio = models.TextField(default='no bio...')
    avatar = models.ImageField(upload_to='avatars',default='no_avatar.jpg')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def str(self):
        return f"User: {self.username} ({self.uid})"
    
class WatchList(models.Model):
    uid = models.ForeignKey(Users, on_delete=models.CASCADE)
    m_id = models.ForeignKey(Movies, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    
    def str(self):
        return f"{timestamp} ({uid})"