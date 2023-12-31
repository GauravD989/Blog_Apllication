from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User
from blog.models import Blog, Category, Tag, Comment
from django.views import View
from math import ceil
from django.contrib.auth import authenticate, login, logout
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404

from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .utils import TokenGenerator, generate_token
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.core.mail import EmailMessage
from django.conf import settings

from .forms import SignupForm, LoginForm

from django.core.paginator import Paginator

from .forms import BlogForm, CommentForm, CategoryForm, EmptyForm

from django.db.models import Q
from django.http import JsonResponse
import json

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
        blogs = Blog.objects.filter(author=user, is_deleted=False).order_by('-created_at')  

        blogs_per_page = 10
        paginator = Paginator(blogs, blogs_per_page)

        page_number = request.GET.get('page')
        
        # Get the blogs for the current page
        page_obj = paginator.get_page(page_number)

        context = {'page_obj': page_obj}
        return render(request, 'my_blogs.html', context)
    else:
        return redirect('login')
    
def category_blogs(request, slug):
    category = get_object_or_404(Category, slug=slug)

    blogs = Blog.objects.filter(category=category, is_deleted=False).order_by('-created_at')

    items_per_page = 9  
    
    paginator = Paginator(blogs, items_per_page)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'page_obj' : page_obj,
    }
    return render(request, 'category_blogs.html', context)

def my_deleted_blogs(request):
    if request.user.is_authenticated:
        user = request.user
        blogs = Blog.objects.filter(author=user, is_deleted=True).order_by('-created_at')

        blogs_per_page = 10
        paginator = Paginator(blogs, blogs_per_page)

        page_number = request.GET.get('page')
        
        # Get the blogs for the current page
        page_obj = paginator.get_page(page_number)

        context = {'page_obj': page_obj}
        return render(request, 'my_deleted_blogs.html', context)
    else:
        return redirect('login')

def list_posts_by_tag(request, slug):

    tag = get_object_or_404(Tag, slug=slug)
    
    posts = Blog.objects.filter(tags__slug=slug, is_deleted=False).order_by('-created_at')

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
        blogs = Blog.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))

    else:
        blogs = []

    context = {
        'query': query,
        'blogs': blogs
    }
    return render(request, 'search_results.html', context)

def dashboard(request):
    user = request.user
    user_posts = Blog.objects.filter(author=user)
    total_posts = Blog.objects.all().count()
    user_tags = Tag.objects.filter(blog__author=user).distinct()
    user_categories = Category.objects.filter(author=user)

    count_user_categories = user_categories.count()

    categories = Category.objects.all()
    my_del_blog = Blog.objects.filter(author=user, is_deleted=True).count()


    context = {
        'user': user,
        'user_posts': user_posts,
        'total_posts': total_posts,
        'user_tags': user_tags,
        'user_categories': user_categories,
        'count_user_categories' : count_user_categories,
        'categories' : categories,
        'my_del_blog':my_del_blog,
    }

    return render(request, 'dashboard.html', context)

# **************************************Fuction based signup**************************************

# def signup(request):
#     if request.method=="POST":
#         username=request.POST['username']
#         email=request.POST['email']
#         password=request.POST['pass1']
#         confirm_password=request.POST['pass2']
        
#         if password!=confirm_password:
#             messages.warning(request, 'Password is Not Matching')
#             return render(request, 'signup.html')
        
#         try:
#             if User.objects.get(username=username):
#                 messages.info(request, 'Username is Taken')
#                 return render(request, 'signup.html')

#         except Exception as identifier:
#             pass
         
#         user = User.objects.create_user(username, email, password)
#         user.is_active=False
#         user.save()

#         email_subject = "Activate Your Account"
#         message = render_to_string('activate.html', {
#             'user':user,
#             'domain':'127.0.0.1:8000', # if i am hosting to www.google.com, then i have write this domain here, Not '127.0.0.1:8000' : localhost
#             'uid':urlsafe_base64_encode(force_bytes(user.pk)),
#             'token':generate_token.make_token(user)
#         })

#         email_message = EmailMessage(email_subject,message, settings.EMAIL_HOST_USER, [email])

#         email_message.send()

#         messages.success(request,"Activate Your Account by clicking the link in your email")
        
#         # messages.success(request,"Welcome! {} Your account is created successfully". format(user.username))
#         return redirect('/login/')
        
#     return render(request, 'signup.html')

