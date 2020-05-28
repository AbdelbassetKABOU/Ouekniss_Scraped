
import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from requests.compat import quote_plus
from . import models

# Create your views here.

#BASE_CRAIGSLIST_URL = 'https://losangeles.craigslist.org/search/?query={}'
BASESE_OUEDKNISS_URL = 'https://www.ouedkniss.com/'
BASE_OUEDKNISS_URL = 'https://www.ouedkniss.com/{}-r'
# BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'


def home(request):
    return render(request, 'base.html')


def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    final_url = BASE_OUEDKNISS_URL.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')

    post_listings = soup.find_all('ul', {'class': 'annonce_left'})
  
    final_postings = []
    for post in post_listings:
        print ('--------------------------')         
        #post_title = post.find(class_='result-title').text
        post_title = post.find(class_='annonce_titre').text 
        print (post_title)

        post_url = post.find('a').get('href')
        post_url = BASESE_OUEDKNISS_URL+post_url
        print ('post_url = ', post_url)


        postimgs = post.find(class_='annonce_image')
        postimg = postimgs.find(class_='annonce_image_img')
        post_image_url = postimg.get('style')[15:-25]
        print ('post_image_url =', post_image_url)


        mytext = post.find(class_='annonce_text')
        prixs = mytext.find(class_='annonce_prix')
        if prixs:
            post_price = prixs.text
        else:
            post_price = 'N/A'    
        print ('post_price =', post_price)
         
        final_postings.append((post_title, post_url, post_price, post_image_url))

    stuff_for_frontend = {
        'search': search,
        'final_postings': final_postings,
    }

    return render(request, 'main/new_search.html', stuff_for_frontend)
    # return render(request, 'base.html')