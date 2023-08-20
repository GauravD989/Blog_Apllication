from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from blog.models import Blog, Category, Tag
from math import ceil
from django.contrib.auth import authenticate, login, logout
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404

from django.core.paginator import Paginator

from .forms import BlogForm
from django.db.models import Q

# Create your views here.

def home(request):
    categories = Category.objects.order_by('created_at')  
    
    items_per_page = 9  
    
    paginator = Paginator(categories, items_per_page)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj, 'categories':categories
    }
    
    return render(request, 'home.html', context)

def my_blogs(request):
    if request.user.is_authenticated:
        user = request.user
        blogs = Blog.objects.filter(author=user).order_by('-created_at')  

        selected_blog_id = request.GET.get('blog_id')

        selected_blog = None
        if selected_blog_id:
            selected_blog = get_object_or_404(Blog, id=selected_blog_id)

        context = {'blogs': blogs, 'selected_blog': selected_blog, 'selected_blog_id': selected_blog_id}
        return render(request, 'my_blogs.html', context)
    else:
        return redirect('login')
    
def category_blogs(request, category_id):
    category = get_object_or_404(Category, pk=category_id)

    blogs = Blog.objects.filter(category=category.name).order_by('-created_at')

    items_per_page = 9  
    
    paginator = Paginator(blogs, items_per_page)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'page_obj' : page_obj,
    }
    return render(request, 'category_blogs.html', context)

def list_posts_by_tag(request, tag_id):

    tag = get_object_or_404(Tag, id=tag_id)

    posts = Blog.objects.filter(tags=tag_id).order_by('-created_at')

    items_per_page = 9  
    
    paginator = Paginator(posts, items_per_page)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "tag_name": tag.name,
        'page_obj' : page_obj,
    }

    return render(request, "filtered_by_tag.html", context)

def search_blogs(request):
    query = request.GET.get('q')
    
    if query:
        blogs = Blog.objects.filter(Q(title__icontains=query) | Q(content__icontains=query) | Q(category__icontains=query))

    else:
        blogs = []

    context = {
        'query': query,
        'blogs': blogs
    }
    return render(request, 'search_results.html', context)

def signup(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['pass1']
        confirm_password=request.POST['pass2']
        
        if password!=confirm_password:
            messages.warning(request, 'Password is Not Matching')
            return render(request, 'signup.html')
        
        try:
            if User.objects.get(username=username):
                messages.info(request, 'Email is Taken')
                return render(request, 'signup.html')

        except Exception as identifier:
            pass
         
        user = User.objects.create_user(username, username, password)
        user.save()
        
        messages.success(request,"Welcome! {} Your account is created successfully". format(user.username))
        return redirect('/login/')
        
    return render(request, 'signup.html')


def handlelogin(request):
    if request.method=="POST":
        username=request.POST['username']
        userpassword=request.POST['pass1']
        myuser=authenticate(username=username, password=userpassword)

        if myuser is not None:
            login(request,myuser)
            messages.success(request,"Login Success")
            return redirect('/home')
    
        else:
            messages.warning(request,'Invalid Credentials')
            return redirect('/login/')
    
    return render(request, "login.html")

def handlelogout(request):
    logout(request)
    messages.warning(request, "You have successfully logged out")
    return redirect('/login/')

def readmore(request, id):
    data = Blog.objects.get(id=id)
    context = {'data' : data}

    return render(request, 'readmore.html', context)

class Addblog(CreateView):
    model = Blog
    form_class = BlogForm
    template_name = "addblog.html"
    success_url = reverse_lazy('home')

class Editblog(UpdateView):
    model = Blog
    form_class = BlogForm
    template_name = "editblog.html"
    success_url = reverse_lazy('my-blogs')


class Deleteblog(DeleteView):
    model = Blog
    fields = ['title','content', 'category', 'image']
    template_name = "deleteblog.html"
    success_url = reverse_lazy('my-blogs')

