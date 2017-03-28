from django.shortcuts import render
from django.http import HttpResponse

from post.models import Post, UserProfile, Voter
from django.contrib.auth.models import User
from post.forms import PostForm
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render, render_to_response, redirect
from django.views.generic.edit import FormView
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse

from django.views.generic.detail import SingleObjectMixin
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import UserForm, UserProfileForm, UserUpdateForm, UserPassUpdateForm
import os 

from django.shortcuts import get_object_or_404

from django.http import JsonResponse
import json

# DELETE ACTIONS FOR COMMENT 
import django_comments
from django_comments.models import Comment
from django_comments.views.moderation import perform_delete
# from django_commrate import perform_delete

from tastypie.models import ApiKey

# Create your views here.
def index(request):
	posts = Post.objects.filter(published=True)
	return render(request, 'post/view.html', {'posts': posts, 'voters':voters})

class ListPostView(ListView): 
	model = Post
	template_name = 'post/view_post.html'

class CreatePostView(FormView):
	form_class = PostForm
	template_name = 'post/edit_post.html'

	def get_success_url(self):
		return reverse('posts:board_index')

	def form_valid(self, form):
		new_post = form.save(commit=True)
		if self.request.user:
			new_post.publisher = self.request.user
		new_post.upvote = 0
		new_post.downvote = 0
		new_post.save()
		# messages.success(self.request, 'File uploaded!')
		return super(CreatePostView, self).form_valid(form)

	def get_context_data(self, **kwargs):
		context = super(CreatePostView, self).get_context_data(**kwargs)
		context['action'] = reverse('posts:post-new')
		return context

class UpdatePostView(UpdateView):
	template_name = 'post/edit_post.html'
	form_class = PostForm
	# success_url = '/some/url'

	def get_success_url(self):
		return reverse('posts:board_index')

	def get_object(self): #and you have to override a get_object method
		return get_object_or_404(Post, pk=self.kwargs['pk'])

	
def detail(request, post_id):
	post = get_object_or_404(Post, pk=post_id)
	base=os.path.basename(post.thumbImage.url)
	filename= os.path.splitext(base)

	voters = Voter.objects.filter(post_id=post_id)
	userprofiles = UserProfile.objects.all()

	
	# filename=os.path.splitext(post.thumbImage.url)[0]
	# head, tail = os.path.split(post.url)
	# filename=tail.split(.)
	thumbname = filename[0] + '.400x650' + filename[1]
	return render(request, 'post/detail.html', {'post': post , 'thumbname':thumbname,'filename':filename[0] , 'base':base, 'ext':filename[1], 'voters':voters, 'userprofiles':userprofiles})

@login_required
def upvote(request, post_id):
	p = get_object_or_404(Post, pk=post_id)
	user = request.user
	if Voter.objects.filter(post_id = p.id, user_id=user.id).exists():
		v = get_object_or_404(Voter, post_id=p.id, user_id=user.id)
		if not v.votedUP:
			p.upvote += 1
			p.downvote -= 1
			p.save()
			data = {
				'count' : p.upvote,
			}
			v.votedUP = not v.votedUP
			v.save()
			return JsonResponse({'count': p.upvote})
	else:
		if request.method == "GET":
			p.upvote += 1
			p.save()
			data = {
				'count' : p.upvote,
			}
			v = Voter(user=request.user, post=p, votedUP=True)
			v.save()
			return JsonResponse({'count': p.upvote})
	return JsonResponse({'count': p.upvote})

@login_required
def downvote(request, post_id):
	p = get_object_or_404(Post, pk=post_id)
	user = request.user
	if Voter.objects.filter(post_id = p.id, user_id=user.id).exists():
		v = get_object_or_404(Voter, post_id=p.id, user_id=user.id)
		if v.votedUP:
			p.downvote += 1
			p.upvote -= 1
			p.save()
			data = {
				'count' : p.downvote,
			}
			v.votedUP = not v.votedUP
			v.save()
			return JsonResponse({'count': p.downvote})
	else:
		if request.method == "GET":
			p.downvote += 1
			p.save()
			data = {
				'count' : p.downvote,
			}
			v = Voter(user=request.user, post=p, votedUP=False)
			v.save()
			return JsonResponse({'count': p.downvote})
	return JsonResponse({'count': p.downvote})

