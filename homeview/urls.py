from django.urls import path
from .views import homepage,aboutpage, PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, like_post

urlpatterns = [
    path('',PostListView.as_view(), name="home"),
    path('post/<int:pk>/', PostDetailView, name="postdetail"),
    path('post/new/', PostCreateView.as_view(), name="postcreate"),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name="postupdate"),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name="postdelete"),
    path('like_post',like_post,name="like_post"),
    path('aboutpage/', aboutpage, name="about"),
]
