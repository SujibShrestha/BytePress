from django.shortcuts import get_object_or_404, render,redirect
from django.http import HttpResponse
from django.db.models import Q
from .models import Blog, Category

# Create your views here.
def search(request):
    query = request.GET.get('q', '').strip()
    posts = Blog.objects.none()
    if query:
        posts = Blog.objects.filter(status='Published').filter(
            Q(title__icontains=query)
            | Q(short_description__icontains=query)
            | Q(blog_body__icontains=query)
        ).order_by('-created_at')
    return render(request, 'search.html', {'query': query, 'posts': posts})


def posts_by_category(request,category_id):
    posts = Blog.objects.filter(status='Published',category=category_id)
    try:
        category = Category.objects.get(pk=category_id)
    except Category.DoesNotExist:
        return redirect('home')
    context = {
        'posts':posts,
        'category': category
    }
    return render(request,'posts_by_category.html',context)


def blogs(request,slug):
    single_blog = get_object_or_404(Blog,slug=slug,status='Published')
    context = {
        'single_blog':single_blog
    }
    return render(request,'blogs.html',context)


def search(request):
    keyword = request.GET.get('q')
    if keyword:
        blogs = Blog.objects.filter(Q(title__icontains=keyword) | Q(short_description__icontains=keyword) | Q(blog_body__icontains=keyword), status='Published')

    context = {
        'blogs': blogs,
    }
    return render(request,'search.html',context)