from django.views.generic import DetailView, ListView
from clickgestion.comments.models import Comment
from clickgestion.comments.filters import CommentFilter
from pure_pagination.mixins import PaginationMixin
from django.shortcuts import get_object_or_404
from clickgestion.videos.models import Video
from clickgestion.users.models import User


class CommentDetailView(DetailView):
    model = Comment
    context_object_name = 'comment'


class CommentListView(PaginationMixin, ListView):
    model = Comment
    context_object_name = 'comments'
    paginate_by = 10
    header = 'Comments'
    queryset = None
    request = None
    filter = None

    def get(self, request, *args, **kwargs):
        self.request = request
        return super().get(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = self.header
        if not self.queryset:
            self.queryset = Comment.objects.all()
        total_comments = self.queryset.count()
        total_users = self.queryset.distinct('user').count()
        total_videos = self.queryset.distinct('video').count()
        context['total_comments'] = total_comments
        context['total_users'] = total_users
        context['total_videos'] = total_videos
        context['filter'] = self.filter

        return context

    def get_queryset(self):
        queryset = Comment.objects.all()
        video_id = self.kwargs.get('video_id', None)
        user_id = self.kwargs.get("user_id", None)
        comment_id = self.kwargs.get("comment_id", None)
        if video_id:
            video = get_object_or_404(Video, pk=video_id)
            self.header = self.header + ' about "{}"'.format(video.title)
            queryset = queryset.filter(video=video)
        if user_id:
            user = get_object_or_404(User, pk=user_id)
            self.header = self.header + " by {}".format(user.name)
            queryset = queryset.filter(user=user)
        if comment_id:
            comment = get_object_or_404(Comment, pk=comment_id)
            self.header = "Replies to {}".format(comment)
            queryset = queryset.filter(reply_to=comment_id)
        # Filter
        self.filter = CommentFilter(self.request.GET, queryset=queryset)
        self.queryset = self.filter.qs

        return self.queryset


