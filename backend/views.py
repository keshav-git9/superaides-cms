from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .seo_tools import get_google_search_console_data, get_seo_keywords_from_meta
from django.core.mail import send_mail,EmailMessage
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse,Http404
from django.core.paginator import Paginator
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, logout
from .middlewares import auth, guest
from django.contrib.auth import get_user_model
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt 
from django.contrib import messages
from django.db.models import Q, Count
from .models import Html,Cms_setting,Pages,Navigroups,Navigroupspages,Contactus,Post,Category,Comment,Tag,CustomUser,Testimonial
from django.contrib.auth.models import Group, Permission
from django.urls import reverse
import re

from .forms import (HtmlForm,logoandfavicon,socialmediapages,googlerecaptcha,googleanalytic,UserEditForm,AuthenticationFormWithCaptcha,
                    sociallogin,facebookpixel,PageForm,NavigroupForm,NavigrouppageForm,PostForm,CategoryForm,TagForm,GroupForm,RegisterForm,TestimonialForm)
#Html,
User = get_user_model()
# Create your views here.


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('dashboard')
    else:
        initial_data = {'username':'', 'password1':'','password2':""}
        form = UserCreationForm(initial=initial_data)
    return render(request, 'auth/register.html',{'form':form})


def forgot_password_view(request):    
    return render(request, 'auth/forgot_password.html')



def login_view(request):
    error_message = ""
    if request.method == 'POST':
        remember_me = request.POST.get('remember_me')
        if not remember_me:
            request.session.set_expiry(0)
        else:
            request.session.set_expiry(604800)

        form = AuthenticationFormWithCaptcha(request, data=request.POST)
        
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
        else:
            error_message = "Invalid username, password, or CAPTCHA."
    else:
        form = AuthenticationFormWithCaptcha()
    
    return render(request, 'auth/login.html', {'form': form, 'error_message': error_message})





def login_view_ssssss(request):
    if request.method == 'POST':
        remember_me = request.POST.get('remember_me')
        if not remember_me:
            request.session.set_expiry(0)  # Session expires when the browser closes
        else:
            # Optional: Set session expiry time (e.g., 1 week)
            request.session.set_expiry(604800)  # 7 days in seconds

        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect('dashboard')
    else:
        initial_data = {'username':'', 'password':''}
        form = AuthenticationForm(initial=initial_data)
    return render(request, 'auth/login.html',{'form':form}) 

@auth
@csrf_exempt
def dashboard_view(request):
    if request.user.groups.filter(name="Admin").exists():
        #return HttpResponse("Welcome Admin!")
        #return render(request, 'dashboard.html')
        return redirect('list-html')
    elif request.user.groups.filter(name="Manager").exists():
        #return HttpResponse("Welcome Manager!")
        #return render(request, 'dashboard.html')
        return redirect('list-html')
    elif request.user.groups.filter(name="Editor").exists():
        return HttpResponse("Welcome Editor!")
    else:
        return HttpResponse("Welcome User!")   


#************Start html form add edit and list view html form **********************

@auth
@csrf_exempt
def listHtml_view(request):
    search_key = ""
    page_number = request.GET.get('page', 1)  # Get page number    
    per_page = 10  # Number of entries per page
    if request.method == "POST":
        search_key = request.POST.get('search_key', '').strip()  # Get search query from POST request
    # Query with LIKE and Aggregation
    queryset = Html.objects.all()
    if search_key:
        queryset = queryset.filter(
            #Q(title=search_key) | Q(code=search_key)
            Q(title__startswith=search_key) | Q(code__endswith=search_key)
        )
    # Count total results found
    total_results = queryset.aggregate(count=Count('id'))['count']
    # Pagination (10 results per page)
    paginator = Paginator(queryset.order_by('-id'), 10)
    page_obj = paginator.get_page(page_number)
    # Calculate "Showing X to Y of Z Entries"
    start_index = (page_obj.number - 1) * per_page + 1
    end_index = start_index + len(page_obj) - 1
    return render(request, 'list_html.html', {
        'page_obj': page_obj,
        'search_key': search_key,
        'total_results': total_results,
        'start_index': start_index,
        'end_index': end_index,
    })

@auth
@csrf_exempt
def addhtml_view(request):
    if request.method == 'POST':
        form = HtmlForm(request.POST)        
        if form.is_valid():                    
                code = form.cleaned_data.get('code')  # Replace with your field
                if Html.objects.filter(code=code).exists():
                    msg = { 'response': 'notSaved','title': 'Duplicate Entry!',  'icon': 'warning', 'msg': 'This code already exists.'}
                else:
                    form.save()
                    msg = {'response': 'success', 'title':'Data Saved!', 'icon':'success',  'msg': 'Your data has been successfully saved.'}          
        
        else:
            #print(form.errors)
            errors = form.errors.as_json()
            msg = {'response': 'notSaved', 'title':'Not Saved!', 'icon':'error', 'msg': 'Your data has not been saved. Please try again.','errors': errors}
        return JsonResponse(msg, safe=True)
    else:
        form = HtmlForm()
    return render(request, 'addhtml.html', {'form': form})


@auth
@csrf_exempt
def edithtml_view(request, id):   
    item = get_object_or_404(Html, id=id) 
    #data = Html.objects.filter(id=id).first()         
    if request.method == "POST":       
        form = HtmlForm(request.POST, instance=item)
        if form.is_valid():
                code = form.cleaned_data.get('code')  # Replace with your unique field
                # Check if another object (not the current one) has the same title
                if(Html.objects.filter(code=code).exclude(id=item.id).exists()):
                    msg = { 'response': 'notSaved','title': 'Duplicate Entry!','icon': 'warning','msg': 'A record with this code already exists.'}
                else:
                    form.save()
                    smsg = {'response': 'success', 'title':'Data Saved!', 'icon':'success',  'msg': 'Your data has been successfully update.'}              
                # form.save()
                #messages.success(request, "Record update successfully!")
            
        else:
            errors = form.errors.as_json()
            msg = {'response': 'notSaved', 'title':'Not Saved!', 'icon':'error', 'msg': 'Your data has not been update. Please try again.','errors': errors}
        
        return JsonResponse(msg, safe=True)    
        #return redirect('list-html')  # Redirect to the list page after updating
    else:
        form = HtmlForm(instance=item)
    return render(request, 'addhtml.html', {'data': item,'form': form})


@auth
@csrf_exempt  # Only for quick testing — use CSRF protection in production
def change_html_status(request):
    if request.method == "POST":
        try:
            post_id = int(request.POST.get('post_id'))
            status = request.POST.get('status') == '1'
            comment = Html.objects.get(id=post_id)
            comment.status = status
            comment.save()
            #return JsonResponse({'success': True, 'status': status})
            msg = {'response': 'success', 'title':'Data Saved!', 'icon':'success',  'msg': 'Your data has been successfully update.'}
            return JsonResponse(msg, safe=True) 
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request'})


