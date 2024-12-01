from django.shortcuts import render, redirect


# Create your views here.
def index(request):
    return render(request, "index.html")

def blog_create(request):
    return render(request, "blog_create.html")

def blogs(request):
    return render(request, "blogs.html")