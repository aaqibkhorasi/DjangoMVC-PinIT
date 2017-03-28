"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
	1. Add an import:  from blog import urls as blog_urls
	2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from post.api import BoardResource, PostResource, UserResource
from post import feed
from tastypie.api import Api
#only if time permits 
from django_comments.feeds import LatestCommentFeed

v1_api = Api(api_name='v1')
v1_api.register(BoardResource())
v1_api.register(UserResource())
v1_api.register(PostResource())

urlpatterns = [
	url(r'', include('post.urls', namespace='posts')),
	#url(r'^users/', include('user.urls', namespace='users')),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^comments/', include('django_comments.urls')),
	#only if time permits
	url(r'^feeds/latest/$', LatestCommentFeed()),
	url(r'^api/', include(v1_api.urls)),
	url(r'^feed.html', feed.index),
]
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
