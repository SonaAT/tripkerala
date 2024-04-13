from django.shortcuts import render

def signIn(request):

    return render (request, "signin/signin.html")

def welcome(request):
    if request.method=="POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        username = ''
        for char in email:
            if char == '@':
                break
            elif char.isalnum():  # Check if the character is alphanumeric
                username += char
        username = username.capitalize()
        
    return render (request, "welcome/welcome.html", {
        "email": username,
        "password": password
    })
