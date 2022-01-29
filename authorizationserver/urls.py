from django.urls import path

from authorizationserver import views

name = 'authorizationserver'

urlpatterns = [
    path('login/', views.Auth.as_view({'post': 'auth'})),
    path('registration/', views.Auth.as_view({'post': 'registration'})),
    path('checkauth/', views.Permission_Auth.as_view({'get': 'is_auth'})),
    path('getroles/', views.Permission_Auth.as_view({'get': 'get_roles'})),
    path('gettoken/', views.TokenHandler.as_view({'get': 'get_token'}))
]