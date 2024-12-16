from django.shortcuts import render
from .scripts import scrape_imdb_news
from django.http import JsonResponse
from .models import News
from django.shortcuts import get_object_or_404


def run_scraper(request):
    scrape_imdb_news()
    return JsonResponse({
        "status" : True,
        "message" : "scraper executed"
    })


def index(request):
    return render(request, 'index.html', context={
        "news_data" : News.objects.all()
    })