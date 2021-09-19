from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    number_followers=models.CharField(max_length=100)
    last_updated=models.DateTimeField()
    Userinfo = models.OneToOneField(User, on_delete=models.CASCADE)
    list_repos = []

    def __str__(self):
        return self.Userinfo.username

class Repository(models.Model):
    name = models.CharField(max_length=100)
    stars= models.CharField(max_length=100)
    owner = models.ForeignKey(Profile,on_delete=models.CASCADE)

    def __str__(self):
        return self.name