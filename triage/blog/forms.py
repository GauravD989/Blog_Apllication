from django import forms
from .models import Blog, Tag

class BlogForm(forms.ModelForm):
    
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False  
    )

    class Meta:
        model = Blog
        fields = ['title', 'author', 'content', 'category', 'tags', 'image']
