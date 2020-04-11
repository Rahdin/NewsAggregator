import requests
from django.shortcuts import render, redirect
from bs4 import BeautifulSoup as BSoup
from .models import Headline

# Create your views here.
def scrapeBI(request):
    session = requests.Session()
    session.headers = {"User-agent": "Googlebot/2.1 (https://www.google.com/bot.html)"}
    url = "https://www.businessinsider.com/"
    content = session.get(url).content
    soup = BSoup(content, "html.parser")
    #get the featured article of the day
    featured_news_title = soup.find('h1', class_='tout-title featured-tout')
    featured_news_image_source = soup.find('img', class_='lazy-image js-queued js-rendered')
    featured_news_image_src = featured_news_image_source.attrs['src']
    featured_news_link = soup.find('a', class_='tout-title-link' ).attrs['href']
    new_headline = Headline()
    new_headline.title = featured_news_title
    new_headline.image = featured_news_image_src
    new_headline.url = featured_news_link
    new_headline.save()
    return redirect("../")

def newslist(request):
    newsheadline = Headline.objects.all()
    context = {'object_list': newsheadline}
    return render(request, 'news/home.hmtl', context)