def user_register(request):
	context = RequestContext(request)
	templatePath = '../templates/user/register.html'

	# A boolean value for telling the template whether the registration was successful.
	# Set to False initially. Code changes value to True when registration succeeds.
	registered = False

	if request.method == 'POST':
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)

		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()
			originPw = user.password
			user.set_password(user.password) # hash the password with the set_password method.
			user.save()

			profile = profile_form.save(commit=False)
			profile.user = user

			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']
			profile.save()
			# Update our variable to tell the template registration was successful.
			registered = True

			logedInUser = authenticate(username=user.username, password=originPw)
			if logedInUser:
				if logedInUser.is_active:
					login(request, logedInUser)					
					return redirect('posts:board_index')
				else:
					return HttpResponse("Your account is disabled.")
		# Invalid form or forms - mistakes or something else?
		# Print problems to the terminal.
		# They'll also be shown to the user.
	else:
		user_form = UserForm()
		profile_form = UserProfileForm()

	return render_to_response(
			templatePath,
			{'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
			context)

def user_login(request):
	context = RequestContext(request)
	templatePath = '../templates/user/login.html'
	isLoginFail = False

	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']

		# Use Django's machinery to attempt to see if the username/password
		# combination is valid - a User object is returned if it is.
		user = authenticate(username=username, password=password)

		# If we have a User object, the details are correct.
		# If None (Python's way of representing the absence of a value), no user
		# with matching credentials was found.
		if user:
			if user.is_active:
				login(request, user)
				return redirect('posts:board_index')
			else:
				return HttpResponse("Your account is disabled.")
		else:
			isLoginFail = True
	return render_to_response(templatePath, {'isLoginFail': isLoginFail}, context)


@login_required
def user_logout(request):
	logout(request)
	return redirect('posts:board_index')
@login_required
def user_edit_info(request):
	context = RequestContext(request)
	templatePath = '../templates/user/edit-info.html'
	isSaved = False

	# A boolean value for telling the template whether the registration was successful.
	# Set to False initially. Code changes value to True when registration succeeds.
	if request.method == 'POST':
		update_form = UserUpdateForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)

		if update_form.is_valid() and profile_form.is_valid():
			user = request.user
			user.first_name = update_form.cleaned_data['first_name']
			user.last_name = update_form.cleaned_data['last_name']
			user.email = update_form.cleaned_data['email']
			user.save()

			profile = get_object_or_404(UserProfile, user=request.user)
			if 'picture' in request.FILES:
				profile.picture.delete()
				profile.picture = request.FILES['picture']
				profile.save()
			isSaved = True

		# Invalid form or forms - mistakes or something else?
		# Print problems to the terminal.
		# They'll also be shown to the user.
	else:
		user = request.user
		update_form = UserUpdateForm(initial={'first_name':user.first_name,
									'last_name':user.last_name,
									'email':user.email,
									'isSaved': isSaved,})
		profile_form = UserProfileForm()
	profile = get_object_or_404(UserProfile, user=request.user)
	if not profile.picture:
		imgURL = "default.png"
	else:
		imgURL = os.path.basename(profile.picture.url)

	return render_to_response(
			templatePath,
			{'update_form': update_form, 'profile_form': profile_form, 'isSaved': isSaved, 'imgURL': imgURL},
			context)
@login_required
def user_info(request):
    context = RequestContext(request)
    templatePath = '../templates/user/info.html'
    profile = get_object_or_404(UserProfile, user=request.user)
    posts = Post.objects.filter(publisher=request.user)
    apikey = ApiKey.objects.get_or_create(user=request.user)[0].key

    if not profile.picture:
	   imgURL = "default.png"
    else:
	   imgURL=os.path.basename(profile.picture.url)

    return render_to_response(
		  templatePath,
		  {'imgURL': imgURL, 'posts': posts, 'apikey':apikey},
		  context)

def other_info(request, user_id):
    context = RequestContext(request)
    templatePath = '../templates/user/other-info.html'
    otherUser = get_object_or_404(User, pk=user_id)
    profile = get_object_or_404(UserProfile, user=otherUser)
    posts = Post.objects.filter(publisher=otherUser)

    if not profile.picture:

	   imgURL = "default.png"
    else:
	   # imgURL = profile.picture
	   imgURL=os.path.basename(profile.picture.url)

    return render_to_response(
		  templatePath,
		  {'otherUser': otherUser, 'imgURL': imgURL, 'posts': posts},
		  context)
@login_required
def user_edit_pass(request):
	context = RequestContext(request)
	templatePath = '../templates/user/edit-pass.html'
	isSaved = False

	# A boolean value for telling the template whether the registration was successful.
	# Set to False initially. Code changes value to True when registration succeeds.
	if request.method == 'POST':
		form = UserPassUpdateForm(request.POST)

		if form.is_valid():
			newPassword = form.cleaned_data['newPassword']
			newPassword_confirm = form.cleaned_data['newPassword_confirm']

			if newPassword == newPassword_confirm:
				request.user.set_password(newPassword)
				request.user.save()
				isSaved = True

				logedInUser = authenticate(username=request.user.username, password=newPassword)
				if logedInUser:
					if logedInUser.is_active:
						login(request, logedInUser)
					else:
						return redirect('posts:board_index')

		# Invalid form or forms - mistakes or something else?
		# Print problems to the terminal.
		# They'll also be shown to the user.
	else:
		form = UserPassUpdateForm()

	return render_to_response(
			templatePath,
			{'form': form, 'isSaved': isSaved,},
			context)
@login_required
def delete_own_comment(request, comment_id):
	comment = get_object_or_404(Comment, id=comment_id)
	postid = comment.content_object.id
	if comment.user == request.user:
		comment.is_removed = True
		comment.save()
	else: 
		raise Http404 
	return HttpResponseRedirect(reverse('posts:post-detail' ,  args=[postid]))
	# return HttpResponse("{0} deleted".format(comment_id))
@login_required
def edit_own_comment(request, comment_id):
	comment = get_object_or_404(Comment, id=comment_id)
	if request.method == "PUT":
		j = json.loads(request.body)
		comment.comment = j["comment"]
		comment.save()
		return HttpResponse(json.dumps(j), content_type="application/json")
	return HttpResponse("{0} edited".format(comment_id))

