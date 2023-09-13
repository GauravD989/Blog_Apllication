from django import forms
from .models import Blog, Tag, Comment, Category

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.contrib.auth.models import User  
from django.contrib.auth import password_validation


class BlogForm(forms.ModelForm):

    class Meta:
        model = Blog
        fields = ['title', 'author', 'content', 'category', 'tags', 'image', 'slug']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'content', 'image', 'slug'] 

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class EmptyForm(forms.Form):
    pass

# ///////////////////////////////////////////////

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Override error messages for password fields
        self.fields['password1'].error_messages = {
            'password_mismatch': 'Passwords do not match.',
        }
        self.fields['password2'].error_messages = {
            'required': 'Please confirm your password.',
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            user = authenticate(username=email, password=password)

            if not user or not user.is_active:
                raise forms.ValidationError("Please Activate your Account First, by Clicking on the Link on your Email! ")

        return cleaned_data