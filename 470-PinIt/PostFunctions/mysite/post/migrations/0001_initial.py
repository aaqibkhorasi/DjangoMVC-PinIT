# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import post.thumbs


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=40, verbose_name=b'Board name')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name=b'Created data')),
                ('description', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['created'],
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('location', models.CharField(default=None, max_length=255, blank=True)),
                ('published', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('upvote', models.IntegerField(default=0)),
                ('downvote', models.IntegerField(default=0)),
                ('image', models.ImageField(null=True, upload_to=b'images/', blank=True)),
                ('thumbImage', post.thumbs.ImageWithThumbsField(upload_to=b'images/')),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('picture', models.ImageField(null=True, upload_to=b'images/user_images/', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Voter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('votedUP', models.BooleanField(default=False)),
                ('post', models.ForeignKey(to='post.Post')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PrivateBoard',
            fields=[
                ('board_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='post.Board')),
            ],
            bases=('post.board',),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='sub_boards',
            field=models.ManyToManyField(to='post.Board', blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='post',
            name='board',
            field=models.ForeignKey(default=None, blank=True, to='post.Board', null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='publisher',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='board',
            name='subscribers',
            field=models.ManyToManyField(to='post.UserProfile', blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='access_list',
            field=models.ManyToManyField(related_name='access_list', to='post.PrivateBoard', blank=True),
        ),
        migrations.AddField(
            model_name='privateboard',
            name='allowed_users',
            field=models.ManyToManyField(to='post.UserProfile'),
        ),
    ]
