from django.contrib import messages
from django.utils.timezone import now
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db.models import Q,Count
from django.http import Http404
from django.http import HttpResponse, JsonResponse,Http404
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt 
from backend.models import Html,Cms_setting,Pages,Navigroups,Navigroupspages,Contactus,Post,Category,Tag,CustomUser,Testimonial,Comment
from .forms import ContactusForm,CommentForm
from django.contrib.auth.models import Group
from django.contrib import messages
from django.views.decorators.http import require_POST


def frontend_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to dashboard or home
        else:
            messages.error(request, 'Invalid email or password.')
    return render(request, 'login.html')

def frontend_logout(request):
    logout(request)
    return redirect('frontend_login')

def frontend_register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        group_id = request.POST.get('group')  # If assigning a group
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
        else:
            user = CustomUser.objects.create_user(email=email, name=name, password=password)
            if group_id:
                group = Group.objects.get(id=group_id)
                user.groups.add(group)
            messages.success(request, 'Registration successful. Please login.')
            return redirect('frontend_login')
    groups = Group.objects.all()
    return render(request, 'register.html', {'groups': groups})



# Create your views here.
def home(request):
    testimonials = Testimonial.objects.filter(is_approved=True)
    return render(request, 'index.html', {'testimonials': testimonials})



def index(request, code="", para=""):
    if not code:  
        return redirect('home') 
    # Define a dictionary mapping code values to functions
    function_map = {
        'contactus': _contactus,
        'aboutus': _aboutus,
        'vision': _vision,        
    }

    if code in function_map:
        return function_map[code](request, para)

    # If the page is dynamic (not predefined)
    #print(code)
    page_content = get_page_content(code) 
    if not page_content:
        return render(request, '404.html', status=404)  # Custom 404 page
    return render(request, 'cms_master.html', {'page_content': page_content})


# Example Functions (replace with real implementations)
def _aboutus(request, para=""):
    return render(request, 'aboutus.html')

def _vision(request, para=""):
    return render(request, 'vision.html')


def _contactus(request, para=""):    
    if request.method == 'POST':
        form = ContactusForm(request.POST)
        #print(request.POST)        
        if form.is_valid():
            form.save()
            name = form.cleaned_data['fullname']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            # Send email
            subject = f"Message from {name}"
            message_body = f"Name: {name}\nEmail: {email}\nMessage: {message}"
            from_email = settings.EMAIL_HOST_USER  # The sender email
            
            # Send the email
            send_mail(
                subject,
                message_body,
                from_email,
                ['satya.prakash434@gmail.com'],  # Recipient email
                fail_silently=False
            )

            msg = {'response': 'success', 'title':'Data Saved!', 'icon':'success',  'msg': 'Your data has been successfully saved.'}
        else:
            #print(form.errors)
            errors = form.errors.as_json()
            msg = {'response': 'notSaved', 'title':'Not Saved!', 'icon':'error', 'msg': 'Your data has not been saved. Please try again.','errors': errors}
            
        return JsonResponse(msg, safe=True)

    else:
        form = ContactusForm()

    return render(request, 'contact.html', {'form': form})

def get_page_content(code):
    try:
        # Query the page content from the database based on the 'code'
        content = Pages.objects.filter(url=code).first()       
        return content
    except Pages.DoesNotExist:
        # Return None or some default message if the page is not found
        return None


#saperate work for blog post comments.
#def blog_list(request):
   # posts = Post.objects.filter(status=True).order_by('-published_at')
   # categories = Category.objects.annotate(post_count=Count('posts')).order_by('-id')
   # return render(request, 'blog_list.html', {'posts': posts,'categories': categories})


