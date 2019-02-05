from clickgestion.comments.models import Comment
import django_filters


class CommentFilter(django_filters.FilterSet):

    text = django_filters.CharFilter(lookup_expr='icontains')
    text.field.widget.attrs['placeholder'] = 'Search in comment text'
    text.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Comment
        fields = ['text',]


