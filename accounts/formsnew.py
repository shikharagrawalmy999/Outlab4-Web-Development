import requests
from requests.exceptions import HTTPError
def fetchuser(username):
    try:
        response=requests.get('https://api.github.com/users/'+username)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        return -1
    except Exception as err:
        print(f'Other error occurred: {err}')
        return -1
    else:
        print('Hello nice')
        dict=response.json()
        list1=[]
        list1.append(username)
        list1.append(dict['name'])
        list1.append(dict['followers'])
        list1.append(str(datetime.datetime.now()))
        return list1

def fetchrepo(username):
    str='https://api.github.com/users/'
    str=str+username
    str=str+'/repos'
    try:
        response=requests.get(str)
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        return -1 
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
        return -1
    else:
        repolist=response.json()
        name=[]
        followers=[]
        for repo in repolist:
            name.append(repo['name'])
            followers.append(repo['stargazers_count'])
        dict_of_name_and_followers={name[i]: followers[i] for i in range(len(name))}
        sorted_dict=dict(sorted(dict_of_name_and_followers.items(), key=lambda item: item[1], reverse=True))
        return list(sorted_dict.keys()),list(sorted_dict.values())
    
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from django import forms
from accounts import models
import datetime

class CustomUserCreationForm(UserCreationForm):
    username=forms.CharField(label=False,widget=forms.TextInput(attrs={'class': 'form-control','style':'width:40%;border-radius:15px','placeholder':'Username'}))
    first_name = forms.CharField(label =False,widget=forms.TextInput(attrs={'class': 'form-control','style':'width:40%;border-radius:15px','placeholder':'First Name'}))
    last_name = forms.CharField(label = False,widget=forms.TextInput(attrs={'class': 'form-control','style':'width:40%;border-radius:15px','placeholder':'Last Name'}),required=False)
    password1= forms.CharField(label=False,widget=(forms.PasswordInput(attrs={'class': 'form-control','style':'width:40%;border-radius:15px','placeholder':'Password'})),help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(label=False, widget=forms.PasswordInput(attrs={'class': 'form-control','style':'width:40%;border-radius:15px','placeholder':'Confirm Password'}))
    class Meta:
        model = User
        fields = ("username","password1",'password2',"first_name", "last_name",)
    
    def clean(self):
        '''
        Verify both passwords match.
        '''

        cleaned_data = super().clean()
        password = cleaned_data.get("password1")
        password_2 = cleaned_data.get("password2")
        if password is not None and password != password_2:
            self.add_error("password2", "Your passwords must match")
        cleaned_username = cleaned_data.get("username")
        if fetchuser(cleaned_username) == -1:
            self.add_error("username","Please enter a valid Git-Hub username")
        return cleaned_data

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        first_name=self.cleaned_data["first_name"]
        last_name=self.cleaned_data["last_name"]
        user.first_name = first_name
        user.last_name = last_name
        user.set_password(self.cleaned_data["password1"])
        p=models.Profile(Userinfo=user)
        p.Userinfo.save()
        print(user.username)
        list=fetchuser(self.cleaned_data["username"])
        print(list)
        p.number_followers=list[2]
        p.last_updated=list[3]
        names,stargazers=fetchrepo(user.username)
        p.save()
        for i in range(len(names)):
            repo=models.Repository(name=names[i],stars=stargazers[i],owner=p)
            repo.save()
        
        if commit:
            user.save()
        return user