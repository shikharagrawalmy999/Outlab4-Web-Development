from django.urls import path, include
from django.conf.urls import url
from .views import Explore
from .views import ExploreView
from .views import SignUpView
from .views import ProfileView
from .views import UpdateNow
urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('myprofile/', ProfileView, name='myprofile'),
    url(r'^explore/$', Explore, name="explore"),
    url(r'^explore/(?P<user_name>\w+)/$', ExploreView, name='exploreuser'),
    path('update/', UpdateNow, name='update'),
]