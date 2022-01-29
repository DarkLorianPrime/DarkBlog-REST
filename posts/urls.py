from django.urls import path
from rest_framework import routers

from posts import views

router = routers.DefaultRouter()
router.register(r'(?P<blog_id>[0-9]+)/posts', views.Posts)

urlpatterns = [
    path('<int:blog_id>/posts/havepermission/', views.Posts.as_view({'get': 'havepermission'})),
    path('<int:blog_id>/posts/<int:pk>/like', views.Posts.as_view({'post': 'like'})),
]
urlpatterns += router.urls
