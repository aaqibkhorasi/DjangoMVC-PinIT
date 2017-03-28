from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views
from board_views import BoardCreate, BoardUpdate, BoardDelete, BoardDetail, BoardIndexView
import post.views



app_name = 'post'

urlpatterns = patterns ('',
    #BOARDS
    url(r'addboard', BoardCreate.as_view(), name='board_add'),  
    url(r'boards$', BoardIndexView.as_view(), name='board_index'),
    url(r'^board/(?P<pk>[0-9]+)$', BoardDetail.as_view(), name='board_detail'),
    url(r'^editboard/(?P<pk>[0-9]+)$', BoardUpdate.as_view(), name='board_update'),
    url(r'^deleteboard/(?P<pk>[0-9]+)$', BoardDelete.as_view(), name='board_delete'),

    #POSTS
    url(r'^$', post.views.ListPostView.as_view(), name='post-list',),
    url(r'^posts/(?P<post_id>[0-9]+)/$', views.detail, name='post-detail'),
    url(r'^new$', login_required(post.views.CreatePostView.as_view()), name='post-new'),
    url(r'^edit/(?P<pk>\d+)/$', login_required(post.views.UpdatePostView.as_view()), name='post-edit'),

    #VOTING
    url(r'^(?P<post_id>[0-9]+)/upvote/$', login_required(views.upvote), name='upvote-detail'),
    url(r'^(?P<post_id>[0-9]+)/downvote/$', login_required(views.downvote), name='downvote-detail'),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),
    
    #USERS
    url(r'^user/register/$', views.user_register, name='user-register'),
    url(r'^user/login/$', views.user_login, name='user-login'),
    url(r'^user/logout/$', views.user_logout, name='user-logout'),
    url(r'^user/editInfo/$', views.user_edit_info, name='user-editInfo'),
    url(r'^user/info/$', views.user_info, name='user-info'),
    url(r'^user/info/(?P<user_id>[0-9]+)$', views.other_info, name='other-info'),
    url(r'^user/editPassword/$', views.user_edit_pass, name='user-editPass'),

    #COMMENTS
    url(r'^comments/delete/(?P<comment_id>.*)/$', views.delete_own_comment, name='delete_own_comment'),
    url(r'^comments/edit/(?P<comment_id>.*)/$', views.edit_own_comment, name='edit_own_comment'),
) +  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
#     # static files (images, css, javascript, etc.)
#     urlpatterns += patterns('',
#         (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
#         'document_root': settings.MEDIA_ROOT}))
