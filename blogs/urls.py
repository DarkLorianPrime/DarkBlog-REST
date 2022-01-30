from django.urls import path, include
from rest_framework import routers

from blogs import views

name = 'blogs'
router = routers.DefaultRouter()
router.register(r'', views.BlogViewSet)
urlpatterns = [
    path('', include(router.urls))
]
