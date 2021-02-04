from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,Http404
from django.http import HttpResponseRedirect,JsonResponse
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .email import send_welcome_email


def index(request):
    return render(request,'index.html')


def signup(request):
    if request.method =='POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            email = form.cleaned_data['email']
            user = authenticate(username=username,password=password)
            send_welcome_email(username,email)
            login(request,user)
            return redirect('index')
    
    else:
        form = SignUpForm()
    return render(request,'registration/registration_form.html',{'form': form})

@login_required(login_url='login')
def profile(request, username):

    user = User.objects.get(username=username)
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateUserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():

            user_form.save()
            profile_form.save()
           
            return HttpResponseRedirect(request.path_info)
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateUserProfileForm(instance=request.user.profile)
    
    return render(request, 'registration/profile.html',{'user_form': user_form, 'profile_form': profile_form,})

@login_required(login_url='login')
def all_hoods(request):
    hoods = Hood.objects.all()
    return render(request,'all_hoods.html',{'hoods':hoods})

@login_required(login_url='login')
def hood(request,hood_id):
    current_user = request.user
    hood_name = current_user.profile.hood
    hood = Hood.objects.get(id=hood_id)
    posts = Post.objects.filter(hood=hood)
    print(posts)
    businesses = Business.objects.filter(hood=hood)
    print(businesses)
    return render(request,'hoods.html',{"hood_name":hood_name,"hood":hood,"posts":posts,"businesses":businesses})

@login_required(login_url='login')
def search_results(request):
    if 'search' in request.GET and request.GET['search']:
        search_term = request.GET.get('search')
        searched_business = Business.search_business(search_term)
        print(searched_business)
        message = f"{search_term}"

        return render(request, 'search.html',{'searched':searched_business})

    else:
        message = "You haven't searched for any business"
        return render(request,'search.html',{"message":message})    

@login_required(login_url='login')
def upload_business(request,hood_id):
    hood = Hood.objects.get(id=hood_id)
    if request.method == 'POST':
        businessform = BusinessForm(request.POST, request.FILES)
        if businessform.is_valid():
            upload = businessform.save(commit=False)
            upload.user=request.user
            upload.hood=hood
            upload.save()
        return redirect('hood',hood.id)
    else:
        businessform = BusinessForm()
    return render(request,'upload/upload_business.html',{'form':businessform,'hood':hood})


@login_required(login_url='login')
def add_post(request,hood_id):
    hood = Hood.objects.get(id=hood_id)
    if request.method == 'POST':
        postform = PostForm(request.POST, request.FILES)
        if postform.is_valid():
            post = postform.save(commit=False)
            post.profile = request.user.profile
            post.user = request.user
            post.hood=hood
            post.save()
            return redirect('hood',hood.id)
    else:
        postform = PostForm()
    return render(request,'upload/upload_post.html',{'postform':postform,'hood':hood})

@login_required(login_url='login')
def join(request,hood_id):
    hood = Hood.objects.get(id=hood_id)
    current_user = request.user
    current_user.profile.hood = hood
    current_user.profile.save()
    return redirect('hood',hood_id)
    



@login_required(login_url='login')
def leave(request,hood_id):
    current_user = request.user
    current_user.profile.hood = None
    current_user.profile.save()
    return redirect('index')

