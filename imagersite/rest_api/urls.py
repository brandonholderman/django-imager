from django.urls import path
from .views import PhotoListApi
from rest_framework.authtoken import views


urlpatterns = [
    path('photo/', PhotoListApi.as_view(), name='photo_list_api'),
    path('auth-token-login/', views.obtain_auth_token),
]
