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
import os, sys, datetime, json
# from bootstrap.forms import BootstrapModelForm, Fieldset

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
  project_name = "A Django HackPack Project" 
  
  #HP project_description is used in <meta name="description"> and the about page.
  project_description = "A super cool app."
  
  #HP Founder information is in popups linked from the footers, the about page, and <meta name="author">
  founders = [
    {'name':'Alex Rattray',
       'email':'rattray@wharton.upenn.edu',
       'url':'http://alexrattray.com/',
       'blurb':'I\'m Alex. I like webdev and most things Seattle.',
       'picture':'http://profile.ak.fbcdn.net/hprofile-ak-ash2/273392_515004220_1419119046_n.jpg'},
    {'name':'Greg Terrono',
       'email':'gterrono@seas.upenn.edu',
       'url':'http://twitter.com/',
       'blurb':'I\'m Greg. I like webdev and most things Boston. And Dogs.',
       'picture':'http://chucknorri.com/wp-content/uploads/2011/03/Chuck-Norris-14.jpg'},
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
  message = 'hello world!' #HP just used for example. Don't do this.
  context = {
    'thispage': 'Home', #HP necessary to know which page we're on (for nav). Always spell the same as the 'Name' field in hackpackify()'s `pages` variable
    'message':message,
  }
  return render_to_response('index.html', hackpackify(request, context))

def about(request):
  context = {
    'thispage':'About', #HP necessary to know which page we're on (for nav). Always spell the same as the 'Name' field in hackpackify()'s `pages` variable
  }
  return render_to_response('about.html', hackpackify(request, context))