@auth
@csrf_exempt
def delete_html(request):
    if request.method == 'POST':
        post_id = request.POST.get('id')
        try:
            post = Html.objects.get(id=post_id)
            post.delete()
            return JsonResponse({'status': 'success'})
            #msg = {'response': 'success', 'title':'Data Delete!', 'icon':'success',  'msg': 'Your data has been successfully Delete.'}
            #return JsonResponse(msg, safe=True) 
        except Post.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Post not found'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

#************Start pages form add edit and list view pages form **********************
@auth
@csrf_exempt
def pagelist(request):
    search_key = ""
    page_number = request.GET.get('page', 1)  # Get page number    
    per_page = 10  # Number of entries per page
    if request.method == "POST":
        search_key = request.POST.get('search_key', '').strip()  # Get search query from POST request
    # Query with LIKE and Aggregation
    queryset = Pages.objects.all()
    if search_key:
        queryset = queryset.filter(
            #Q(title=search_key) | Q(code=search_key)
            Q(title__startswith=search_key) | Q(code__endswith=search_key)
        )
    # Count total results found
    total_results = queryset.aggregate(count=Count('id'))['count']
    # Pagination (10 results per page)
    paginator = Paginator(queryset.order_by('-id'), 10)
    page_obj = paginator.get_page(page_number)
    # Calculate "Showing X to Y of Z Entries"
    start_index = (page_obj.number - 1) * per_page + 1
    end_index = start_index + len(page_obj) - 1
    return render(request, 'page_list.html', {
        'page_obj': page_obj,
        'search_key': search_key,
        'total_results': total_results,
        'start_index': start_index,
        'end_index': end_index,
    })


@auth
@csrf_exempt
def page_add(request):
    if request.method == 'POST':
        allData = request.POST
        allFiles = request.FILES                
        form = PageForm(data=allData, files=allFiles) 
        #form = PageForm(request.POST)                
        if form.is_valid():
                code = form.cleaned_data.get('code')  # Replace with your field
                if Pages.objects.filter(code=code).exists():
                    msg = { 'response': 'notSaved','title': 'Duplicate Entry!',  'icon': 'warning', 'msg': 'This code already exists.'}
                else:
                    form.save()
                    msg = {'response': 'success', 'title':'Data Saved!', 'icon':'success',  'msg': 'Your data has been successfully saved.'}  
                    #form.save()
                    #msg = {'response': 'success', 'title':'Data Saved!', 'icon':'success',  'msg': 'Your data has been successfully saved.'}
        else:
            #print(form.errors)
            errors = form.errors.as_json()
            msg = {'response': 'notSaved', 'title':'Not Saved!', 'icon':'error', 'msg': 'Your data has not been saved. Please try again.','errors': errors}
            
        return JsonResponse(msg, safe=True)

    else:
        form = PageForm()
    return render(request, 'page_add.html', {'form': form,'request': request})


@auth
@csrf_exempt
def page_edit(request, id):   
    item = get_object_or_404(Pages, id=id) 
    data = Pages.objects.filter(id=id).first()         
    if request.method == "POST":       
        form = PageForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
                code = form.cleaned_data.get('code')  # Replace with your unique field
                # Check if another object (not the current one) has the same title
                if(Pages.objects.filter(code=code).exclude(id=item.id).exists()):
                    msg = { 'response': 'notSaved','title': 'Duplicate Entry!','icon': 'warning','msg': 'A record with this code already exists.'}
                else:
                    form.save()
                    msg = {'response': 'success', 'title':'Data Saved!', 'icon':'success',  'msg': 'Your data has been successfully update.'}   
                        
        else:
            errors = form.errors.as_json()
            msg = {'response': 'notSaved', 'title':'Not Saved!', 'icon':'error', 'msg': 'Your data has not been update. Please try again.','errors': errors}
        
        return JsonResponse(msg, safe=True)    
        #return redirect('list-html')  # Redirect to the list page after updating
    else:
        form = PageForm(instance=item)
    return render(request, 'page_add.html', {'data': data,'form': form})

@auth
@csrf_exempt  # Only for quick testing — use CSRF protection in production
def change_page_status(request):
    if request.method == "POST":
        try:
            post_id = int(request.POST.get('post_id'))
            status = request.POST.get('status') == '1'
            comment = Pages.objects.get(id=post_id)
            comment.status = status
            comment.save()            
            msg = {'response': 'success', 'title':'Data Saved!', 'icon':'success',  'msg': 'Your data has been successfully update.'}
            return JsonResponse(msg, safe=True) 
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request'})


@auth
@csrf_exempt
def delete_page(request):
    if request.method == 'POST':
        post_id = request.POST.get('id')
        try:
            post = Pages.objects.get(id=post_id)
            post.delete()
            return JsonResponse({'status': 'success'})            
        except Post.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Post not found'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})





def generate_unique_slug(title):
    """Generates a unique slug by removing special characters and handling duplicates"""
    title_slug = re.sub(r'[^a-zA-Z0-9\-]', '-', title)    # Clean title

    # If the slug exists, append a number and check again
    if Pages.objects.filter(title=title_slug).exists():
        return generate_unique_slug(f"{title_slug}{random.randint(1, 100)}")
    
    return title_slug


def find_page_title(request):
    """AJAX View to return a unique slug based on the title"""
    title = request.GET.get("title", "").strip()  # Get title from query params
    if not title:
        return JsonResponse({"error": "Title is required"}, status=400)

    unique_slug = generate_unique_slug(title)    
    return JsonResponse({"slug": unique_slug})

#************end pages form add edit and list view pages form **********************
#************Start Navigroups form add edit and list view Navigroups form **********************

@auth
@csrf_exempt
def navigroup(request):
    search_key = ""
    page_number = request.GET.get('page', 1)  # Get page number    
    per_page = 10  # Number of entries per page
    if request.method == "POST":
        search_key = request.POST.get('search_key', '').strip()  # Get search query from POST request
    # Query with LIKE and Aggregation
    queryset = Navigroups.objects.all()
    if search_key:
        queryset = queryset.filter(
            #Q(title=search_key) | Q(code=search_key)
            Q(title__startswith=search_key) | Q(code__endswith=search_key)
        )
    # Count total results found
    total_results = queryset.aggregate(count=Count('id'))['count']
    # Pagination (10 results per page)
    paginator = Paginator(queryset.order_by('-id'), 10)
    page_obj = paginator.get_page(page_number)
    # Calculate "Showing X to Y of Z Entries"
    start_index = (page_obj.number - 1) * per_page + 1
    end_index = start_index + len(page_obj) - 1
    return render(request, 'navi_group_list.html', {
        'page_obj': page_obj,
        'search_key': search_key,
        'total_results': total_results,
        'start_index': start_index,
        'end_index': end_index,
    })

