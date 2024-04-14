from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import LoginForm, RegisterForm



def signin(request):
    if request.method=="POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user=authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            username = username.capitalize() 
            return render (request, "welcome/welcome.html", {
                "username": username 
            })
        else:
            return render(request, "signin/signin.html", {
                "message" : "Invalid credentials!"
            })
    else:
        return render(request, "signin/signin.html")

        
def signout(request):
    logout(request)

    return render(request, "signin/signin.html", {
        "message" : "Logged out!"
    })

def signup(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, "signin/signup.html", {'form': form})    
   
    if request.method == 'POST':
        form = RegisterForm(request.POST) 
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            username = user.username.capitalize() 
            return render (request, "welcome/welcome.html", {
                "username": username 
            })
        else:
            return render(request, "signin/signup.html", {'form': form})