from django.shortcuts import render_to_response
from django.utils import feedgenerator
from post.models import Post
import re

def index(request):
	templatePath = '../templates/feed/feed.html'	
	feed = feedgenerator.Rss201rev2Feed(
		title=u"Pin It!",
		link=u"http://cmpt470.csil.sfu.ca:8003/PinIt",
		description=u"A virtual bulletin board",
		language=u"en",
	)
	
	posts = Post.objects.all()
	for post in posts:		
		feed.add_item(
			title=post.title,
			link="http://{0}/posts/{1}/".format(request.get_host(), post.id),
			description=post.description
		)	
	return render_to_response(templatePath, {'feed':format(feed.writeString('utf-8'))})

def format(string):
	string = string.replace('>', '>\n')
	string = string.replace('<', '\n<')
	string = string.replace('\n\n', '\n')
	return string