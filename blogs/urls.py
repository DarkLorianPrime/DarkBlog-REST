from django.urls import path

from blogs import views

name = 'blogs'

urlpatterns = [
    path('blogs/', views.Blogs.as_view({'get': 'list', 'post': 'create'}))
]