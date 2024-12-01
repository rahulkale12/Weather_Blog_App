from django.urls import path
from . import views

urlpatterns = [
    path('blogger_register/', views.blogger_register, name="blogger_register"),
    path('blogger_login/',views.blogger_login, name="blogger_login"),
    path('user_register/', views.user_register, name="user_register"),
    path('user_login/', views.user_login, name="user_login"),

]