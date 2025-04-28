# discussionboard/urls.py
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

app_name = 'discussionboard'

router = DefaultRouter()
router.register(r'api/posts', views.PostViewSet)
router.register(r'api/comments', views.CommentViewSet)

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('new/', views.post_create, name='post_create'),
    path('<int:post_id>/', views.post_detail, name='post_detail'),
    path('<int:post_id>/like/', views.like_post, name='like_post'),
    path('comment/<int:comment_id>/vote/', views.vote_comment, name='vote_comment'),
    path('', include(router.urls)),
]
