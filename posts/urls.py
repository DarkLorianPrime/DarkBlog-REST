from django.urls import path
from rest_framework import routers

from posts import views

router = routers.DefaultRouter()
router.register(r'(?P<blog_id>[0-9]+)/posts', views.Posts)
router.register(r'(?P<blog_id>[0-9]+)/posts/(?P<post_id>[0-9]+)/comments', views.CommentsViewSet)
urlpatterns = [
    path('<int:blog_id>/posts/havepermission/', views.Posts.as_view({'get': 'havepermission'})),
    path('<int:blog_id>/posts/<int:pk>/like', views.Posts.as_view({'post': 'like'})),
    path('<int:blog_id>/posts/<int:post_id>/comments/<int:pk>/like/', views.CommentsViewSet.as_view({'post': 'like'})),
    path('posts/last/', views.MainPage.as_view({"get": "list"})),
]
urlpatterns += router.urls
