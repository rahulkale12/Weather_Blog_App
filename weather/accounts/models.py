from django.db import models

# Create your models here.
class Blogger_register(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)

class User_register(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)


class Blogger_profile_picture(models.Model):
    blogger = models.ForeignKey(Blogger_register, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to="BloggerProfileImage/")

class User_profile_picture(models.Model):
    user = models.ForeignKey(User_register, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to="UserProfileImage/")