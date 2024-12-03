from django.db import models
from accounts.models import Blogger_register, User_register

# Create your models here.
class Blogs(models.Model):
    blogger = models.ForeignKey(Blogger_register, on_delete=models.CASCADE)
    blog_image = models.ImageField(upload_to='blogImage/')
    observations = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"blog by {self.blogger}  - {self.observations[:10]}"


class Comments(models.Model):
    blogs_toComment = models.ForeignKey(Blogs, on_delete=models.CASCADE)
    comment = models.CharField(max_length=100)
    user = models.ForeignKey(User_register, on_delete=models.CASCADE,  null=True, blank=True)
    blogger = models.ForeignKey(Blogger_register, on_delete=models.CASCADE,  null=True, blank=True)


class Likes(models.Model):
    blogs_toLike = models.ForeignKey(Blogs, on_delete=models.CASCADE)
    like = models.IntegerField()
    user = models.ForeignKey(User_register, on_delete=models.CASCADE,  null=True, blank=True)
    blogger = models.ForeignKey(Blogger_register, on_delete=models.CASCADE,  null=True, blank=True)
