
from django.shortcuts import redirect, render
from blog_main.forms import RegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from blogs.models import Category,Blog
from django.contrib.auth import authenticate, login as auth_login ,logout as auth_logout
def home(request):
    categories = Category.objects.all()
    featured_post = Blog.objects.filter(is_featured = True,status ="Published").order_by('updated_at')
    posts = Blog.objects.filter(is_featured=False,status ="Published")
    
    context = {
        'categories':categories,
        'featured_post':featured_post,
        'posts':posts
    }

    return render(request,'home.html',context)


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            print(form.errors)
    else:
         form = RegistrationForm()
    context = {
        'form': form
    }
    return render(request,'register.html',context)

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()

    context = {
        'form': form
    }
    return render(request,'login.html',context)


def logout(request):
    auth_logout(request)
    return redirect('home')