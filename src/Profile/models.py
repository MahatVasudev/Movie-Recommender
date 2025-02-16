from django.db import models
from Movies.models import Movies
from django.contrib.auth.models import User
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    bio = models.TextField(default='no bio...')
    avatar = models.ImageField(upload_to='avatars',default='no_avatar.jpg')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def str(self):
        return f"User: {self.user.username}"
    
class WatchList(models.Model):
    uid = models.ForeignKey(User, on_delete=models.CASCADE)
    m_id = models.ForeignKey(Movies, on_delete=models.CASCADE,default=0)
    rating = models.FloatField(default=5, max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def str(self):
        return f"{timestamp} ({uid})"
    
    def check_exists(self,user,movies):
        try:
            self.objects.get(uid=user, m_id=movies)
            return True
        except:
            return False