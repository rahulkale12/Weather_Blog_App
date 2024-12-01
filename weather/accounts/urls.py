from django.urls import path
from . import views

urlpatterns = [
    path('blogger_register/', views.blogger_register, name="blogger_register"),
    path('blogger_login/',views.blogger_login, name="blogger_login"),
    

    path('blogger_profile/', views.blogger_profile, name='blogger_profile'),
    path('blogger_profile_pic/<int:id>/',views.blogger_profile_pic,name="blogger_profile_pic"),
    path('update_blogger_profile/<int:id>/', views.update_blogger_profile, name='update_blogger_profile'),
    path('edit_blogger_profile/<int:id>/', views.edit_blogger_profile, name='edit_blogger_profile'),
    path('delete_blogger_profile/<int:id>/', views.delete_blogger_profile, name="delete_blogger_profile"),
    path('blogger_logout/', views.blogger_logout, name="blogger_logout"),


    path('user_register/', views.user_register, name="user_register"),
    path('user_login/', views.user_login, name="user_login"),

    path('user_profile/', views.user_profile, name='user_profile'),
    path('user_profile_pic/<int:id>/',views.user_profile_pic,name="user_profile_pic"),
    path('update_user_profile/<int:id>/', views.update_user_profile, name='update_user_profile'),
    path('edit_user_profile/<int:id>/', views.edit_user_profile, name='edit_user_profile'),
    path('delete_user_profile/<int:id>/', views.delete_user_profile, name="delete_user_profile"),
    path('user_logout/', views.user_logout, name="user_logout"),

]