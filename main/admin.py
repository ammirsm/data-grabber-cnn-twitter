from django.contrib import admin
from main.models import News, Tweet


class QuoteAdmin(admin.ModelAdmin):
    list_display = ('author', 'text', )


class NewsAdmin(admin.ModelAdmin):
    list_display = ('headline', 'body', 'url', )


class TweetAdmin(admin.ModelAdmin):
    list_display = ('tweet', 'time', )


# Register your models here.
admin.site.register(News, NewsAdmin)
admin.site.register(Tweet, TweetAdmin)