from django.shortcuts import render, redirect
from accounts.models import Blogger_register, User_register
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from App.models import Blogs, Comments, Likes
from django.utils import timezone
import pytz
            



# Create your views here.
def index(request):
    blogs = Blogs.objects.all()
    blogger_id = request.session.get('blogger_id')
    user_id = request.session.get('user_id')
    local_tz = pytz.timezone('Asia/Kolkata')

    # Check interactions for each blog
    for blog in blogs:
        blog.created_at = blog.created_at.astimezone(local_tz)
        blog.likes_count = Likes.objects.filter(blogs_toLike=blog).count()

        if blogger_id:  # If blogger is logged in
            blogger = Blogger_register.objects.get(id=blogger_id)
            blog.is_liked_by_user = Likes.objects.filter(blogs_toLike=blog, blogger=blogger).exists()
        elif user_id:  # If normal user is logged in
            user = User_register.objects.get(id=user_id)
            blog.is_liked_by_user = Likes.objects.filter(blogs_toLike=blog, user=user).exists()
        else:
            blog.is_liked_by_user = False

        blog.comments = Comments.objects.filter(blogs_toComment = blog)

    return render(request, "index.html", {"blogs": blogs})




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

        if not (observations and location and image):
            messages.error(request, "All fields are mandatory")
            return redirect('/blog_create/')
        blog_data = Blogs.objects.create(blogger = blogger, blog_image = image ,observations=observations, location = location )
        blog_data.save()
        return redirect('/my_blogs/')

    return render(request, "blog_create.html")


### Dispaly blogs ####################################################################
    
def my_blogs(request):
    blogger_id = request.session.get('blogger_id')
    if not blogger_id:
        return redirect('/')
    try:
        blogger = Blogger_register.objects.get(id = blogger_id)
    except Blogger_register.DoesNotExist:
        return redirect('/accounts/blogger_register/')
    
    blogs = Blogs.objects.filter(blogger = blogger)
    local_tz = pytz.timezone('Asia/Kolkata')


    # for like count ###########
    for blog in blogs:
        
        blog.created_at = blog.created_at.astimezone(local_tz)
        blog.likes_count = Likes.objects.filter(blogs_toLike = blog).count()
        blog.comments =  Comments.objects.filter(blogs_toComment = blog)


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

    if blogger_id is None and user_id is None:
        return redirect('/accounts/user_login/')  
    
    blogger = None
    user = None
    
    if blogger_id:
        try:
        
             blogger = Blogger_register.objects.get(id=blogger_id)
        except Blogger_register.DoesNotExist:
            return redirect('/accounts/blogger_register/')
    

    if user_id:
        try:
            user = User_register.objects.get(id=user_id)
        except User_register.DoesNotExist:
            return redirect('/accounts/user_register/')
   

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
                
            
        else:
            messages.error(request, "You must enter a comment to post.")
    

    return redirect('/')



######## Edit Comment view ##########################################################################


# def edit_comment(request, id):
#     comment = Comments.objects.get(id = id)
#     blogger_id = request.session.get('blogger_id')
#     user_id = request.session.get('user_id')

   
#     if not blogger_id and not user_id:
#         # messages.error(request, "You must be logged in to comment.")
#         return redirect('/accounts/user_login/')  
    
#     if blogger_id:
#         try:
        
#              blogger = Blogger_register.objects.get(id=blogger_id)
#         except Blogger_register.DoesNotExist:
#             return redirect('/accounts/blogger_register/')
#     else:
#         blogger = None


#     if user_id:
#         try:
#             user = User_register.objects.get(id=user_id)
#         except User_register.DoesNotExist:
#             return redirect('/accounts/user_register/')
#     else:
#         user = None
    
#     if request.method == "POST":
#         edit_comment = request.POST.get('comment_text')

#         if edit_comment:

#             comment.comment = edit_comment
#             comment.save()
#             messages.success(request, "Comment updated successfully.")
#             return redirect('/my_blogs/')
#     return render(request, 'edit_comment.html', {'comment': comment})


def edit_comment(request, id):
    try:
        comment = Comments.objects.get(id=id)
    except Comments.DoesNotExist:
        return redirect('/')

    blogger_id = request.session.get('blogger_id')
    user_id = request.session.get('user_id')

    if comment.user and comment.user.id != user_id:
        return redirect('/') 

    if comment.blogger and comment.blogger.id != blogger_id:
        return redirect('/') 


    if request.method == "POST":
        updated_text = request.POST.get('comment_text')
        if updated_text:
            comment.comment = updated_text
            comment.save()

            return redirect('/')


    return render(request, 'edit_comment.html', {'comment': comment})




#### Delete Comment view ############################################################################################

# def delete_comment(request, id):

#     try:
#         comment = Comments.objects.get(id=id)
#     except Comments.DoesNotExist:
#         # messages.error(request, "Comment not found.")
#         return redirect('my_blog')  


#     if request.session.get('user_id'):
#         if comment.user.id != request.session.get('user_id'):
#             messages.error(request, "You do not have permission to delete this comment.")
#             return redirect('/my_blogs/') 
#     elif request.session.get('blogger_id'):
#         if comment.blogger.id != request.session.get('blogger_id'):
#             messages.error(request, "You do not have permission to delete this comment.")
#             return redirect('/my_blogs/')
        
#     comment.delete()
#     messages.success(request, "Comment deleted successfully.")
#     return redirect('/my_blogs/')


def delete_comment(request, id):
    comment = Comments.objects.get(id=id)
    blogger_id = request.session.get('blogger_id')
    user_id = request.session.get('user_id')

    if user_id and comment.user and comment.user.id == user_id:
        comment.delete()

        return redirect('/')

    # Case 2: Blogger is logged in and wants to delete comments on their blog
    if blogger_id:
        # Check if the comment is associated with a valid blog and blogger
        if comment.blogs_toComment and comment.blogs_toComment.blogger and comment.blogs_toComment.blogger.id == blogger_id:
            comment.delete()

            return redirect('/')

    return redirect('/')


 ### Like add View #####################################################################################################

def like_blog(request, id):
    blog = Blogs.objects.get(id = id)
    blogger_id = request.session.get('blogger_id')
    user_id = request.session.get('user_id')

    if not user_id and not blogger_id:
        return redirect('/accounts/user_login/')  
    
    
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
            Likes.objects.create(blogs_toLike=blog, blogger=blogger, like=1)   # Like

    elif user:
        like_check = Likes.objects.filter(blogs_toLike=blog, user=user).exists()
        if like_check:
            Likes.objects.filter(blogs_toLike=blog, user=user).delete()  
        else:
            Likes.objects.create(blogs_toLike=blog, user=user, like=1)  

   
    return redirect("/my_blogs/")  
    


