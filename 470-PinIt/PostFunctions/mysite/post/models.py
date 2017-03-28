from django.db import models
from django.core.urlresolvers import reverse
from thumbs import ImageWithThumbsField
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Board(models.Model):
    name = models.CharField("Board name", max_length = 40)
    created = models.DateTimeField("Created data", auto_now_add = True)
    description = models.CharField(max_length=255)
    subscribers = models.ManyToManyField('UserProfile', blank=True)

    def __str__(self):
        return ('%s') % self.name

    def get_absolute_url(self):
        return reverse('posts:board_detail', kwargs={'pk': self.id})

    class Meta:
        ordering = ['created']

class PrivateBoard(Board):
    allowed_users = models.ManyToManyField('UserProfile')

class Post(models.Model):
    publisher = models.ForeignKey(User, null=True)
    title = models.CharField(max_length=255)
    board = models.ForeignKey(Board, null=True, blank=True, default=None)
    description = models.CharField(max_length=255)
    content = models.TextField()
    location = models.CharField(max_length=255, blank=True)
    published = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    upvote = models.IntegerField(default=0)
    downvote = models.IntegerField(default=0)

    image = models.ImageField(upload_to='images/',
    	null=True,
        blank=True,
        editable=True,

    )
    thumbImage = ImageWithThumbsField(upload_to='images/', sizes=((125,125),(200,200), (400,650)))

    class Meta:
        ordering = ['-created']

    def __unicode__(self):
        return "{0}".format(self.image)

    def __str__(self):
        return ('%s') % self.title

	def get_absolute_url(self):
		return reverse('post-detail', kwargs={'pk': self.id})
		
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    picture = models.ImageField(upload_to='images/user_images/', blank=True, null=True,)
    sub_boards = models.ManyToManyField(Board, blank=True)
    access_list = models.ManyToManyField(PrivateBoard, related_name='access_list', blank=True)

    def __str__ (self):
        return ('%s') % self.user


class Voter(models.Model):
	# This field is required. (Implementing Django's authentication system)
	user = models.ForeignKey(User)
	post = models.ForeignKey(Post)
	votedUP = models.BooleanField(default=False)
	def __str__ (self):
			if (self.votedUP == True):
				voteChoice = 'up'
			else:
				voteChoice = 'down'
			return ('%s') % self.user + " voted " + voteChoice
