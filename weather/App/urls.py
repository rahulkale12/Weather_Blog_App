from django.urls import path
from . import views

urlpatterns = [
    path('', views.index , name="index"),
    path('blog_create/', views.blog_create, name="blog_create"),
    path('delete_blog/<int:blog_id>/', views.delete_blog, name='delete_blog'),

    path('my_blogs/', views.my_blogs, name="my_blogs"),
    path('blog_comment/<int:id>/',views.blog_comment, name='blog_comment'),
    path('edit_comment/<int:id>/',views.edit_comment, name='edit_comment'),
    path('delete_comment/<int:id>/',views.delete_comment, name='delete_comment'),

    path('like_blog/<int:id>/', views.like_blog, name="like_blog"),

    
]