@auth
@csrf_exempt
def navigroup_add(request):
    if request.method == 'POST':
        form = NavigroupForm(request.POST)       
        if form.is_valid():
            form.save()
            msg = {'response': 'success', 'title':'Data Saved!', 'icon':'success',  'msg': 'Your data has been successfully saved.'}
        else:
            #print(form.errors)
            errors = form.errors.as_json()
            msg = {'response': 'notSaved', 'title':'Not Saved!', 'icon':'error', 'msg': 'Your data has not been saved. Please try again.','errors': errors}
            
        return JsonResponse(msg, safe=True)

    else:
        form = NavigroupForm()
    return render(request, 'navi_group_add.html', {'form': form})


@auth
@csrf_exempt
def navigroups_edit(request, id):   
    item = get_object_or_404(Navigroups, id=id) 
    data = Navigroups.objects.filter(id=id).first()         
    if request.method == "POST":       
        form = NavigroupForm(request.POST, instance=item)
        if form.is_valid():
            form.save()           
            msg = {'response': 'success', 'title':'Data Saved!', 'icon':'success',  'msg': 'Your data has been successfully update.'}
        else:
            errors = form.errors.as_json()
            msg = {'response': 'notSaved', 'title':'Not Saved!', 'icon':'error', 'msg': 'Your data has not been update. Please try again.','errors': errors}
        
        return JsonResponse(msg, safe=True)           
    else:
        form = NavigroupForm(instance=item)
    return render(request, 'navi_group_add.html', {'data': data,'form': form})



@auth
@csrf_exempt  # Only for quick testing — use CSRF protection in production
def change_navig_status(request):
    if request.method == "POST":
        try:
            navi_id = int(request.POST.get('post_id'))
            status = request.POST.get('status') == '1'
            comment = Navigroups.objects.get(id=navi_id)
            comment.status = status
            comment.save()            
            msg = {'response': 'success', 'title':'Data Saved!', 'icon':'success',  'msg': 'Your data has been successfully update.'}
            return JsonResponse(msg, safe=True) 
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request'})

#************Start html form add edit and list view html form **********************

@auth
@csrf_exempt
def navigrouppage(request, nid):
    search_key = ""
    page_number = request.GET.get('page', 1)  # Get page number    
    per_page = 10  # Number of entries per page
    if request.method == "POST":
        search_key = request.POST.get('search_key', '').strip()  # Get search query from POST request
    # Query with LIKE and Aggregation
    #queryset = Navigroupspages.objects.all()
    queryset = Navigroupspages.objects.filter(navi_code=nid,parent=None)
    if search_key:
        queryset = queryset.filter(
            #Q(title=search_key) | Q(code=search_key)
            Q(title__startswith=search_key) | Q(code__endswith=search_key)
        )
    # Count total results found
    total_results = queryset.aggregate(count=Count('id'))['count']
    # Pagination (10 results per page)
    paginator = Paginator(queryset.order_by('-id'), 10)
    page_obj = paginator.get_page(page_number)
    # Calculate "Showing X to Y of Z Entries"
    start_index = (page_obj.number - 1) * per_page + 1
    end_index = start_index + len(page_obj) - 1
    return render(request, 'navi_group_page_list.html', {
        'page_obj': page_obj,
        'search_key': search_key,
        'total_results': total_results,
        'start_index': start_index,
        'end_index': end_index,
        'nid':nid,
    })

@auth
@csrf_exempt
def navigrouppage_add(request, nid): 
    page_data = Pages.objects.all()
    
    if request.method == 'POST':
        allData = request.POST.copy()  # Create a mutable copy of request.POST
        allData['navi_code'] = nid  # Injecting nid into POST data 
        # Ensure required fields have default values if not provided
        #for field in ['parent', 'order', 'target', 'external_link', 'link_type']:
            #allData.setdefault(field, 0)     
            #   
        allFiles = request.FILES        
        form = NavigrouppageForm(data=allData, files=allFiles)  
        if form.is_valid():
            form.save()
            msg = {'response': 'success', 'title': 'Data Saved!', 'icon': 'success', 'msg': 'Your data has been successfully saved.'}
        else:
            errors = form.errors.as_json()
            msg = {'response': 'notSaved', 'title': 'Not Saved!', 'icon': 'error', 'msg': 'Your data has not been saved. Please try again.', 'errors': errors}
        
        return JsonResponse(msg, safe=True)
    
    else:
        form = NavigrouppageForm()    
    return render(request, 'navi_group_page_add.html', {'form': form, 'pagedata': page_data, 'nid': nid})




@auth
@csrf_exempt
def navigroupspage_edit(request, nid, id):   
    item = get_object_or_404(Navigroupspages, id=id) 
    data = Navigroupspages.objects.filter(id=id).first()  
    page_data = Pages.objects.all()       
    if request.method == "POST":     
        allData = request.POST.copy()  # Create a mutable copy of request.POST
        allData['navi_code'] = nid  # Injecting nid into POST data 
        allFiles = request.FILES          
        form = NavigrouppageForm(data=allData, files=allFiles, instance=item)
       
        if form.is_valid():
            form.save()           
            msg = {'response': 'success', 'title':'Data Saved!', 'icon':'success',  'msg': 'Your data has been successfully update.'}
        else:
            errors = form.errors.as_json()
            msg = {'response': 'notSaved', 'title':'Not Saved!', 'icon':'error', 'msg': 'Your data has not been update. Please try again.','errors': errors}
        return JsonResponse(msg, safe=True)           
    else:
        form = NavigrouppageForm(instance=item)
    return render(request, 'navi_group_page_add.html', {'data': data,'form': form, 'pagedata': page_data,'nid': nid})

@auth
@csrf_exempt  # Only for quick testing — use CSRF protection in production
def change_navigpage_status(request):
    if request.method == "POST":
        try:
            navi_id = int(request.POST.get('post_id'))
            status = request.POST.get('status') == '1'
            comment = Navigroupspages.objects.get(id=navi_id)
            comment.status = status
            comment.save()            
            msg = {'response': 'success', 'title':'Data Saved!', 'icon':'success',  'msg': 'Your data has been successfully update.'}
            return JsonResponse(msg, safe=True) 
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request'})


@auth
@csrf_exempt
def delete_navigpage(request):
    if request.method == 'POST':
        post_id = request.POST.get('id')
        try:
            post = Navigroupspages.objects.get(id=post_id)
            post.delete()
            return JsonResponse({'status': 'success'})            
        except Post.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Post not found'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})



#**********************************************************************************************
@auth
@csrf_exempt
def navigroupchildpage(request, npid):
    search_key = ""
    page_number = request.GET.get('page', 1)  # Get page number    
    per_page = 10  # Number of entries per page
    if request.method == "POST":
        search_key = request.POST.get('search_key', '').strip()  # Get search query from POST request
    # Query with LIKE and Aggregation
    queryset = Navigroupspages.objects.filter(parent=npid)
    if search_key:
        queryset = queryset.filter(
            #Q(title=search_key) | Q(code=search_key)
            Q(title__startswith=search_key) | Q(code__endswith=search_key)
        )
    # Count total results found
    total_results = queryset.aggregate(count=Count('id'))['count']
    # Pagination (10 results per page)
    paginator = Paginator(queryset.order_by('-id'), 10)
    page_obj = paginator.get_page(page_number)
    # Calculate "Showing X to Y of Z Entries"
    start_index = (page_obj.number - 1) * per_page + 1
    end_index = start_index + len(page_obj) - 1
    return render(request, 'navi_group_child_page_list.html', {
        'page_obj': page_obj,
        'search_key': search_key,
        'total_results': total_results,
        'start_index': start_index,
        'end_index': end_index,
        'npid':npid,
    })


