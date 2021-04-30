from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
     path('', views.post_list, name='post_list'),     
     path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
     path('post-search/', views.post_search, name='post_search'),
     path('signup/', views.SignUpView.as_view(), name='signup'),
     path('post/<int:pk>/', views.post_detail, name='post_detail'),
     path('post/new/', views.post_new, name='post_new'),
     path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
     path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),     
]
