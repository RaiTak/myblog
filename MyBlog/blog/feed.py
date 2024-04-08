import markdown
from django.contrib.auth import get_user_model
from django.contrib.syndication.views import Feed
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import truncatewords_html
from django.urls import reverse_lazy
from .models import Post

user_model = get_user_model()

class LatestPostsFeed(Feed):
    title = 'Новости'
    link = reverse_lazy('blog:list')
    description = 'Новые статьи'

    def items(self):
        return Post.published.all()[:5]
    
    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords_html(markdown.markdown(item.body), 30)

    def item_pubdate(self, item):
        return item.publish