@auth
@csrf_exempt
def navigroupchildpage_add(request, npid): 
    page_data = Pages.objects.all()
    #, parent=npid
    navi_code = Navigroupspages.objects.filter(id=npid).values_list('navi_code', flat=True).first()
        
    if request.method == 'POST':
        allData = request.POST.copy()  # Create a mutable copy of request.POST
        allData['navi_code'] = navi_code  # Injecting navi_code into POST data 
        allData['parent'] = npid  # Injecting nid into POST data        
        # Ensure required fields have default values if not provided        
        #for field in ['order', 'target', 'external_link', 'link_type']:
        #    allData.setdefault(field, 0)
        allFiles = request.FILES        
        form = NavigrouppageForm(data=allData, files=allFiles)  
        if form.is_valid():
            form.save()
            msg = {'response': 'success', 'title': 'Data Saved!', 'icon': 'success', 'msg': 'Your data has been successfully saved.'}
        else:
            errors = form.errors.as_json()
            msg = {'response': 'notSaved', 'title': 'Not Saved!', 'icon': 'error', 'msg': 'Your data has not been saved. Please try again.', 'errors': errors}
        
        return JsonResponse(msg, safe=True)
    
    else:
        form = NavigrouppageForm()    
    return render(request, 'navi_group_child_page_add.html', {'form': form, 'pagedata': page_data, 'npid': npid})




@auth
@csrf_exempt
def navigroupschildpage_edit(request, npid, id):   
    item = get_object_or_404(Navigroupspages, id=id) 
    data = Navigroupspages.objects.filter(id=id).first()  
    
    navi_code = Navigroupspages.objects.filter(id=npid).values_list('navi_code', flat=True).first()

    page_data = Pages.objects.all()       
    if request.method == "POST":     
        allData = request.POST.copy()  # Create a mutable copy of request.POST
        allData['navi_code'] = navi_code  # Injecting nid into POST data 
        allData['parent'] = npid  # Injecting nid into POST data 
        # Ensure required fields have default values if not provided
        #for field in ['order', 'target', 'external_link', 'link_type']:
        #    allData.setdefault(field, 0)

        allFiles = request.FILES          
        form = NavigrouppageForm(data=allData, files=allFiles, instance=item)
       
        if form.is_valid():
            form.save()           
            msg = {'response': 'success', 'title':'Data Saved!', 'icon':'success',  'msg': 'Your data has been successfully update.'}
        else:
            errors = form.errors.as_json()
            msg = {'response': 'notSaved', 'title':'Not Saved!', 'icon':'error', 'msg': 'Your data has not been update. Please try again.','errors': errors}
        return JsonResponse(msg, safe=True)           
    else:
        form = NavigrouppageForm(instance=item)
    return render(request, 'navi_group_child_page_add.html', {'data': data,'form': form, 'pagedata': page_data,'npid': npid})

#****************************************************************************************************************************
@auth
@csrf_exempt
def contactus(request):
    search_key = ""
    page_number = request.GET.get('page', 1)  # Get page number    
    per_page = 10  # Number of entries per page
    if request.method == "POST":
        search_key = request.POST.get('search_key', '').strip()  # Get search query from POST request
    # Query with LIKE and Aggregation
    queryset = Contactus.objects.all()
    if search_key:
        queryset = queryset.filter(
            #Q(title=search_key) | Q(code=search_key)
            Q(fullname__startswith=search_key) | Q(email__endswith=search_key ) | Q(phone__endswith=search_key )
        )
    # Count total results found
    total_results = queryset.aggregate(count=Count('id'))['count']
    # Pagination (10 results per page)
    paginator = Paginator(queryset.order_by('-id'), 10)
    page_obj = paginator.get_page(page_number)
    # Calculate "Showing X to Y of Z Entries"
    start_index = (page_obj.number - 1) * per_page + 1
    end_index = start_index + len(page_obj) - 1
    return render(request, 'contact_list.html', {
        'page_obj': page_obj,
        'search_key': search_key,
        'total_results': total_results,
        'start_index': start_index,
        'end_index': end_index,
    })

@auth
@csrf_exempt
def delete_all_contact(request):
    if request.method == 'POST':
        # Get the comma-separated string of ids from the POST request
        id_array = request.POST.get('idarray', '')        
        # Split the string by colon ":" to get the individual ids
        ids = id_array.split(':')        
        # Loop through the ids and delete the corresponding Html records
        for id in ids:
            if id.strip():  # Avoid deleting empty values
                try:                   
                    # Find the record by ID and delete it
                    contact_record = Contactus.objects.get(id=id)
                    contact_record.delete()
                except Contactus.DoesNotExist:
                    pass  # If the Html object does not exist, skip it

        # Redirect to the 'admin/htmls/index' view after deletion
        return redirect('contact-us')  # Update this to your URL pattern name
    # If the request is not POST, just render the page or return an error
    return render(request, 'contact_list.html')
# Function to simulate database content retrieval


