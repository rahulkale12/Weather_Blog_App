from django.urls import path
from . import views

urlpatterns = [
    path('', views.index , name="index"),
    path('blog_create/', views.blog_create, name="blog_create"),
    path('blogs/', views.blogs, name="blogs"),
]