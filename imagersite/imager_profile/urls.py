from django.urls import path
from .views import profile_view, library_view


urlpatterns = [
    path('', profile_view, name='profile'),
    path('<str:username>', profile_view, name='named_profile'),
    path('', library_view, name='library'),
    path('<str:username>/library/', library_view, name='library'),
    # path('settings/<str:username', profile_view, name='settings'),
]
