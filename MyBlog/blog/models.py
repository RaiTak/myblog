from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager

user = get_user_model()


class PublishMeneger(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Черновик'
        PUBLISHED = 'PB', 'Опубликован'

    title = models.CharField(max_length=150, verbose_name='Название')
    slug = models.SlugField(max_length=250, unique_for_date='publish', verbose_name='URL')
    body = models.TextField(verbose_name='Текст')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата последнего обновления')
    publish = models.DateTimeField(default=timezone.now, verbose_name='Дата публикации')
    author = models.ForeignKey(user, on_delete=models.CASCADE, related_name='posts', verbose_name='Автор')
    status = models.CharField(
        max_length=2, choices=Status.choices, default=Status.DRAFT, null=True, verbose_name='Статус')

    objects = models.Manager()
    published = PublishMeneger()
    tags = TaggableManager()

    class Meta:
        verbose_name = 'Статью'
        verbose_name_plural = 'Статьи'
        ordering = ['-publish']
        indexes = [models.Index(fields=['-publish'])]

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={
            'post_slug': self.slug,
            'year': self.publish.year,
            'month': self.publish.month,
            'day': self.publish.day})


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='Статья')
    author = models.ForeignKey(user, on_delete=models.CASCADE, related_name='comments', verbose_name='Автор')
    body = models.TextField(verbose_name='Текст')
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['created']
        indexes = [models.Index(fields=['created'])]

    def __str__(self):
        return f'Комментарий {self.author} в посту {self.post}'
