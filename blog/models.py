from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
    title = models.TextField()
    content = models.TextField()
    date_post = models.DateTimeField(default=timezone.now)    #auto_now_add=True
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title
        
        
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
        

class Value(models.Model):
    temperature = models.IntegerField()
    ph = models.IntegerField()
    date = models.DateTimeField(default=timezone.now)
    
    def __int__(self):
        return self.temperature