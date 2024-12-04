from django.shortcuts import render, redirect
from accounts.models import Blogger_register, User_register
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from App.models import Blogs, Comments, Likes



# Create your views here.
def index(request):
    return render(request, "index.html")

def blog_create(request):
    blogger_id = request.session.get('blogger_id')
    if not blogger_id:
        return redirect('/accounts/blogger_login/')
    try:
        blogger = Blogger_register.objects.get(id= blogger_id)
    except Blogger_register.DoesNotExist:
        return redirect('/accounts/blogger_register/')
    
    if request.method == "POST":
        observations = request.POST.get('observations')
        location = request.POST.get('location')
        image = request.FILES.get('image')

        print(f"Observations: {observations}, Location: {location}, Image: {image}")  # Debug line


        if not (observations and location and image):
            messages.error(request, "All fields are mandatory")
            return redirect('/blog_create/')
        blog_data = Blogs.objects.create(blogger = blogger, blog_image = image ,observations=observations, location = location )
        blog_data.save()
        return redirect('/my_blogs/')

    return render(request, "blog_create.html")


### Dispaly blogs ####################################################################
from django.utils import timezone
import pytz
                
def my_blogs(request):
    blogger_id = request.session.get('blogger_id')
    if not blogger_id:
        return redirect('/accounts/blogger_login/')
    try:
        blogger = Blogger_register.objects.get(id = blogger_id)
    except Blogger_register.DoesNotExist:
        return redirect('/accounts/blogger_register/')
    
    blogs = Blogs.objects.filter(blogger = blogger)
    local_tz = pytz.timezone('Asia/Kolkata')
    # for like count ###########
    for blog in blogs:
        print(f"Original UTC time: {blog.created_at}")
        
        blog.created_at = blog.created_at.astimezone(local_tz)
        print(f"Converted local time: {blog.created_at}")
        likes = Likes.objects.filter(blogs_toLike = blog).count()
        blog.likes_count = likes


        # Check if the blogger or user liked the blog
        blog.is_liked_by_user = Likes.objects.filter(blogs_toLike=blog, blogger=blogger).exists() if blogger else False
        blog.is_liked_by_user = Likes.objects.filter(blogs_toLike=blog, user=request.user).exists() if not blogger else blog.is_liked_by_user

        

    if not blogs:
        messages.info(request, "No blogs Posted")
        return render(request, "my_blogs.html", {'blogs':[]})
    

    return render(request, 'my_blogs.html', {'blogs':blogs, 'blogger':blogger})

### Delete Blog view ######################################################################################


def delete_blog(request, blog_id):
    blogger_id = request.session.get('blogger_id')
    if not blogger_id:
        return redirect('/accounts/blogger_login/')
    
    try:
        blogger = Blogger_register.objects.get(id = blogger_id)
    except Blogger_register.DoesNotExist:
        return redirect('/accounts/blogger_register/')
    
    blog = Blogs.objects.get(id=blog_id)

    if blog.blogger:
        blog.delete()
        return redirect('/my_blogs/')
    else:
        return redirect('/my_blogs/')





### Comment add view ########################################################################################


def blog_comment(request, id):
    blog = Blogs.objects.get(id=id)
    blogger_id = request.session.get('blogger_id')
    user_id = request.session.get('user_id')

    

    print(f"Session Data - Blogger ID: {blogger_id}, User ID: {user_id}")  #

    if not blogger_id and not user_id:
        messages.error(request, "You must be logged in to comment.")
        return redirect('/accounts/user_login/')  
    
    if blogger_id:
        try:
        
             blogger = Blogger_register.objects.get(id=blogger_id)
        except Blogger_register.DoesNotExist:
            return redirect('/accounts/blogger_register/')
    else:
        blogger = None


    if user_id:
        try:
            user = User_register.objects.get(id=user_id)
        except User_register.DoesNotExist:
            return redirect('/accounts/user_register/')
    else:
        user = None

    if request.method == "POST":
        
        comment_content = request.POST.get('comment_text')

      
        if comment_content:
            
            if blogger:
               
                comment_create = Comments(blogs_toComment=blog, blogger=blogger, comment=comment_content)
                comment_create.save()
                print(f"Comment created by blogger: {comment_create}")

            elif user:
                comment_create = Comments(blogs_toComment=blog, user=user, comment=comment_content)
                comment_create.save()
                print(f"Comment created by user: {comment_create}")
            messages.success(request, "Your comment has been posted!")
        else:
            messages.error(request, "You must enter a comment to post.")
    

    return redirect('/my_blogs/')



