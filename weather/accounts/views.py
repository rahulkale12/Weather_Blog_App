from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from accounts.models import Blogger_register, User_register
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

def blogger_register(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password == confirm_password:
            if Blogger_register.objects.filter(email=email).exists():
                messages.info(request, "Email ALready taken, please try with new email.")
                return redirect("/accounts/blogger_register/")  
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
                return redirect('blogger_profile/')
            else:
                messages.info(request, "Invalid Credentilas")
                return redirect('/accounts/blogger_login/')
        except ObjectDoesNotExist:
            messages.info(request, "Email Does Not Exist, Please Register")
            return render(request,'blogger_login.html')
    return render(request, "blogger_login.html")



def user_register(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password == confirm_password :
            if User_register.objects.filter(email=email).exists():
                messages.info(request, "Email already taken, Please try with new email. ")
                return redirect("/accounts/user_register/")
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
                return redirect("{% url static 'index %}")
            else:
                messages.info(request, "Invalid Credentials")
                return redirect("/accounts/user_login/")
        except ObjectDoesNotExist:
            messages.info(request, "Email does not exists , please register.")
            return redirect("/accounts/user_login/")
    return render(request, "user_login.html")