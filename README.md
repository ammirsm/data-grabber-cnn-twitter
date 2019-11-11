# CNN and Twitter Crawler for getting clear data
Basic setup to get data from twitter and CNN with a keyword.

* A crawler that crawls the latest 25 articles about Trump from CNN.com and his latest 25 tweets
* A simple website that displays the titles of the crawled information
* A convenient way of displaying the information after I click on one of the titles
* Word Cloud of lastests news and tweet


## Setup
1 - Install requirements
````
$ pip install -r requirements.txt
````
2 - Configure the database
````
$ python manage.py migrate
````
## Start the project
In order to start this project you will need to have running Django and Scrapyd at the same time.

In order to run Django
````
$ python manage.py runserver
````
In order to run Scrapyd
````
$ cd scrapy_app
$ scrapyd
````

At this point you will be able to send job request to Scrapyd. This project is setup with a demo spider from the oficial tutorial of scrapy. To run it you must send a http request to Scrapyd with the job info

We have two spider 'icrawler' for crawling CNN and 'twitter' for crawling twitter.

````
curl http://localhost:6800/schedule.json -d project=default -d spider=icrawler
````

The crawled data will be automatically be saved in the Django models

For running this you have an access on homepage two.
