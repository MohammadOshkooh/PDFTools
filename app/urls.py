from django.urls import path

from .views import merge, split, pdf_to_word, Index

app_name = 'app'
urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('merge/', merge, name='merge'),
    path('split/', split, name='split'),
    path('to-word', pdf_to_word, name='to_word'),
]
