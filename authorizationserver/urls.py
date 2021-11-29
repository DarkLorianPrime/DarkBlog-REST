from django.urls import path

from authorizationserver import views

name = 'authorizationserver'

urlpatterns = [
    path('login/', views.Login.as_view({'post': 'Auth'})),
    path('registration/', views.Login.as_view({'post': 'Registration'})),
    path('checkauth/', views.Login.as_view({'get': 'is_auth'}))
]