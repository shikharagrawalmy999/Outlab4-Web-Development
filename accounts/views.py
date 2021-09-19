from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.shortcuts import redirect
from accounts import formsnew
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from accounts import models

class SignUpView(generic.CreateView):
    form_class = formsnew.CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

def GetProfile(user_name):
    current_usermodel = User.objects.get(username=user_name)
    current_profile = models.Profile.objects.get(Userinfo=current_usermodel)
    return current_profile

def ProfileView(request):
    list_of_details = []
    p = GetProfile(request.user.username)
    list_of_details.append(request.user.username)
    list_of_details.append(p.number_followers)
    list_of_details.append(p.last_updated)
    list_of_repos = list(models.Repository.objects.filter(owner=request.user.profile))
    list_of_details.append(list_of_repos)
    list_of_details.append(request.user.first_name)
    list_of_details.append(request.user.last_name)
    template = loader.get_template('profile.html')
    context = {
        'list_of_details': list_of_details,
    }
    return HttpResponse(template.render(context, request))

def UpdateNow(request):
    current_userprofile=GetProfile(request.user.username)
    list_of_userinfo=formsnew.fetchuser(request.user.username)
    list_of_repo, list_of_stars=formsnew.fetchrepo(request.user.username)
    current_userprofile.number_followers=list_of_userinfo[2]
    current_userprofile.last_updated=list_of_userinfo[3]
    current_userprofile.save()
    number_of_repo_deleted=models.Repository.objects.filter(owner=current_userprofile).delete()
    for i in range(len(list_of_repo)):
        repo=models.Repository(name=list_of_repo[i], stars=list_of_stars[i], owner=request.user.profile)
        repo.save()
    response = redirect('../myprofile/')
    return response

def Explore(request):
    allprofiles=list(models.Profile.objects.all())
    template = loader.get_template('explore.html')
    context = {
        'allprofiles': allprofiles,
    }
    print(allprofiles)
    return HttpResponse(template.render(context, request))    

def ExploreView(request, user_name):

    list_of_details = []
    p = GetProfile(user_name)
    list_of_details.append(user_name)
    list_of_details.append(p.number_followers)
    list_of_details.append(p.last_updated)
    list_of_repos = list(models.Repository.objects.filter(owner=p))
    list_of_details.append(list_of_repos)
    list_of_details.append(p.Userinfo.first_name)
    list_of_details.append(p.Userinfo.last_name)
    template = loader.get_template('profile.html')
    context = {
        'list_of_details': list_of_details,
    }
    print(list_of_details)
    return HttpResponse(template.render(context, request))