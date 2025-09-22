from django.shortcuts import render

# Create your views here.
def home(req):
    return render(req,'home.html',{})

def register(req):
    return render(req,'register.html',{})

def todo(req):
    return render(req,'todo.html',{})