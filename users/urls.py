from django.urls import path

from users.views import Profile, request

app_name = 'users'

urlpatterns = [
    path('profile/', Profile, name='profile'),
    path('request/', request, name='request')

]