# class ActivateAccountView(View):
#     def get(self, request, uidb64, token):
#         try:
#             uid=force_text(urlsafe_base64_decode(uidb64))
#             user=User.objects.get(pk=uid)
#         except Exception as identifier:
#             user=None
#         if user is not None and generate_token.check_token(user, token):
#             user.is_active = True
#             user.save()
#             messages.info(request,"Welcome! {} Your Account is Activated Successfully".format(user.username))        
#             return redirect('/login/')
#         return render(request, 'activatefail.html')

# *************************************fuction base login.*******************

# def handlelogin(request):
#     if request.method=="POST":
#         username=request.POST['username']
#         userpassword=request.POST['pass1']
#         myuser=authenticate(username=username, password=userpassword)

#         if myuser is not None:
#             login(request,myuser)
#             messages.success(request,"Login Success")
#             return redirect('/home')
    
#         else:
#             messages.warning(request,'Invalid Credentials')
#             return redirect('/login/')
    
#     return render(request, "login.html")

class SignupView(View):
    def get(self, request):
        form = SignupForm()
        return render(request, 'signup.html', {'form': form})

    def post(self, request):
        print('heee')
        form = SignupForm(request.POST)
        if form.is_valid():
            print('neee')
            user = form.save(commit=False)
            user.is_active = False
            email = form.cleaned_data['email']
            user.save()

            email_subject = "Activate Your Account"
            message = render_to_string('activate.html', {
                'user':user,
                'domain':'127.0.0.1:8000', # if i am hosting to www.google.com, then i have write this domain here, Not '127.0.0.1:8000' : localhost
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':generate_token.make_token(user)
            })

            email_message = EmailMessage(email_subject,message, settings.EMAIL_HOST_USER, [email])

            email_message.send()

            messages.success(request, "Activate Your Account by clicking the link in your email")
            return redirect('/login/')
        else:
            print(form.errors)
        return render(request, 'signup.html', {'form': form})
    
class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid=force_text(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=uid)
        except Exception as identifier:
            user=None
        if user is not None and generate_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.info(request,"Welcome! {} Your Account is Activated Successfully".format(user.username))        
            return redirect('/login/')
        return render(request, 'activatefail.html')
    
class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None and user.is_active:
                login(request, user)
                messages.success(request, "Login Success")
                return redirect('/home')
            else:
                messages.warning(request, 'Invalid Credentials')
        return render(request, 'login.html', {'form': form})
    

def handlelogout(request):
    logout(request)
    messages.warning(request, "You have successfully logged out")
    return redirect('/login/')

def readmore(request, slug):
    blog = Blog.objects.get(slug=slug, is_deleted=False)

    comments = Comment.objects.filter(blog=blog).order_by('-timestamp')
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        
        if form.is_valid():
            comment = form.save(commit=False)   
            comment.user = request.user
            comment.blog = blog
            comment.save()
            
            return redirect('readmore', slug=slug)
    else:
        form = CommentForm()

    context = {'data': blog, 'comments': comments, 'form': form}

    return render(request, 'readmore.html', context)

# As we have used Ajax, we have added a fuction save_comment, it will saved the comments in the database
def save_comment(request):
    if request.method=='POST':
        comment = request.POST['comment']
        dataid = request.POST['dataid']
        data = Blog.objects.get(pk=dataid)
        user=request.user
        
        comment_obj = Comment.objects.create(
                        blog = data,
                        user = user,
                        content = comment
                    )

        formatted_timestamp = comment_obj.timestamp.strftime("%b. %d, %Y, %I:%M %p")
       
        return JsonResponse({'bool': True, 'timestamp': formatted_timestamp})

def my_categories(request):
    categories = Category.objects.filter(author=request.user).order_by('-created_at')    # Get the user's categories

    blogs_per_page = 10
    
    paginator = Paginator(categories, blogs_per_page)

    page_number = request.GET.get('page')
    
    # Get the blogs for the current page
    page_obj = paginator.get_page(page_number)

    context = {'page_obj': page_obj}
    return render(request, 'my_categories.html', context)
    

def edit_category(request, slug):
    category = get_object_or_404(Category, slug=slug)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)  
        if form.is_valid():
            form.save()
            return redirect('my-categories')
    else:
        form = CategoryForm(instance=category) 

    context = {'form': form}
    return render(request, 'edit_category.html', context)

def delete_category(request, slug):
    category = get_object_or_404(Category, slug=slug)

    if request.method == 'POST':
        category.delete()
        return redirect('my-categories')

    context = {'category': category}
    return render(request, 'delete_category.html', context)

