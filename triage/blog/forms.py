from django import forms
from .models import Blog, Tag, Comment, Category

class BlogForm(forms.ModelForm):

    class Meta:
        model = Blog
        fields = ['title', 'author', 'content', 'category', 'tags', 'image']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'content', 'image'] 

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class EmptyForm(forms.Form):
    pass