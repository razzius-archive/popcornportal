# Create your views here.
#HP Django stuff
from django import forms
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext

#HP app-specific stuff
from app.models import *
from app.forms import *
import settings, urls

#HP everything else (these are usually useful)
import os, sys, datetime, json, re, string, urllib2, logging, random
# from bootstrap.forms import BootstrapModelForm, Fieldset
from bs4 import BeautifulSoup

trailer = re.compile("<link rel='alternate' type='text.html' href='https:..www.youtube.com.watch.v=(.*?)&")
non_numbers = re.compile('[^\d_]+')
non_chars = re.compile('[^\w_\s]+')
image_url_pattern = re.compile(r'\._(.+)\.jpg')
linfo = logging.info


#HP:
def hackpackify(request, context):
  '''
  Updates a view's context to include variables expected in base.html
  Intended to make boilerplate info conveyance and menu bars quick and easy.
  and returns a RequestContext of the resulting dict (which is usually better).

  CHANGE EVERYTHING IN THIS!
  '''
  pages = []
  for urlpat in urls.urlpatterns:
    if urlpat.__dict__.__contains__('name'):
      if '(' not in urlpat.regex.pattern:
        pages.append({'name':urlpat.name, 'url':urlpat.regex.pattern.replace('^','/').replace('$','')})
  
  #HP project_name is used in navbar, copyright (footer), about page, and <title>
  project_name = "Popcorn Portal" 
  
  #HP project_description is used in <meta name="description"> and the about page.
  project_description = "Pick Flicks based on their innards"
  
  #HP Founder information is in popups linked from the footers, the about page, and <meta name="author">
  founders = [
    {'name':'Alex Rattray',
       'email':'rattray@wharton.upenn.edu',
       'url':'http://alexrattray.com/',
       'blurb':'I\'m Alex. I like webdev and most things Seattle.',
       'picture':'http://profile.ak.fbcdn.net/hprofile-ak-ash2/273392_515004220_1419119046_n.jpg'},
    {'name':'Razzi Abuissa',
       'email':'razzi.abuissa@facebook.com',
       'url':'http://www.thedp.com/staff/razzi_abuissa',
       'blurb':'Razzi is rad. ',
       'picture':'http://sphotos-a.xx.fbcdn.net/hphotos-ash4/303412_10151222262202576_730518393_n.jpg'},
    ]
  hackpack_context = {
      'pages': pages,
      'project_name': project_name,
      'founders': founders,
      'project_description': project_description,
      }
  if not context.__contains__('hackpack'):
    #HP add the hackpack dict to the page's context
    context['hackpack'] = hackpack_context

  return RequestContext(request, context) #HP RequestContext is good practice. (I think).

def index(request):
  context = {
  }
  return render_to_response('index.html', hackpackify(request, context))

def about(request):
  context = {
  }
  return render_to_response('about.html', hackpackify(request, context))

def getMovieFromNYT(request, bubble1="neighbor", bubble2="totoro"):
    #make the api call to NYT
    query = bubble1 + "+" + bubble2
    linfo(query)
    page = urllib2.urlopen("http://en.wikipedia.org/w/api.php?action=query&list=search&srseach={}&srprop=timestamp".format(query))
    NYTResponse = page.read()
    linfo(NYTResponse)
    # do something with 'results' here
    # convert to a variable which is a string of the movie name
    # call the youtube api and get a video url
    return HttpResponse(NYTResponse)

def getKeywords(request):
  keyword_pairs = []

  with open('keyword1000.html', 'rU') as keyword_out_file:
    soup = BeautifulSoup(keyword_out_file.read())
    links = soup.findAll('span')
    
    for link in links:
        text = link.getText()
        (name, num) = text.rsplit('(',1)
        num = int(non_numbers.sub('', num)) # get rid of non-digits so it can be an int
        name = str(non_chars.sub('',name)) #get rid of noncharacter symbols 
        slug = name.lower().replace(' ','-')
        linfo(name+str(num))
        keyword_pairs.append([name, slug, num])
    # keyword_pairs.sort(key=lambda x: -x[-1]) #this ranks by number of flicks
    random.shuffle(keyword_pairs)
    linfo(keyword_pairs)
    response = json.dumps(keyword_pairs[:100]) # only first 

  return HttpResponse(response, content_type="application/json")

def _getMoviesFromBubbles(bubbles):
    '''
    takes a comma-separated list of bubbles of arbitrary length. returns list of movies
    '''
    url = 'http://www.imdb.com/keyword/'
    bubbles = bubbles.split(',')
    for bubble in bubbles:
        url+=str(bubble)
        url+='/'
    linfo(url)
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page.read())
    linfo(soup.select('table.results'))
    try:
      results = soup.select('table.results')[0]
    except:
      return HttpResponse('None Available')

    rows = results.select('tr.detailed') #detailed limits to top 10 and excludes headers
    movies = []
    for row in rows:
        cells = row.findAll('td') 
        name = cells[2].a.get_text()
        year = cells[2].span.get_text()
        year = non_numbers.sub('', year)
        if len(cells[2].select('p.outline')) > 0:
            description = cells[2].select('p.outline')[0].get_text()
        else:
            description = ''
        image_url = cells[1].find('img')['src']
        linfo(image_url)
        image_url = image_url_pattern.sub('',image_url)+'.jpg'
        linfo(image_url)
        if '10' in row.select('td.user_rating')[0].get_text():
            rating = float(row.select('td.user_rating')[0].b.string)
        else:
            rating = None
        num_votes = float(row.select('td.num_votes')[0].get_text().replace(',',''))
        video = _getVideoFromYoutube(name, year)
        movies.append({
            'name':name,
            'year':year,
            'description':description,
            'image_url':image_url,
            'rating':rating,
            'num_votes':num_votes,
            'video':video,
            })
    linfo(movies)
    return movies

def getMoviesFromBubbles(request, bubbles):
  movies = _getMoviesFromBubbles(bubbles)
  response = json.dumps(movies)
  return HttpResponse(response)

# getMoviesForBubbles('hi', 'boyfriend-girlfriend-relationship,murder,psychiatrist')

def _getVideoFromYoutube(movieTitle, year):
  #get the words from the title
  linfo(movieTitle+year)
  words = movieTitle.split()
  movie = ""
  for word in words:
    movie += word + "+"
  movie+= year+"+"
  movie += "Trailer"
  page = urllib2.urlopen("https://gdata.youtube.com/feeds/api/videos?q={}&orderby=relevance&start-index=1&max-results=1&v=2".format(movie))
  xml=page.read()
  try:
    video = re.findall(trailer, xml)[0]
  except:
    video = ''
  return video 

def getVideoFromYoutube(request, movieTitle, year):
  video = _getVideoFromYoutube(movieTitle, year)
  return HttpResponse(video)

def movieCarousel(request, bubbles):
  context = _getMoviesFromBubbles(bubbles)
  return render_to_response('movieCarousel.html', context)