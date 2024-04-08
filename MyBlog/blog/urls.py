from django.urls import path
from .views import PostListView, PostDetailView, MyPostListView, PostShareView, CommentPostView, SearchPostView, \
    PostAddView, PostDeleteView, PostChangeView, CommentDeleteView, CommentChangeView, UserListApiView, \
    UserDetailApiView, PostApiViewSet
from .feed import LatestPostsFeed


app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name='list'),
    path('tag/<str:tag_slug>/', PostListView.as_view(), name='list_by_tag'),
    path('myblog/', MyPostListView.as_view(), name='mylist'),
    path('myblog/add/', PostAddView.as_view(), name='post-add'),
    path('myblog/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('myblog/<int:pk>/change/', PostChangeView.as_view(), name='post-update'),
    path('myblog/comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
    path('myblog/comment/<int:pk>/change/', CommentChangeView.as_view(), name='comment-update'),
    path('post/<int:year>/<int:month>/<int:day>/<slug:post_slug>', PostDetailView.as_view(), name='detail'),
    path('post/<int:post_id>/share/', PostShareView.as_view(), name='share'),
    path('post/<int:post_id>/comment/', CommentPostView.as_view(), name='comment'),
    path('feed/', LatestPostsFeed(), name='feed'),
    path('search/', SearchPostView.as_view(), name='search'),

    path('api/v1/post/', PostApiViewSet.as_view({'get': 'list'}), name='post-api-list'),
    path('api/v1/post/<int:pk>/', PostApiViewSet.as_view({'get': 'retrieve'}), name='post-api-detail'),
    path('api/v1/users/', UserListApiView.as_view(), name='user-api-list'),
    path('api/v1/users/<int:pk>/', UserDetailApiView.as_view(), name='user-api-detail'),
]
