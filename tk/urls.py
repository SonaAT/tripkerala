from django.urls import path
from . import views

urlpatterns=[
    path("signin",views.signIn,name="signIn"),
    path("welcome",views.welcome,name="welcome")
]