
from django.shortcuts import redirect, render
from blog_main.forms import RegistrationForm
from blogs.models import Category,Blog

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