#*******************************************************************************************
@auth
@csrf_exempt
def send_email(request):
    if request.method == 'POST':
        recipient_email = request.POST.get('recipient_email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        attachment = request.FILES.get('attachment')  # Get the file from the form

        # Create an email message
        email = EmailMessage(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [recipient_email],
        )

        # Attach the file to the email if there's an attachment
        if attachment:
            email.attach(attachment.name, attachment.read(), attachment.content_type)
        try:
            # Send the email
            email.send()
            messages.success(request, 'Email sent successfully!')
            return redirect('contact-us')  # Redirect to a success page
        except Exception as e:
            messages.error(request, f'Failed to send email: {str(e)}')
            return redirect('contact-us')  # Redirect to an error page

    return HttpResponse('Invalid request method.', status=400)

#****************start for setting forms add edit****************************************
@auth
@csrf_exempt
def setting_view(request):
    data = Cms_setting.objects.all().values()[:1]
    cm_data=''     
    if data and data[0].get('id') is not None:
        cm_data = Cms_setting.objects.filter(id=data[0]['id'], is_deleted = False).first()        
    return render(request, 'setting.html',{'data':cm_data})



@auth
@csrf_exempt
def add_logo(request):     
    data = Cms_setting.objects.all().values()[:1]       
    if request.method == "POST":   
        allData = request.POST
        allFiles = request.FILES
        if data and data[0]['id'] is not None:
            obj = get_object_or_404(Cms_setting, id=data[0]['id'])
            logoandfavicon_form = logoandfavicon(data=allData, files=allFiles, instance=obj)
            socialmediapages_form = socialmediapages(data=allData, files=allFiles, instance=obj)
            googlerecaptcha_form = googlerecaptcha(data=allData, files=allFiles, instance=obj)
            googleanalytic_form = googleanalytic(data=allData, files=allFiles, instance=obj)
            sociallogin_form = sociallogin(data=allData, files=allFiles, instance=obj)
            facebookpixel_form = facebookpixel(data=allData, files=allFiles, instance=obj)
        else:
            logoandfavicon_form = logoandfavicon(data=allData, files=allFiles)
            socialmediapages_form = socialmediapages(data=allData, files=allFiles)
            googlerecaptcha_form = googlerecaptcha(data=allData, files=allFiles)
            googleanalytic_form = googleanalytic(data=allData, files=allFiles)
            sociallogin_form = sociallogin(data=allData, files=allFiles)
            facebookpixel_form = facebookpixel(data=allData, files=allFiles)

        if logoandfavicon_form.is_valid():
            logoandfavicon_form.save()
            msg = {'response': 'success', 'title':'Data Saved!', 'icon':'success',  'msg': 'Your data has been successfully saved.'}
        else:
            #print(form.errors)
            errors = logoandfavicon_form.errors.as_json()
            msg = {'response': 'notSaved', 'title':'Not Saved!', 'icon':'error', 'msg': 'Your data has not been saved. Please try again.','errors': errors}

        if socialmediapages_form.is_valid():
            socialmediapages_form.save()
            msg = {'response': 'success', 'title':'Data Saved!', 'icon':'success',  'msg': 'Your data has been successfully saved.'}
        else:
            #print(form.errors)
            errors = socialmediapages_form.errors.as_json()
            msg = {'response': 'notSaved', 'title':'Not Saved!', 'icon':'error', 'msg': 'Your data has not been saved. Please try again.','errors': errors}
        
        if googlerecaptcha_form.is_valid():
            googlerecaptcha_form.save()
            msg = {'response': 'success', 'title':'Data Saved!', 'icon':'success',  'msg': 'Your data has been successfully saved.'}
        else:
            #print(form.errors)
            errors = googlerecaptcha_form.errors.as_json()
            msg = {'response': 'notSaved', 'title':'Not Saved!', 'icon':'error', 'msg': 'Your data has not been saved. Please try again.','errors': errors}
        
        if googleanalytic_form.is_valid():
            googleanalytic_form.save()
            msg = {'response': 'success', 'title':'Data Saved!', 'icon':'success',  'msg': 'Your data has been successfully saved.'}
        else:
            #print(form.errors)
            errors = googleanalytic_form.errors.as_json()
            msg = {'response': 'notSaved', 'title':'Not Saved!', 'icon':'error', 'msg': 'Your data has not been saved. Please try again.','errors': errors}
        
        if sociallogin_form.is_valid():
            sociallogin_form.save()
            msg = {'response': 'success', 'title':'Data Saved!', 'icon':'success',  'msg': 'Your data has been successfully saved.'}
        else:
            #print(form.errors)
            errors = sociallogin_form.errors.as_json()
            msg = {'response': 'notSaved', 'title':'Not Saved!', 'icon':'error', 'msg': 'Your data has not been saved. Please try again.','errors': errors}
        
        if facebookpixel_form.is_valid():
            facebookpixel_form.save()
            msg = {'response': 'success', 'title':'Data Saved!', 'icon':'success',  'msg': 'Your data has been successfully saved.'}
        else:
            #print(form.errors)
            errors = facebookpixel_form.errors.as_json()
            msg = {'response': 'notSaved', 'title':'Not Saved!', 'icon':'error', 'msg': 'Your data has not been saved. Please try again.','errors': errors}
        return JsonResponse(msg, safe=False)
    else:
        udData = {
            'activefor':'ud_category',
            'MEDIA_URL':settings.MEDIA_URL,
            'page_title':'Category'
        }  
    return render(request, 'setting.html',{'data':data,'count':post_count})
#end for setting forms add edit****************************************



@auth
@csrf_exempt
def seo_view(request):
    # Fetch top search keywords from Google Search Console
    gsc_keywords = get_google_search_console_data()
    
    # Fetch meta keywords from the website (replace with your actual website URL)
    website_keywords = get_seo_keywords_from_meta('http://pss.bharatpayroll.com/')

    context = {
        'gsc_keywords': gsc_keywords,
        'website_keywords': website_keywords
    }

    return render(request, 'seo_template.html', context)

#**************************************************************************************

@auth
@csrf_exempt
def comment_list(request, cpid=None):    
    search_key = ""  
    page_number = request.GET.get('page', 1)  # Get page number    
    per_page = 10  # Number of entries per page
    if request.method == "POST":
        search_key = request.POST.get('search_key', '').strip()  # Get search query from POST request       
    # Query with LIKE and Aggregation
    queryset = Comment.objects.select_related('post').all()
    if search_key:
        queryset = queryset.filter(
            Q(post__title__icontains=search_key) |  # search in related post title
            Q(content__icontains=search_key)         # search in comment content
        )
    if cpid:
        queryset = queryset.filter(
            Q(post__id__icontains=cpid)  # search in related post title
                  # search in comment content
        )
    
    # Count total results found
    total_results = queryset.aggregate(count=Count('id'))['count']    
    # Pagination (10 results per page)
    paginator = Paginator(queryset.order_by('-id'), 10)
    post_obj = paginator.get_page(page_number)
    # Calculate "Showing X to Y of Z Entries"
    start_index = (post_obj.number - 1) * per_page + 1
    end_index = start_index + len(post_obj) - 1
    return render(request, 'comment_list.html', {
        'post_obj': post_obj,
        'search_key': search_key,
        'total_results': total_results,
        'start_index': start_index,
        'end_index': end_index        
    })

@auth
@csrf_exempt
def delete_comment(request):
    if request.method == 'POST':
        comment_id = request.POST.get('id')
        try:
            post = Comment.objects.get(id=comment_id)
            post.delete()
            return JsonResponse({'status': 'success'})            
        except Post.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Comment not found'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})


@auth
@csrf_exempt  # Only for quick testing — use CSRF protection in production
def comment_status(request):
    if request.method == "POST":
        try:
            comment_id = int(request.POST.get('comment_id'))
            is_approved = request.POST.get('status')
            comment = Comment.objects.get(id=comment_id)
            comment.is_approved = is_approved
            comment.save()            
            msg = {'response': 'success', 'title':'Data Saved!', 'icon':'success',  'msg': 'Your data has been successfully update.'}
            return JsonResponse(msg, safe=True) 
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request'})

#**************************************************************************************
@auth
@csrf_exempt
def post_list(request):    
    search_key = ""
    search_category = ""
    page_number = request.GET.get('page', 1)  # Get page number    
    per_page = 10  # Number of entries per page
    if request.method == "POST":
        search_key = request.POST.get('search_key', '').strip()  # Get search query from POST request
        search_category = request.POST.get('category', '').strip()
    # Query with LIKE and Aggregation
    queryset = Post.objects.select_related('category').all()
    if search_key:
        queryset = queryset.filter(
            #Q(title=search_key) | Q(slug=search_key) | Q(contents__endswith=search_key)
            (Q(title__startswith=search_key) | Q(slug__endswith=search_key))
        )   
    if search_category:
        queryset = queryset.filter(           
             Q(category__slug__icontains=search_category)
        )      
    # Count total results found
    total_results = queryset.aggregate(count=Count('id'))['count']    
    # Pagination (10 results per page)
    paginator = Paginator(queryset.order_by('-id'), 10)
    post_obj = paginator.get_page(page_number)
    # Calculate "Showing X to Y of Z Entries"
    start_index = (post_obj.number - 1) * per_page + 1
    end_index = start_index + len(post_obj) - 1
    categories = Category.objects.all().order_by('name')
    return render(request, 'post_list.html', {
        'post_obj': post_obj,
        'search_key': search_key,
        'total_results': total_results,
        'start_index': start_index,
        'end_index': end_index,
        'categories': categories,
        'search_category':search_category,
    })

@auth
@csrf_exempt
def post_add(request):
    categories = Category.objects.all().order_by('name')
    if request.method == 'POST':
        allData = request.POST
        allFiles = request.FILES                
        form = PostForm(data=allData, files=allFiles)       
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            form.save()
            msg = {'response': 'success', 'title':'Data Saved!', 'icon':'success',  'msg': 'Your data has been successfully saved.'}
        else:
            #print(form.errors)
            errors = form.errors.as_json()
            msg = {'response': 'notSaved', 'title':'Not Saved!', 'icon':'error', 'msg': 'Your data has not been saved. Please try again.','errors': errors}
            
        return JsonResponse(msg, safe=True)

    else:
        form = PostForm()
    return render(request, 'post_add.html', {'form': form,'request': request, 'categories': categories})


@auth
@csrf_exempt
def post_edit(request, id):   
    post = get_object_or_404(Post, id=id)  # Get the post object directly
    data = Post.objects.filter(id=id).first()   
    categories = Category.objects.all().order_by('name') 

    if request.method == "POST":       
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # ✅ Ensures author is set on update
            post.save()
            #form.save_m2m()
            #messages.success(request, "Record update successfully!")
            msg = {'response': 'success', 'title':'Data Saved!', 'icon':'success',  'msg': 'Your data has been successfully update.'}
        else:
            errors = form.errors.as_json()
            msg = {'response': 'notSaved', 'title':'Not Saved!', 'icon':'error', 'msg': 'Your data has not been update. Please try again.','errors': errors}
        
        return JsonResponse(msg, safe=True)    
        #return redirect('list-html')  # Redirect to the list page after updating
    else:
        form = PostForm(instance=post)
    return render(request, 'post_add.html', {'data': data,'form': form, 'categories': categories})

@auth
@csrf_exempt  # Only for quick testing — use CSRF protection in production
def change_post_status(request):
    if request.method == "POST":
        try:
            post_id = int(request.POST.get('post_id'))
            status = request.POST.get('status') == '1'
            comment = Post.objects.get(id=post_id)
            comment.status = status
            comment.save()            
            msg = {'response': 'success', 'title':'Data Saved!', 'icon':'success',  'msg': 'Your data has been successfully update.'}
            return JsonResponse(msg, safe=True) 
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request'})


@auth
@csrf_exempt
def delete_post(request):
    if request.method == 'POST':
        post_id = request.POST.get('id')
        try:
            post = Post.objects.get(id=post_id)
            post.delete()
            return JsonResponse({'status': 'success'})            
        except Post.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Post not found'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})


#**************************************************************************************
@auth
@csrf_exempt
def tag_list(request):
    search_key = ""
    page_number = request.GET.get('page', 1)  # Get page number    
    per_page = 10  # Number of entries per page
    if request.method == "POST":
        search_key = request.POST.get('search_key', '').strip()  # Get search query from POST request
    # Query with LIKE and Aggregation
    queryset = Tag.objects.all()
    if search_key:
        queryset = queryset.filter(
            #Q(title=search_key) | Q(code=search_key)
            Q(name__startswith=search_key) | Q(slug__endswith=search_key)
        )
    # Count total results found
    total_results = queryset.aggregate(count=Count('id'))['count']
    # Pagination (10 results per page)
    paginator = Paginator(queryset.order_by('-id'), 10)
    page_obj = paginator.get_page(page_number)
    # Calculate "Showing X to Y of Z Entries"
    start_index = (page_obj.number - 1) * per_page + 1
    end_index = start_index + len(page_obj) - 1
    return render(request, 'tag_list.html', {
        'page_obj': page_obj,
        'search_key': search_key,
        'total_results': total_results,
        'start_index': start_index,
        'end_index': end_index,
    })

@auth
@csrf_exempt
def post_tag_add(request):
    if request.method == 'POST':
        form = TagForm(request.POST)       
        if form.is_valid():
            form.save()
            msg = {'response': 'success', 'title':'Data Saved!', 'icon':'success',  'msg': 'Your data has been successfully saved.'}
        else:
            #print(form.errors)
            errors = form.errors.as_json()
            msg = {'response': 'notSaved', 'title':'Not Saved!', 'icon':'error', 'msg': 'Your data has not been saved. Please try again.','errors': errors}
            
        return JsonResponse(msg, safe=True)

    else:
        form = NavigroupForm()
    return render(request, 'tag_add.html', {'form': form})


@auth
@csrf_exempt
def post_tag_edit(request, id):   
    item = get_object_or_404(Tag, id=id) 
    data = Tag.objects.filter(id=id).first()         
    if request.method == "POST":       
        form = TagForm(request.POST, instance=item)
        if form.is_valid():
            form.save()           
            msg = {'response': 'success', 'title':'Data Saved!', 'icon':'success',  'msg': 'Your data has been successfully update.'}
        else:
            errors = form.errors.as_json()
            msg = {'response': 'notSaved', 'title':'Not Saved!', 'icon':'error', 'msg': 'Your data has not been update. Please try again.','errors': errors}
        
        return JsonResponse(msg, safe=True)           
    else:
        form = TagForm(instance=item)
    return render(request, 'tag_add.html', {'data': data,'form': form})



#*********************************************************************************
"""@auth
@csrf_exempt
def post_comment(request, slug):       
    post = get_object_or_404(Post, slug=slug, status=True)
    search_key = ""
    page_number = request.GET.get('page', 1)  # Get page number    
    per_page = 10  # Number of entries per page
    if request.method == "POST":
        search_key = request.POST.get('search_key', '').strip()  # Get search query from POST request
    # Query with LIKE and Aggregation    
    queryset = post.comments.filter().order_by('-created_at')   
    if search_key:
        queryset = queryset.filter(
            #Q(title=search_key) | Q(code=search_key)
             Q(name__icontains=search_key) | Q(email__icontains=search_key) | Q(content__icontains=search_key)
        )
    # Count total results found
    #print(queryset)
    total_results = queryset.aggregate(count=Count('id'))['count']
    
    # Pagination (10 results per page)
    paginator = Paginator(queryset.order_by('-id'), 10)
    page_obj = paginator.get_page(page_number)
    # Calculate "Showing X to Y of Z Entries"
    start_index = (page_obj.number - 1) * per_page + 1
    end_index = start_index + len(page_obj) - 1
    
    return render(request, 'postcomment_list.html', {
        'page_obj': page_obj,
        'search_key': search_key,
        'total_results': total_results,
        'start_index': start_index,
        'end_index': end_index,        
    })"""

"""@auth
@csrf_exempt  # Only for quick testing — use CSRF protection in production
def change_comment_status(request):
    if request.method == "POST":
        try:
            post_id = int(request.POST.get('post_id'))
            status = request.POST.get('status') == '1'
            comment = Comment.objects.get(id=post_id)
            comment.is_approved = status
            comment.save()
            #return JsonResponse({'success': True, 'status': status})
            msg = {'response': 'success', 'title':'Data Saved!', 'icon':'success',  'msg': 'Your data has been successfully update.'}
            return JsonResponse(msg, safe=True) 
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request'})"""

@auth
@csrf_exempt
def category(request):
    search_key = ""
    page_number = request.GET.get('page', 1)  # Get page number    
    per_page = 10  # Number of entries per page
    if request.method == "POST":
        search_key = request.POST.get('search_key', '').strip()  # Get search query from POST request
    # Query with LIKE and Aggregation
    queryset = Category.objects.all()
    if search_key:
        queryset = queryset.filter(
            #Q(title=search_key) | Q(code=search_key)
            Q(name__startswith=search_key) | Q(slug__endswith=search_key)
        )
    # Count total results found
    total_results = queryset.aggregate(count=Count('id'))['count']
    # Pagination (10 results per page)
    paginator = Paginator(queryset.order_by('-id'), 10)
    page_obj = paginator.get_page(page_number)
    # Calculate "Showing X to Y of Z Entries"
    start_index = (page_obj.number - 1) * per_page + 1
    end_index = start_index + len(page_obj) - 1
    return render(request, 'category_list.html', {
        'page_obj': page_obj,
        'search_key': search_key,
        'total_results': total_results,
        'start_index': start_index,
        'end_index': end_index,
    })

@auth
@csrf_exempt
def category_add(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            msg = {'response': 'success', 'title':'Data Saved!', 'icon':'success',  'msg': 'Your data has been successfully saved.'}
        else:
            #print(form.errors)
            errors = form.errors.as_json()
            msg = {'response': 'notSaved', 'title':'Not Saved!', 'icon':'error', 'msg': 'Your data has not been saved. Please try again.','errors': errors}
            
        return JsonResponse(msg, safe=True)
    else:
        form = CategoryForm()
    return render(request, 'category_add.html', {'form': form})

@auth
@csrf_exempt
def category_edit(request, id):   
    item = get_object_or_404(Category, id=id) 
    data = Category.objects.filter(id=id).first()         
    if request.method == "POST":       
        form = CategoryForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            #messages.success(request, "Record update successfully!")
            msg = {'response': 'success', 'title':'Data Saved!', 'icon':'success',  'msg': 'Your data has been successfully update.'}
        else:
            errors = form.errors.as_json()
            msg = {'response': 'notSaved', 'title':'Not Saved!', 'icon':'error', 'msg': 'Your data has not been update. Please try again.','errors': errors}
        
        return JsonResponse(msg, safe=True)    
        #return redirect('list-html')  # Redirect to the list page after updating
    else:
        form = CategoryForm(instance=item)
    return render(request, 'category_add.html', {'data': data,'form': form})



#==================================================================================================================

@auth
@csrf_exempt
def testimonials_list(request):    
    search_key = ""
    search_category = ""
    page_number = request.GET.get('page', 1)  # Get page number    
    per_page = 10  # Number of entries per page
    if request.method == "POST":
        search_key = request.POST.get('search_key', '').strip()  # Get search query from POST request        
    # Query with LIKE and Aggregation
    queryset = Testimonial.objects.filter().all().order_by('-id')
    if search_key:
        queryset = queryset.filter(
            #Q(title=search_key) | Q(slug=search_key) | Q(contents__endswith=search_key)
            (Q(name__startswith=search_key) | Q(contents__endswith=search_key))
        )   
        
    # Count total results found
    total_results = queryset.aggregate(count=Count('id'))['count']    
    # Pagination (10 results per page)
    paginator = Paginator(queryset.order_by('-id'), 10)
    post_obj = paginator.get_page(page_number)
    # Calculate "Showing X to Y of Z Entries"
    start_index = (post_obj.number - 1) * per_page + 1
    end_index = start_index + len(post_obj) - 1   
    return render(request, 'testimonials_list.html', {
        'post_obj': post_obj,
        'search_key': search_key,
        'total_results': total_results,
        'start_index': start_index,
        'end_index': end_index,       
        'search_category':search_category,
    })


@auth
@csrf_exempt
def testimonials_add(request):    
    if request.method == 'POST':
        allData = request.POST
        allFiles = request.FILES                
        form = TestimonialForm(data=allData, files=allFiles)       
        if form.is_valid():
            form.save()
            msg = {'response': 'success', 'title':'Data Saved!', 'icon':'success',  'msg': 'Your data has been successfully saved.'}
        else:
            #print(form.errors)
            errors = form.errors.as_json()
            msg = {'response': 'notSaved', 'title':'Not Saved!', 'icon':'error', 'msg': 'Your data has not been saved. Please try again.','errors': errors}
            
        return JsonResponse(msg, safe=True)

    else:
        form = PostForm()
    return render(request, 'testimonials_add.html', {'form': form,'request': request})

@auth
@csrf_exempt
def testimonials_edit(request, id):   
    #post = get_object_or_404(Testimonial, id=id)  # Get the post object directly
    data = Testimonial.objects.filter(id=id).first()      
    if request.method == "POST":       
        form = TestimonialForm(request.POST, request.FILES, instance=data)
        if form.is_valid():
            form.save()
            #messages.success(request, "Record update successfully!")
            msg = {'response': 'success', 'title':'Data Saved!', 'icon':'success',  'msg': 'Your data has been successfully update.'}
        else:
            errors = form.errors.as_json()
            msg = {'response': 'notSaved', 'title':'Not Saved!', 'icon':'error', 'msg': 'Your data has not been update. Please try again.','errors': errors}
        
        return JsonResponse(msg, safe=True)    
        #return redirect('list-html')  # Redirect to the list page after updating
    else:
        form = TestimonialForm(instance=data)
    return render(request, 'testimonials_add.html', {'data': data,'form': form})

@auth
@csrf_exempt  # Only for quick testing — use CSRF protection in production
def testimonials_status(request):
    if request.method == "POST":
        try:
            tmlid = int(request.POST.get('tmlid'))
            is_approved = request.POST.get('status')
            comment = Testimonial.objects.get(id=tmlid)
            comment.is_approved = is_approved
            comment.save()            
            msg = {'response': 'success', 'title':'Data Saved!', 'icon':'success',  'msg': 'Your data has been successfully update.'}
            return JsonResponse(msg, safe=True) 
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request'})

@auth
@csrf_exempt
def delete_testimonials(request):
    if request.method == 'POST':
        tmlid = request.POST.get('id')
        try:
            post = Testimonial.objects.get(id=tmlid)
            post.delete()
            return JsonResponse({'status': 'success'})            
        except Post.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Post not found'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

#==================================================================================================================
@auth
@csrf_exempt
def group_list(request):
    search_key = ""
    page_number = request.GET.get('page', 1)  # Get page number    
    per_page = 10  # Number of entries per page
    if request.method == "POST":
        search_key = request.POST.get('search_key', '').strip()  # Get search query from POST request
    # Query with LIKE and Aggregation
    queryset = Group.objects.all()
    if search_key:
        queryset = queryset.filter(
            #Q(title=search_key) | Q(code=search_key)
            Q(name__startswith=search_key) | Q(slug__endswith=search_key)
        )
    # Count total results found
    total_results = queryset.aggregate(count=Count('id'))['count']
    # Pagination (10 results per page)
    paginator = Paginator(queryset.order_by('-id'), 10)
    page_obj = paginator.get_page(page_number)
    # Calculate "Showing X to Y of Z Entries"
    start_index = (page_obj.number - 1) * per_page + 1
    end_index = start_index + len(page_obj) - 1
    return render(request, 'role_list.html', {
        'groups': page_obj,
        'search_key': search_key,
        'total_results': total_results,
        'start_index': start_index,
        'end_index': end_index,
    })


@auth
@csrf_exempt
def group_add(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            msg = {'response': 'success', 'title':'Data Saved!', 'icon':'success',  'msg': 'Your data has been successfully saved.'}            
        else:
            #print(form.errors)
            errors = form.errors.as_json()
            msg = {'response': 'notSaved', 'title':'Not Saved!', 'icon':'error', 'msg': 'Your data has not been saved. Please try again.','errors': errors}
            
        return JsonResponse(msg, safe=True)
    else:
        form = GroupForm()
    return render(request, 'role_add.html', {'form': form})

@auth
@csrf_exempt
def group_edit(request, id):   
    item = get_object_or_404(Group, id=id) 
    data = Group.objects.filter(id=id).first()         
    if request.method == "POST":       
        form = GroupForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            #messages.success(request, "Record update successfully!")
            msg = {'response': 'success', 'title':'Data Saved!', 'icon':'success',  'msg': 'Your data has been successfully update.'}
        else:
            errors = form.errors.as_json()
            msg = {'response': 'notSaved', 'title':'Not Saved!', 'icon':'error', 'msg': 'Your data has not been update. Please try again.','errors': errors}
        
        return JsonResponse(msg, safe=True)    
        #return redirect('list-html')  # Redirect to the list page after updating
    else:
        form = GroupForm(instance=item)
    return render(request, 'role_add.html', {'data': data,'form': form})

@auth
@csrf_exempt
def group_delete(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        try:
            group = Group.objects.get(id=id)
            group.delete()
            return JsonResponse({'status': 'success'})            
        except Post.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Post not found'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

#===============================================================================================================

@auth
@csrf_exempt
def users(request):
    search_key = ""
    page_number = request.GET.get('page', 1)  # Get page number    
    per_page = 10  # Number of entries per page
    if request.method == "POST":
        search_key = request.POST.get('search_key', '').strip()  # Get search query from POST request
    # Query with LIKE and Aggregation
    queryset = CustomUser.objects.all()
    if search_key:
        queryset = queryset.filter(
            #Q(title=search_key) | Q(code=search_key)
            Q(name__startswith=search_key) | Q(email__endswith=search_key) | Q(mobile__endswith=search_key)
        )
    # Count total results found
    total_results = queryset.aggregate(count=Count('id'))['count']
    # Pagination (10 results per page)
    paginator = Paginator(queryset.order_by('-id'), 10)
    page_obj = paginator.get_page(page_number)
    # Calculate "Showing X to Y of Z Entries"
    start_index = (page_obj.number - 1) * per_page + 1
    end_index = start_index + len(page_obj) - 1
    return render(request, 'users_list.html', {
        'page_obj': page_obj,
        'search_key': search_key,
        'total_results': total_results,
        'start_index': start_index,
        'end_index': end_index,
    })


@auth
@csrf_exempt
def users_add(request):
    groups = Group.objects.all()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Ensure password is hashed
            user.save()

            group_ids = request.POST.getlist('groups')
            if group_ids:
                user.groups.set(group_ids)  # Assign groups to the user

            msg = {
                'response': 'success',
                'title': 'Data Saved!',
                'icon': 'success',
                'msg': 'Your data has been successfully saved.'
            }
        else:
            errors = form.errors.as_json()
            print(errors)
            msg = {
                'response': 'notSaved',
                'title': 'Not Saved!',
                'icon': 'error',
                'msg': 'Your data has not been saved. Please try again.',
                'errors': errors
            }

        return JsonResponse(msg, safe=True)
    else:
        form = RegisterForm()

    return render(request, 'users_add.html', {'form': form, 'groups': groups})

@auth
@csrf_exempt
def users_edit(request, id):   
    groups = Group.objects.all()
    data = get_object_or_404(CustomUser, id=id)  # ✅ Load user
         
    if request.method == "POST":       
        form = UserEditForm(request.POST, instance=data)
        if form.is_valid():
            user = form.save()
            # Update group assignment if needed
            group_ids = request.POST.getlist('groups')
            user.groups.set(group_ids)
            msg = {
                'response': 'success',
                'title': 'Data Saved!',
                'icon': 'success',
                'msg': 'Your data has been successfully updated.'
            }
        else:
            errors = form.errors.as_json()
            msg = {
                'response': 'notSaved',
                'title': 'Not Saved!',
                'icon': 'error',
                'msg': 'Your data has not been updated. Please try again.',
                'errors': errors
            }
        return JsonResponse(msg, safe=True)    
    else:
        form = UserEditForm(instance=data)
    return render(request, 'users_edit.html', {'data': data, 'form': form, 'groups': groups})


@auth
@csrf_exempt  # Only for quick testing — use CSRF protection in production
def users_status(request):
    if request.method == "POST":
        try:
            user_id = int(request.POST.get('user_id'))
            is_active = request.POST.get('status')
            user = CustomUser.objects.get(id=user_id)
            user.is_active = is_active
            user.save()            
            msg = {'response': 'success', 'title':'Data Saved!', 'icon':'success',  'msg': 'Your data has been successfully update.'}
            return JsonResponse(msg, safe=True) 
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request'})


@auth
@csrf_exempt
def users_delete(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        print(id)
        try:
            user = CustomUser.objects.get(id=id)
            user.delete()
            return JsonResponse({'status': 'success'})            
        except Post.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Post not found'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

















def logout_view(request):
    logout(request)
    return redirect('login')