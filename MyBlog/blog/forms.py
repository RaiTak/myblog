from django import forms
from .models import Comment, Post


class EmailSharePostForm(forms.Form):
    name = forms.CharField(max_length=50, label='Имя')
    to = forms.EmailField(label='Кому')
    comments = forms.CharField(widget=forms.Textarea, label='Послание')


class CommentPostForm(forms.ModelForm):
    body = forms.CharField(label='Текст', widget=forms.Textarea())

    class Meta:
        model = Comment
        fields = ['body']


class SearchPostForm(forms.Form):
    query = forms.CharField(label='Ключ')


class PostAddForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = '__all__'
        exclude = ['slug', 'publish', 'author']