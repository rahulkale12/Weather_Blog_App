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




# def blog_detail(request, blog_id):
#     blog = Blogs.objects.get(id=blog_id)

#     # Handle Like
#     if request.method == "POST" and 'like' in request.POST:
#         if request.user.is_authenticated:
#             if not Likes.objects.filter(blogs_toLike=blog, user=request.user).exists():
#                 Likes.objects.create(blogs_toLike=blog, user=request.user)
#                 messages.success(request, "You liked this blog.")
#             else:
#                 messages.error(request, "You have already liked this blog.")
#         else:
#             messages.error(request, "You need to be logged in to like this blog.")
#         return redirect('blog_detail', blog_id=blog.id)

#     # Handle Comment
#     if request.method == "POST" and 'comment' in request.POST:
#         comment_content = request.POST.get('comment_content')
#         if request.user.is_authenticated:
#             Comments.objects.create(blog=blog, comment=comment_content, user=request.user)
#             messages.success(request, "Comment added successfully!")
#         else:
#             messages.error(request, "You need to be logged in to comment.")
#         return redirect('blog_detail', blog_id=blog.id)

#     # Handle Comment Deletion
#     if request.method == "POST" and 'delete_comment' in request.POST:
#         comment_id = request.POST.get('comment_id')
#         comment = Comments.objects.get(id=comment_id)
#         if comment.user == request.user or comment.blogger == request.user:
#             comment.delete()
#             messages.success(request, "Comment deleted successfully.")
#         else:
#             messages.error(request, "You are not authorized to delete this comment.")
#         return redirect('blog_detail', blog_id=blog.id)

#     return render(request, "blog_detail.html", {'blog': blog})




# def blogs(request, blog_id):
#     blog = Blogs.objects.get(id=blog_id)
#     blogger_id = request.session.get('blogger_id')
#     user_id = request.session.get('user_id')

#     if not blogger_id:
#         return redirect('/accounts/blogger_login/')
#     elif not user_id:
#         return redirect('/accounts/user_login/')

#     try:
#         blogger = Blogger_register.objects.get(blogger=blogger_id)
#     except Blogger_register.DoesNotExist:
#         return redirect('/accounts/blogger_register/')

#     try:
#         user = User_register.objects.get(user=user_id)
#     except User_register.DoesNotExist:
#         return redirect('/accounts/user_register/')

#     if request.method == "POST":
#         # Handle Like
#         if 'like' in request.POST:
#             if user:
#                 # Check if the user has already liked the post
#                 like_exists = Likes.objects.filter(blogs_toLike=blog, user=user).exists()
#                 if not like_exists:
#                     Likes.objects.create(blogs_toLike=blog, user=user, like=1)
#                     messages.success(request, "You liked the blog!")
#                 else:
#                     messages.warning(request, "You have already liked this blog.")
#             elif blogger:
#                 # Check if the blogger has already liked the post
#                 like_exists = Likes.objects.filter(blogs_toLike=blog, blogger=blogger).exists()
#                 if not like_exists:
#                     Likes.objects.create(blogs_toLike=blog, blogger=blogger, like=1)
#                     messages.success(request, "You liked the blog!")
#                 else:
#                     messages.warning(request, "You have already liked this blog.")

#         # Handle Comment
#         elif 'comment' in request.POST:
#             comment_content = request.POST.get('comment')
#             if comment_content:
#                 if user:
#                     Comments.objects.create(blogs_toComment=blog, user=user, comment=comment_content)
#                     messages.success(request, "Comment added successfully!")
#                 elif blogger:
#                     Comments.objects.create(blogs_toComment=blog, blogger=blogger, comment=comment_content)
#                     messages.success(request, "Comment added successfully!")
#                 else:
#                     messages.error(request, "You must be logged in to comment.")

#         return redirect('blog_detail', blog_id=blog.id)

#     return render(request, 'blogs.html', {'blog': blog})

                
def my_blogs(request):
    blogger_id = request.session.get('blogger_id')
    if not blogger_id:
        return redirect('/accounts/blogger_login/')
    try:
        blogger = Blogger_register.objects.get(id = blogger_id)
    except Blogger_register.DoesNotExist:
        return redirect('/accounts/blogger_register/')
    
    blogs = Blogs.objects.filter(blogger = blogger)

    if not blogs:
        messages.info(request, "No blogs Posted")
        return render(request, "my_blogs.html", {'bogs':[]})

    return render(request, 'my_blogs.html', {'blogs':blogs})




def delete_blog(request, blog_id):
    try:
        blog = Blogs.objects.get(id=blog_id)
        blog.delete()
    except Blogs.DoesNotExist:
        return redirect('my_blogs')
    return redirect('my_blogs') 




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
