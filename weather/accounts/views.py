from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from accounts.models import Blogger_register, User_register, Blogger_profile_picture,User_profile_picture
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.validators import validate_email
# Create your views here.

### blogger view starts here #####################################################################################


def blogger_register(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Invalid email format. Please enter a valid email.")
            return render(request, "blogger_register.html")
        

        if password == confirm_password:
            if Blogger_register.objects.filter(email=email).exists():
                messages.info(request, "Email ALready taken, please try with new email.")
                return render(request, "blogger_register.html")  
            else:
                password = make_password(password)
                blogger = Blogger_register.objects.create(name=name, email=email, password=password)      
                blogger.save()
                return redirect('/accounts/blogger_login/')    
        messages.info(request, "confirm Password didn't match")
        return render(request, "blogger_register.html")
    return render(request, "blogger_register.html")


def blogger_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            blogger = Blogger_register.objects.get(email=email)
            if blogger.email == email and check_password(password, blogger.password):
                request.session['blogger_id'] = blogger.id
                return redirect('/accounts/blogger_profile/')
            else:
                messages.info(request, "Invalid Credentilas")
                return redirect('/accounts/blogger_login/')
        except ObjectDoesNotExist:
            messages.info(request, "Email Does Not Exist, Please Register")
            return render(request,'blogger_login.html')
    return render(request, "blogger_login.html")


def blogger_profile_pic(request,id):
    if request.method == "POST":
        blogger_pic = request.FILES.get('blogger_profile_pic')
        blogger_id = request.session.get('blogger_id')
        if not blogger_id:
           return redirect('/accounts/blogger_login/')
        try:
           blogger = Blogger_register.objects.get(id = blogger_id)
           if Blogger_profile_picture.objects.filter(blogger = blogger).exists():
               image = Blogger_profile_picture.objects.get(blogger= blogger)
               image.profile_image = blogger_pic
               image.save()
               return redirect('/accounts/blogger_profile/')
           else:
               new_create = Blogger_profile_picture.objects.create(blogger = blogger, profile_image = blogger_pic)
               new_create.save()
               return redirect('/accounts/blogger_profile/')
        except Blogger_register.DoesNotExist:
           return redirect('/accounts/blogger_register/')
    return render(request,"blogger_profile.html" )
           
 

def blogger_profile(request):
    blogger_id = request.session.get('blogger_id')

    if not blogger_id:
        return redirect('/accounts/blogger_login/')
    
    try:
        blogger = Blogger_register.objects.get(id = blogger_id)
    except Blogger_register.DoesNotExist:
        return redirect('/accounts/blogger_register/')
    
    try: 
        profile_pic = Blogger_profile_picture.objects.get(blogger = blogger)
        return render(request, 'blogger_profile.html', {'blogger':blogger, 'profile_pic':profile_pic})
    except Blogger_profile_picture.DoesNotExist:
        return render(request, "blogger_profile.html",{'blogger':blogger})


def update_blogger_profile(request,id):
    blogger_id = request.session.get('blogger_id')
    if not blogger_id:
        return redirect('/accounts/blogger_login/')
  
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')

        try:
            blogger = Blogger_register.objects.get(id = id)
            blogger.name = name
            blogger.email = email
            blogger.save()
            return redirect('/accounts/blogger_profile/')
        except Blogger_register.DoesNotExist:
            return redirect('/accounts/blogger_register/')
    return render(request, "blogger_profile.html")
    
            
def edit_blogger_profile(request,id):
    try:
        blogger = Blogger_register.objects.get(id = id)
    except Blogger_register.DoesNotExist:
         return redirect('/accounts/blogger_register/')
    return render(request, "blogger_profile.html", {"blogger":blogger})


def delete_blogger_profile(request, id):
    blogger = Blogger_register.objects.get(id = id)
    blogger.delete()
    return redirect('/accounts/blogger_login/')


def blogger_logout(request):
    blogger = request.session.get('blogger_id')
    request.session.flush()
    return redirect('/accounts/blogger_login/')


##### User view starts here #################################################



def user_register(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Invalid email format. Please enter a valid email.")
            return render(request, "user_register.html")
        

        if password == confirm_password :
            if User_register.objects.filter(email=email).exists():
                messages.info(request, "Email already taken, Please try with new email. ")
                return render(request, "user_register.html")
            else:
                password = make_password(password)
                user = User_register.objects.create(name = name , email = email, password = password)
                user.save()
                return redirect("/accounts/user_login/")
        messages.info(request, "Password didn't match.")

    return render(request, 'user_register.html')



def user_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User_register.objects.get(email=email)
            if user.email == email and check_password(password, user.password):
                request.session['user_id'] =user.id
                return redirect("/accounts/user_profile/")
            else:
                messages.info(request, "Invalid Credentials")
                return redirect("/accounts/user_login/")
        except ObjectDoesNotExist:
            messages.info(request, "Email does not exists , please register.")
            return redirect("/accounts/user_login/")
    return render(request, "user_login.html")


   


def user_profile_pic(request,id):
    if request.method == "POST":
        user_pic = request.FILES.get('user_profile_pic')
        user_id = request.session.get('user_id')
        if not user_id:
           return redirect('/accounts/user_login/')
        try:
           user = User_register.objects.get(id = user_id)
           if User_profile_picture.objects.filter(user = user).exists():
               image = User_profile_picture.objects.get(user = user)
               image.profile_image = user_pic
               image.save()
               return redirect('/accounts/blogger_profile/')
           else:
               new_create = User_profile_picture.objects.create(user = user, profile_image = user_pic)
               new_create.save()
               return redirect('/accounts/user_profile/')
        except User_register.DoesNotExist:
           return redirect('/accounts/user_register/')
    return render(request,"user_profile.html" )
           
 


def user_profile(request):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('/accounts/user_login/')
    
    try:
        user = User_register.objects.get(id = user_id)
    except User_register.DoesNotExist:
        return redirect('/accounts/user_register/')
    
    try: 
        profile_pic = User_profile_picture.objects.get(user = user)
        return render(request, 'user_profile.html', {'user':user, 'profile_pic':profile_pic})
    except User_profile_picture.DoesNotExist:
        return render(request, "user_profile.html",{'user':user})
    


    

def update_user_profile(request,id):
    blogger_id = request.session.get('user_id')
    if not blogger_id:
        return redirect('/accounts/user_login/')
  
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')

        try:
            blogger = User_register.objects.get(id = id)
            blogger.name = name
            blogger.email = email
            blogger.save()
            return redirect('/accounts/user_profile/')
        except User_register.DoesNotExist:
            return redirect('/accounts/user_register/')
    return render(request, "user_profile.html")
    
            
def edit_user_profile(request,id):
    try:
        user = User_register.objects.get(id = id)
    except User_register.DoesNotExist:
         return redirect('/accounts/blogger_register/')
    return render(request, "user_profile.html", {"user": user})


def delete_user_profile(request, id):
    user = User_register.objects.get(id = id)
    user.delete()
    return redirect('/accounts/user_login/')


def user_logout(request):
    user = request.session.get('user_id')
    request.session.flush()
    return redirect('/accounts/user_login/')



####################################################################################################################