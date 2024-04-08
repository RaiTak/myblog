from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.postgres.search import TrigramSimilarity
from django.core.mail import send_mail
from django.db.models import Count
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy, reverse
from django.utils.text import slugify
from django.views.generic import ListView, DetailView, FormView, CreateView, DeleteView, UpdateView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, RetrieveAPIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .models import Post, Comment
from .forms import EmailSharePostForm, CommentPostForm, PostAddForm
from taggit.models import Tag
from transliterate import translit
from blog.serializers import PostSerializer, UserSerializer


class PostListView(ListView):
    template_name = 'blog/list.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        tag_slug = self.kwargs.get('tag_slug')
        if tag_slug:
            tag = get_object_or_404(Tag, slug=self.kwargs['tag_slug'])
            return Post.published.filter(tags__in=[tag])

        return Post.published.all()


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    slug_url_kwarg = 'post_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        post_tags_ids = post.tags.values_list('id', flat=True)
        similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
        similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:3]

        context['similar'] = similar_posts
        context['comments'] = post.comments.filter(active=True)
        context['form'] = CommentPostForm()
        return context

    def get_object(self, queryset=None):
        queryset = super(PostDetailView, self).get_queryset()
        slug = self.kwargs.get(self.slug_url_kwarg)

        if self.request.user.is_authenticated:
            try:
                post = queryset.get(slug=slug)
            except Post.DoesNotExist:
                raise Http404("Post does not exist")

        else:
            try:
                post = queryset.filter(status=Post.Status.PUBLISHED).get(slug=slug)
            except Post.DoesNotExist:
                raise Http404("No Post matches the given query.")

        return post


class MyPostListView(LoginRequiredMixin, ListView):
    template_name = 'blog/mylist.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.groups.filter(name='moderator').exists():
                return Post.objects.filter(status=Post.Status.DRAFT)
            else:
                return Post.objects.filter(author=user)
        else:
            return reverse_lazy('main:home')


class PostShareView(FormView):
    form_class = EmailSharePostForm
    template_name = 'blog/share.html'
    success_url = reverse_lazy('main:home')

    def form_valid(self, form):
        post = get_object_or_404(Post, id=self.kwargs['post_id'], status=Post.Status.PUBLISHED)
        cd = form.cleaned_data
        post_url = self.request.build_absolute_uri(post.get_absolute_url())
        subject = f"{cd['name']} рекомендует вам прочитать {post.title}"
        message = f"Прочитайте {post.title} по ссылке: {post_url}\n\nКомментарии {cd['name']}: {cd['comments']}"
        send_mail(subject, message, 'kairatgamerhill@gmail.com', [cd['to']])
        return render(self.request, 'blog/share_done.html')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = get_object_or_404(Post, id=self.kwargs['post_id'], status=Post.Status.PUBLISHED)
        return context


class CommentPostView(LoginRequiredMixin, FormView):
    form_class = CommentPostForm
    template_name = 'blog/includes/comment_form.html'

    def form_valid(self, form):
        post = get_object_or_404(Post, id=self.kwargs['post_id'], status=Post.Status.PUBLISHED)
        comment = form.save(commit=False)
        comment.post = post
        comment.author = self.request.user
        comment.save()
        return HttpResponseRedirect(post.get_absolute_url())


class SearchPostView(ListView):
    template_name = 'blog/search.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('query')
        if query:
            results = Post.published.annotate(
                similarity=TrigramSimilarity('title', query)
            ).filter(similarity__gt=0.1).order_by('-similarity')

        else:
            results = Post.objects.none()

        return results


class PostAddView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostAddForm
    template_name = 'blog/post_add.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        cd = form.cleaned_data
        print(cd)
        post.slug = slugify(translit(cd['title'], 'ru', reversed=True))
        post.author = self.request.user
        saved_post = form.save()

        tags = form.cleaned_data.get('tags')

        if tags:
            saved_post.tags.set(tags)

        post_detail_url = reverse('blog:detail', kwargs={
            'year': post.created.year,
            'month': post.created.month,
            'day': post.created.day,
            'post_slug': post.slug,
        })

        return HttpResponseRedirect(post_detail_url)


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blog:mylist')
    template_name = 'blog/delete_confirm.html'

    def test_func(self):
        post = self.get_object()
        current_user = self.request.user == post.author
        moderator_user = self.request.user.has_perm('blog.delete_post')
        return current_user or moderator_user


class PostChangeView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'body', 'status', 'tags']
    template_name = 'blog/update.html'

    def test_func(self):
        post = self.get_object()
        current_user = self.request.user == post.author
        moderator_user = self.request.user.has_perm('blog.change_post')
        return current_user or moderator_user

    def get_success_url(self):
        obj = self.get_object()
        return reverse('blog:detail', kwargs={
            'year': obj.created.year,
            'month': obj.created.month,
            'day': obj.created.day,
            'post_slug': obj.slug,
        })

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user

        if user.groups.filter(name='moderator').exists():
            for f in form.fields:
                form.fields[f].widget.attrs['readonly'] = True

            form.fields['status'].widget.attrs.pop('readonly', None)

        return form


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment

    def test_func(self):
        comment = self.get_object()
        current_user = self.request.user == comment.author
        moderator_user = self.request.user.has_perm('blog.delete_comment')
        return current_user or moderator_user

    def get_success_url(self):
        comment = self.get_object()
        obj = comment.post
        return reverse('blog:detail', kwargs={
            'year': obj.created.year,
            'month': obj.created.month,
            'day': obj.created.day,
            'post_slug': obj.slug,
        })


class CommentChangeView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    template_name = 'blog/comment_update.html'
    fields = ['body']

    def test_func(self):
        comment = self.get_object()
        current_user = self.request.user == comment.author
        moderator_user = self.request.user.has_perm('blog.change_comment')
        return current_user or moderator_user

    def get_success_url(self):
        comment = self.get_object()
        obj = comment.post
        return reverse('blog:detail', kwargs={
            'year': obj.created.year,
            'month': obj.created.month,
            'day': obj.created.day,
            'post_slug': obj.slug,
        })


class PostApiViewSet(ReadOnlyModelViewSet):
    queryset = Post.published.all()
    serializer_class = PostSerializer


class UserListApiView(ListAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class UserDetailApiView(RetrieveAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
