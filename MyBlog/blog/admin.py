from django.contrib import admin
from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['title']}
    list_display = ('title', 'author', 'status')
    list_filter = ('status', 'publish', 'author')
    search_fields = ('author__username', 'title')
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')
    list_editable = ('status',)
    list_per_page = 10


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created', 'active')
    list_filter = ('active', 'created')
    search_fields = ('author__username', 'post__title')
    raw_id_fields = ('author', 'post')
    date_hierarchy = 'created'
    ordering = ('active', 'created')
    list_editable = ('active', )
    list_per_page = 10
