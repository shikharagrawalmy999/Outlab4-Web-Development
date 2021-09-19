from django.contrib import admin
from .models import Profile
admin.site.register(Profile)
from .models import Repository
admin.site.register(Repository)
# Register your models here.
