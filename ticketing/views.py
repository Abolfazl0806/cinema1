from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from ticketing.models import Movie, Cinema


def movie_list(request):
    # select data
    movies = Movie.objects.all()
    count = len(movies)
    context = {
        'movie_list': movies,
        'movie_count': count
    }

    return render(request, 'movie_list.html', context)


def cinema_list(request):
    cinemas = Cinema.objects.all()
    #count = len(movies)
    context = {
        'cinamas': cinemas
    }

    return render(request, 'cinema_list.html', context)