def blog_list(request):
    search_key = request.POST.get('search_key', '').strip()

    tags = Tag.objects.annotate(post_count=Count('posts')).filter(posts__status=True).distinct()

    # Annotate posts with count of approved comments only
    post_list = Post.objects.filter(status=True).annotate(
        comment_count=Count('comments', filter=Q(comments__is_approved=True))
    ).order_by('-published_at')

    if search_key:
        post_list = post_list.filter(
            Q(title__startswith=search_key) | Q(slug__endswith=search_key)
        )

    paginator = Paginator(post_list, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.annotate(post_count=Count('posts')).order_by('-id')

    return render(request, 'blog_list.html', {
        'posts': post_list,
        'tags': tags,
        'page_obj': page_obj,
        'categories': categories,
        'search_key': search_key
    })

def get_client_ip(request):
    """ Utility to get the client's IP address. """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status=True)
    comments = post.comments.filter(is_approved=True).order_by('-created_at')
    ip_address = get_client_ip(request)
    today = now().date()

    if request.method == 'POST':
        comment_count = Comment.objects.filter(
            ip_address=ip_address,
            created_at__date=today
        ).count()

        form = CommentForm(request.POST)
        
        if comment_count >= 5:
            messages.error(request, 'You have reached the daily comment limit (5 per day).')
            return redirect(request.path_info)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.is_approved = 0
            comment.ip_address = ip_address
            comment.save()
            messages.success(request, 'Your comment has been submitted and is pending approval.')
            return redirect(request.path_info)
        else:
            messages.error(request, 'There was an error submitting your comment. Please check the form.')

    else:
        form = CommentForm()

    tags = Tag.objects.annotate(post_count=Count('posts')).filter(posts__status=True).distinct()
    post_list = Post.objects.filter(status=True).order_by('-published_at')
    categories = Category.objects.annotate(post_count=Count('posts')).order_by('-id')

    return render(request, 'post_detail.html', {
        'post': post,
        'tags': tags,
        'posts': post_list,
        'categories': categories,
        'comments': comments,
        'form': form,
    })



@csrf_exempt  # or use CSRF token in your JS
def like_post(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post = Post.objects.get(id=post_id)
        post.likes += 1
        post.save()
        return JsonResponse({'likes': post.likes})
    return JsonResponse({'error': 'Invalid request'}, status=400)



def category_posts(request, slug):
    search_key = request.POST.get('search_key', '').strip()  # Get search query from POST request 
    category = get_object_or_404(Category, slug=slug)
    tags = Tag.objects.annotate(post_count=Count('posts')).filter(posts__status=True).distinct()
    #post_list = Post.objects.filter(category=category, status=True).order_by('-published_at')

    post_list = Post.objects.filter(category=category,status=True).annotate(
        comment_count=Count('comments', filter=Q(comments__is_approved=True))
    ).order_by('-published_at')

    if search_key:
        post_list = post_list.filter(           
            (Q(title__startswith=search_key) | Q(slug__endswith=search_key))
        )      
    paginator = Paginator(post_list, 2)  # Show 5 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    categories = Category.objects.annotate(post_count=Count('posts')).order_by('-id')
    return render(request, 'category_posts.html', {
        'category': category,
        'posts': post_list,
        'tags':tags,
        'page_obj': page_obj,
        'categories': categories,
        'search_key': search_key
    })

def sitemap(request):
    return HttpResponse(open("sitemap.xml").read(), content_type="text/xml")
    



@require_POST
@csrf_exempt  # Optional if CSRF token is sent properly
def send_email_loudoun(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    loudounzip = request.POST.get('loudounzip')   

    subject = f"Message from {name}"
    full_message = f" Name : {name} \n\n Email : {email} \n\n This is your location :{loudounzip} \n\n\n\n Regards : SuperAides"
    try:      
        send_mail(
            subject,
            full_message,
            'info@superaides.com',  # From
            ['satya.prakash@pranathiss.com'],  # To
            fail_silently=False,
        )        
        return JsonResponse({'message': 'Email sent successfully!'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    

@require_POST
@csrf_exempt  # Optional if CSRF token is sent properly
def send_email_fairfax(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    fairfaxzip = request.POST.get('fairfaxzip')   

    subject = f"Message from {name}"
    full_message = f" Name : {name} \n\n Email : {email} \n\n This is your location :{fairfaxzip} \n\n\n\n Regards : SuperAides"
    try:      
        send_mail(
            subject,
            full_message,
            'info@superaides.com',  # From
            ['satya.prakash@pranathiss.com'],  # To
            fail_silently=False,
        )        
        return JsonResponse({'message': 'Email sent successfully!'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    


#=============================================================
def custom_404(request, exception):
    return render(request, '404.html', status=404)