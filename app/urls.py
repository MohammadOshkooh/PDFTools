from django.urls import path

from .views import merge, split

app_name = 'app'
urlpatterns = [
    path('merge/', merge, name='merge'),
    path('split/', split, name='split')
]
