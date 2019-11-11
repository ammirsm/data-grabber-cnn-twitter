# -*- coding: utf-8 -*-
from uuid import uuid4
from urllib.parse import urlparse
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_POST, require_http_methods
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from scrapyd_api import ScrapydAPI
# from main.utils import URLUtil
from main.models import ScrapyItem, Tweet, News
import matplotlib.pyplot as pPlot
from wordcloud import WordCloud, STOPWORDS
import numpy as npy
from PIL import Image
from django.shortcuts import render
from django.conf import settings


# connect scrapyd service
scrapyd = ScrapydAPI('http://localhost:6800')


def create_word_cloud(string, file_name):
    maskArray = npy.array(Image.open(settings.STATIC_ROOT + '/cloud.jpg'))
    cloud = WordCloud(background_color="white", max_words=200, mask=maskArray, stopwords=set(STOPWORDS))
    cloud.generate(string)
    cloud.to_file(settings.MEDIA_ROOT + "/" + file_name)


def homepage(request):
    list_of_tweets = Tweet.objects.all().order_by('-created_at')[:15]
    dataset_tweet = " ".join([i.tweet for i in list_of_tweets]).lower()
    create_word_cloud(dataset_tweet, "tweets_cloud.png")

    list_of_news = News.objects.all().order_by('-created_at')[:25]
    dataset_news = " ".join([i.headline for i in list_of_news]).lower()
    create_word_cloud(dataset_news, "news_cloud.png")
    context = {
        "tweets": list_of_tweets,
        "news": list_of_news
    }
    return render(request, 'icrawler/home.html', context)


def article(request, id):
    news = News.objects.get(id=id)
    context = {
        "article": news
    }
    return render(request, 'icrawler/article.html', context)


@csrf_exempt
@require_http_methods(['POST', 'GET'])  # only get and post
def crawl(request):
    # Post requests are for new crawling tasks
    if request.method == 'POST':

        # domain = urlparse(url).netloc  # parse the url and extract the domain
        unique_id = str(uuid4())  # create a unique ID.
        # This is the custom settings for scrapy spider.
        type = request.POST["type"]
        # We can send anything we want to use it inside spiders and pipelines.
        # I mean, anything
        settings = {
            'unique_id': unique_id,  # unique ID for each record for DB
            'USER_AGENT': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
        }

        # Here we schedule a new crawling task from scrapyd.
        # Notice that settings is a special argument name.
        # But we can pass other arguments, though.
        # This returns a ID which belongs and will be belong to this task
        # We are goint to use that to check task's status.
        if type == "twitter":
            task = scrapyd.schedule('default', 'twitter',
                                    settings=settings)
        elif type == "cnn":
            task = scrapyd.schedule('default', 'icrawler',
                                    settings=settings)

        return JsonResponse({'task_id': task, 'unique_id': unique_id, 'status': 'started'})

    # Get requests are for getting result of a specific crawling task
    elif request.method == 'GET':
        # We were passed these from past request above. Remember ?
        # They were trying to survive in client side.
        # Now they are here again, thankfully. <3
        # We passed them back to here to check the status of crawling
        # And if crawling is completed, we respond back with a crawled data.
        task_id = request.GET.get('task_id', None)
        unique_id = request.GET.get('unique_id', None)

        if not task_id or not unique_id:
            return JsonResponse({'error': 'Missing args'})

        # Here we check status of crawling that just started a few seconds ago.
        # If it is finished, we can query from database and get results
        # If it is not finished we can return active status
        # Possible results are -> pending, running, finished
        status = scrapyd.job_status('default', task_id)
        if status == 'finished':
            try:
                # this is the unique_id that we created even before crawling started.
                item = ScrapyItem.objects.get(unique_id=unique_id)
                return JsonResponse({'data': item.to_dict['data']})
            except Exception as e:
                return JsonResponse({'error': str(e)})
        else:
            return JsonResponse({'status': status})
