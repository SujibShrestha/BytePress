from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from blogs.models import Blog

# Create your views here.

@login_required(login_url='login')
def dashboard(request):
    posts = Blog.objects.filter(author=request.user)
    context = posts.aggregate(
        total_posts=Count('id'),
        published_posts=Count('id', filter=Q(status='Published')),
        draft_posts=Count('id', filter=Q(status='Draft')),
    )
    context['recent_posts'] = posts.select_related('category').order_by('-updated_at')[:5]
    return render(request, 'dashboard/dashboard.html', context)