class Addblog(CreateView):
    model = Blog
    form_class = BlogForm
    template_name = "addblog.html"
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        blog = form.save(commit=False)  # Get the unsaved instance
        blog.author = self.request.user  # Assuming you want to associate the logged-in user as the author

        tags_data = form.cleaned_data['tags']
        print('tags_data', tags_data)
        if tags_data:
            tag_dicts = json.loads(tags_data)
            print('tag_dicts',tag_dicts)
            tag_names = [tag_dict['value'] for tag_dict in tag_dicts]
            print('tag_names', tag_names)

            
            tags_id=[]
            for tag_name in tag_names:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                print('tag', tag)

                newtag = get_object_or_404(Tag, name=tag.name)
                newtag_id = newtag.pk
                tags_id.append(newtag_id)

            print(tags_id)  
            # blog.tags.set(tags_id)
              
            form.cleaned_data.pop('tags')
            form.cleaned_data['tags']=tags_id
            
            

        return super().form_valid(form)
    
    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_suggestions = Tag.objects.values_list('name', flat=True)
        context['tag_suggestions'] = json.dumps(list(tag_suggestions))
        return context
    
# class Addblog(CreateView):
#     model = Blog
#     form_class = BlogForm
#     template_name = "addblog.html"
#     success_url = reverse_lazy('home')

#     def form_valid(self, form):
#         blog = form.save(commit=False)  # Get the unsaved instance
#         blog.author = self.request.user  # Assuming you want to associate the logged-in user as the author
#         blog.save()  # Save the blog instance

#         tags_data = form.cleaned_data['tags']
#         if tags_data:
#             tag_dicts = json.loads(tags_data)
#             tag_names = [tag_dict['value'] for tag_dict in tag_dicts]

#             tags = []
#             for tag_name in tag_names:
#                 tag, _ = Tag.objects.get_or_create(name=tag_name)
#                 tags.append(tag)
            
#             # Associate tags with the blog
#             blog.tags.set(tags)

#         return super().form_valid(form)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         tag_suggestions = Tag.objects.values_list('name', flat=True)
#         context['tag_suggestions'] = json.dumps(list(tag_suggestions))
#         return context


def get_tag_suggestions(request):
    query = request.GET.get('q', '')
    tag_suggestions = Tag.objects.filter(name__istartswith=query).values_list('name', flat=True)
    return JsonResponse(list(tag_suggestions), safe=False)

class Addcategory(CreateView):
    model = Category
    fields = ['name', 'content', 'author', 'image']
    template_name = "addcategory.html"
    success_url = reverse_lazy('addblog')

class Editblog(UpdateView):
    model = Blog
    form_class = BlogForm
    template_name = "editblog.html"
    success_url = reverse_lazy('my-blogs')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blog = self.get_object()
        tag_names = [tag.name for tag in blog.tags.all()]
        context['tag_names'] = json.dumps(tag_names)  # Provide tag names to the context
        return context


class Deleteblog(View):
    template_name = "deleteblog.html"
    success_url = reverse_lazy('my-blogs')

    def get(self, request, slug):
        # Retrieve the blog post to be deleted
        blog = get_object_or_404(Blog, slug=slug)
        context = {'blog': blog}
        return render(request, self.template_name, context)

    def post(self, request, slug):
        # Retrieve the blog post to be deleted
        blog = get_object_or_404(Blog, slug=slug)

        # Soft delete the blog post by marking it as deleted
        blog.is_deleted = True
        blog.save()

        # Redirect to the success URL
        return redirect(self.success_url)
    
class Restoreblog(View):
    template_name = "restore_blog.html"
    success_url = reverse_lazy('my-blogs')

    def get(self, request, slug):
        # Retrieve the blog post to be deleted
        blog = get_object_or_404(Blog, slug=slug)
        context = {'blog': blog}
        return render(request, self.template_name, context)

    def post(self, request, slug):
        # Retrieve the blog post to be deleted
        blog = get_object_or_404(Blog, slug=slug)

        # Soft delete the blog post by marking it as deleted
        blog.is_deleted = False
        blog.save()

        # Redirect to the success URL
        return redirect(self.success_url)
    

# def restore_blog(request, pk):
#     deleted_blog = DeletedBlog.objects.get(pk=pk)
#     deleted_blog.restore()
#     return redirect('my-blogs')

