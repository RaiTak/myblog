from django.contrib.auth import get_user_model
from django.utils.text import slugify
from rest_framework import serializers
from transliterate import translit

from .models import Post


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['title', 'body', 'status']

    def create(self, validated_data):
        validated_data['slug'] = slugify(translit(validated_data['title'], 'ru', reversed=True))
        validated_data['author'] = self.context['request'].user
        return Post.objects.create(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    posts = serializers.PrimaryKeyRelatedField(many=True, queryset=Post.published.all())

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'posts']
