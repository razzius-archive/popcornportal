from django.template import RequestContext

#HP EDIT THE BELOW

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


class HackPackify(object):
  def process_template_response(self, request, response):
    print response
    print response.context_data
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
    
    hackpack_context = {
        'pages': pages,
        'project_name': project_name,
        'founders': founders,
        'project_description': project_description,
        }
    if not response.context_data.__contains__('hackpack'):
      #HP add the hackpack dict to the page's context
      response.context_data['hackpack'] = hackpack_context
    response = RequestContext(request, response.context_data) #HP RequestContext is good practice. (I think).
    return response
