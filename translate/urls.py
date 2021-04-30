from django.urls import path
from . import views

app_name = 'translate'

urlpatterns = [
    path('', views.translate, name='translate')
]