######## Edit Comment view ##########################################################################


def edit_comment(request, id):
    comment = Comments.objects.get(id = id)
    blogger_id = request.session.get('blogger_id')
    user_id = request.session.get('user_id')

   
    if not blogger_id and not user_id:
        messages.error(request, "You must be logged in to comment.")
        return redirect('/accounts/user_login/')  
    
    if blogger_id:
        try:
        
             blogger = Blogger_register.objects.get(id=blogger_id)
        except Blogger_register.DoesNotExist:
            return redirect('/accounts/blogger_register/')
    else:
        blogger = None


    if user_id:
        try:
            user = User_register.objects.get(id=user_id)
        except User_register.DoesNotExist:
            return redirect('/accounts/user_register/')
    else:
        user = None
    
    if request.method == "POST":
        edit_comment = request.POST.get('comment_text')

        if edit_comment:

            comment.comment = edit_comment
            comment.save()
            messages.success(request, "Comment updated successfully.")
            return redirect('/my_blogs/')
    return render(request, 'edit_comment.html', {'comment': comment})


#### Delete Comment view ############################################################################################

def delete_comment(request, id):

    try:
        comment = Comments.objects.get(id=id)
    except Comments.DoesNotExist:
        messages.error(request, "Comment not found.")
        return redirect('my_blog')  


    if request.session.get('user_id'):
        if comment.user.id != request.session.get('user_id'):
            messages.error(request, "You do not have permission to delete this comment.")
            return redirect('/my_blogs/') 
    elif request.session.get('blogger_id'):
        if comment.blogger.id != request.session.get('blogger_id'):
            messages.error(request, "You do not have permission to delete this comment.")
            return redirect('/my_blogs/')
        
    comment.delete()
    messages.success(request, "Comment deleted successfully.")
    return redirect('/my_blogs/')

 ### Like add View #####################################################################################################

def like_blog(request, id):
    blog = Blogs.objects.get(id = id)
    blogger_id = request.session.get('blogger_id')
    user_id = request.session.get('user_id')

    if not blogger_id and user_id:
        messages.info('you need to log in to like the post')
        return redirect('accounts/blogger_login/')
    
    
    if blogger_id:
        try:
            blogger = Blogger_register.objects.get(id = blogger_id)
        except Blogger_register.DoesNotExist:
            return redirect('/accounts/blogger_register/')
    else:
        blogger = None

    if user_id:
        try: 
            user = User_register.objects.get(id = user_id)
        except User_register.DoesNotExist:
            return redirect('/accounts/user_register/')
    else:
        user = None

    if blogger:
        like_check = Likes.objects.filter(blogs_toLike=blog, blogger=blogger).exists()
        if like_check:
            Likes.objects.filter(blogs_toLike=blog, blogger=blogger).delete()  # Unlike
        else:
            Likes.objects.create(blogs_toLike=blog, blogger=blogger, like=1)  # Like

    elif user:
        like_check = Likes.objects.filter(blogs_toLike=blog, user=user).exists()
        if like_check:
            Likes.objects.filter(blogs_toLike=blog, user=user).delete()  # Unlike
        else:
            Likes.objects.create(blogs_toLike=blog, user=user, like=1)  # Like

   
    return redirect("/my_blogs/")  
    


