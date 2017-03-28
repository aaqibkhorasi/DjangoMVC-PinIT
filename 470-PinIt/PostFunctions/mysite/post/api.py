from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import DjangoAuthorization, Authorization
from tastypie.resources import ModelResource, ALL
from post.models import Board, Post
from django.contrib.auth.models import User
from tastypie import fields
from tastypie.exceptions import ImmediateHttpResponse
from tastypie import http
from django.utils.html import escape
import re

class PostAuthorization(Authorization):
	def __init__(self):
		pass

	def read_list(self, object_list, bundle):        
		return object_list

	def read_detail(self, object_list, bundle):        
		return True

	def create_list(self, object_list, bundle):  		
		raise ImmediateHttpResponse(response=http.HttpNotImplemented("Not available."))

	def create_detail(self, object_list, bundle):		
		return True
		
	def update_list(self, object_list, bundle):
		return object_list

	def update_detail(self, object_list, bundle):
		if str(re.findall("""user\/([\d]*)\/$""", bundle.data['publisher'])[0]) != str(bundle.request.user.id):
			raise ImmediateHttpResponse(response=http.HttpUnauthorized("User can only update own posts."))
		else:
			return True			

	def delete_list(self, object_list, bundle):
		raise ImmediateHttpResponse(response=http.HttpNotImplemented("Not available."))

	def delete_detail(self, object_list, bundle):
		raise ImmediateHttpResponse(response=http.HttpNotImplemented("Not available."))

class BoardResource(ModelResource):
	class Meta:
		queryset = Board.objects.all()
		resource_name = 'board'
		list_allowed_methods = ['get']
		authentication = ApiKeyAuthentication()		

class UserResource(ModelResource):
	class Meta:
		queryset = User.objects.all()
		resource_name = 'user'
		fields = ['username', 'first_name', 'last_name', 'email', 'id']
		filtering = {'username': ALL}
		list_allowed_methods = ['get']
		authentication = ApiKeyAuthentication()

class PostResource(ModelResource):
	board = fields.ForeignKey(BoardResource, 'board', null=True, blank=True)
	publisher = fields.ForeignKey(UserResource, 'publisher', null=True, blank=True)

	class Meta:
		queryset = Post.objects.all()
		resource_name = 'post'
		list_allowed_methods = ['get', 'post', 'put']
		excludes = ['thumbImage', 'image', 'published']
		authentication = ApiKeyAuthentication()
		authorization = PostAuthorization()
		always_return_data = True

	def obj_update(self, bundle, **kwargs):
		post = Post.objects.get(id=bundle.data['id'])
		if 'title' in bundle.data:
			post.title = escape(bundle.data['title'])
		if 'content' in bundle.data:
			post.content = escape(bundle.data['content'])
		if 'description' in bundle.data:
			post.description = escape(bundle.data['description'])
		post.save()
		raise ImmediateHttpResponse(response=http.HttpAccepted("Post Updated."))

	def obj_create(self, bundle, **kwargs):
		post = Post.objects.create()
		try:
			userID = int(bundle.request.user.id)
		except:
			raise ImmediateHttpResponse(response=http.HttpApplicationError("Invalid User ID."))

		try:
			user = User.objects.get(id=userID)
			post.publisher = user
		except:
			raise ImmediateHttpResponse(response=http.HttpApplicationError("Invalid User ID."))

		if 'title' in bundle.data:
			post.title = escape(bundle.data['title']).encode('utf-8')
		else:
			post.title = ""
		if 'content' in bundle.data:
			post.content = escape(bundle.data['content']).encode('utf-8')
		else:
			post.content = ""
		if 'description' in bundle.data:
			post.description = escape(bundle.data['description']).encode('utf-8')
		else:
			post.description = ""
		if 'board' in bundle.data:
			try:
				boardID = int(bundle.data['board'])
			except:
				raise ImmediateHttpResponse(response=http.HttpApplicationError("Invalid Board ID."))
			try:
				board = Board.objects.get(id=boardID)
				post.board = board
			except:
				raise ImmediateHttpResponse(response=http.HttpApplicationError("Invalid Board ID."))
		else:
			raise ImmediateHttpResponse(response=http.HttpApplicationError("Missing Board ID."))
		post.save()
		raise ImmediateHttpResponse(response=http.HttpAccepted("Post Created."))
	