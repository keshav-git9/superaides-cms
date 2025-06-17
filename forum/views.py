# Create your views here.
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.shortcuts import render, get_object_or_404, redirect
from .models import ForumCategory, ForumPost, ForumReply
from .forms import ForumPostForm, ForumReplyForm
from django.contrib.auth.decorators import login_required


def forum_home(request):
    search_query = request.POST.get('q', '').strip()
    # Filter active categories
    categories = ForumCategory.objects.filter(status=True).annotate(post_count=Count('posts'))
    repost = ForumPost.objects.filter(status=True).order_by('-created_at')  
    # Apply search filter if a query is provided
    if search_query:
        categories = categories.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # Paginate the categories list
    paginator = Paginator(categories, 10)  # 10 categories per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'posts': repost,
        'search_query': search_query,
    }
    return render(request, 'forum/forum_home.html', context)

def forum_category(request, id):
    category = get_object_or_404(ForumCategory, id=id)
    posts = category.posts.filter(status=True)
    return render(request, 'forum/forum_category.html', {'category': category, 'posts': posts})



def forum_post_detail(request, id):
    post = get_object_or_404(ForumPost, id=id)
    replies = post.replies.all()
    if request.method == "POST":
        form = ForumReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.post = post
            reply.user = request.user
            reply.save()
            return redirect('forum_post_detail', id=post.id)
    else:
        form = ForumReplyForm()
    return render(request, 'forum/forum_post_detail.html', {'post': post, 'replies': replies, 'form': form})

@login_required
def forum_post_create(request):
    if request.method == "POST":
        form = ForumPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('forum_home')
    else:
        form = ForumPostForm()
    return render(request, 'forum/forum_post_create.html', {'form': form})
