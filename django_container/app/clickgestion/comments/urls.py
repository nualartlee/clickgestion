from django.conf.urls import url
from clickgestion.comments import views

urlpatterns = [
    url(r'^$', views.CommentListView.as_view(), name='comments'),
    url(r'^replies/(?P<comment_id>[a-f0-9]{40})/$', views.CommentListView.as_view(), name='comments'),
    url(r'^user/(?P<user_id>[a-f0-9]{40})/$', views.CommentListView.as_view(), name='comments'),
    url(r'^video/(?P<video_id>[^/]{11})/$', views.CommentListView.as_view(), name='comments'),
    url(r'^(?P<pk>[a-f0-9]+)/$', views.CommentDetailView.as_view(), name='comment'),
]
