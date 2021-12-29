from typing import AsyncIterable
from django.contrib.auth.models import User
from django.core import paginator
from django.shortcuts import redirect, render
from .models import Author, BlogPost, Category, Chat
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .forms import EditProfile
from django.contrib import messages
from django.db.models import Q

from django.core.paginator import Paginator

# Create your views here.
def home(request):
    # posts = BlogPost.objects.all()
    s_w = request.GET.get('q')
    cat = request.GET.get('cat')
    
    if s_w is not None:
        s_w = str(s_w).title()
        posts = BlogPost.objects.filter(title__icontains=s_w).order_by("-created_at")
    elif cat is not None:
        category = Category.objects.get(name=cat)
        posts = BlogPost.objects.filter(category=category).order_by("-created_at")
    else:
        posts = BlogPost.objects.all().order_by("-created_at")
        
    paginator = Paginator(posts,4)
    categories = Category.objects.all()
    page_number = request.GET.get('page')
    p_posts = paginator.get_page(page_number)
    featured_posts = BlogPost.objects.filter(is_featured=True)

    context = {
        'posts':p_posts,
        'paginator':paginator,
        'categories':categories,
        'featured_posts':featured_posts,
    }

    return render(request,'post/index.html',context)

def about(request):
    return render(request,'post/about.html')

def registerpage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        if username == "":
            messages.error(request, "Username cannot be blank.")
            return redirect('register')
        

        # username = request.POST.get('username') #more secure
        email = request.POST.get('email')

        password = request.POST.get('password')
        if password == "":
            messages.error(request,"Password cannot be blank.")
            return redirect('register')

        c_password = request.POST.get('c_password')
        if password != c_password:
            messages.error(request, "Password do not match.")
            return redirect('register')

        name = request.POST.get('name')
        phone = request.POST.get('phone')

        #check if there is already a user with same username
        try:
            p_user = User.objects.get(username=username)
        except:
            p_user = None

        if p_user is not None:
            messages.error(request, "Username already exists.")
            return redirect('register')
        else:
            user = User.objects.create_user(username,email,password)
            user.save()

            author = Author(
                    user=user,
                    name=name,
                    phone=phone,
                    address=''
                    )
            author.save()
            messages.error(request,'Account Created Succesfully')
            return redirect('register')

    return render(request,'post/register.html')

def loginpage(request):
    if(request.method == "POST"):
        name = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=name,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, "No user matching those credentials.")

    return render(request,'post/login.html')

def logoutpage(request):
    logout(request)
    return redirect('home')

def post_details(request,pk):
    post = BlogPost.objects.get(title=pk)
    context = {
        'post':post,
    }
    return render(request,'post/detail.html',context)

@login_required(login_url='login')
def create_post(request):
    categories = Category.objects.all()

    if (request.method == 'POST'):
        # print(request.user)
        title = request.POST['title']
        category = request.POST['category']
        content = request.POST['content']
        image = request.FILES['image']
        blog = BlogPost(title=title,
            author=request.user,
            category=Category.objects.get(name=category),
            content=content,
            image= image
            )
        blog.save()
        
        messages.add_message(request,messages.INFO,'Post created Successfully !!!')

    context = {
        'categories':categories,
    }

    return render(request,'post/createpost.html',context)

def editprofile(request):
    user = User.objects.get(username=request.user)

    if request.method == "POST":
        author = EditProfile(request.POST,request.FILES,instance= user.author)
        author.save()
        messages.add_message(request,messages.INFO,'Edited Successfully !!!')
    else:
        author = EditProfile(instance=user.author)

    context = {
        'author':author,
    }

    return render(request,'post/edit-user.html',context)

def mypost(request):
    posts = BlogPost.objects.all().filter(author=request.user)
    context = {
        'posts':posts,
    }
    return render(request,'post/mypost.html',context)

def chat(request):
    if request.method == "POST":
        chat = request.POST.get('message')
        new_chat = Chat(sender=request.user,message=chat)
        new_chat.save()

    chats = Chat.objects.all()

    context = {
        'chats':chats
    }
    
    return render(request,'post/chat.html',context)

