from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Piscina(models.Model):
    n_piscina = models.IntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __int__(self):
        return self.n_piscina

class Value(models.Model):
    temperature = models.FloatField()
    ph = models.FloatField()
    date = models.DateTimeField(default=timezone.now)
    piscina = models.ForeignKey(Piscina, on_delete=models.CASCADE)
    
    def __int__(self):
        return self.temperature

