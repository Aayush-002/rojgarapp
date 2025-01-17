from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    return render(request, "index.html")


def about(request):
    return HttpResponse("Welcome to rojgarapp about page")


def contact(request):
    return HttpResponse("Welcome to rojgarapp contact page")
