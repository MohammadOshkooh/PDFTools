from django.urls import path

from .views import merge

app_name = 'app'
urlpatterns = [
    path('', merge, name='merge')
]
