from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User

# Create your models here.
    
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=255)
    content = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    image = models.ImageField(upload_to='category/images', blank=True, null=True, default="")

    def __str__(self):
        return self.name

class Blog(models.Model):
    title = models.CharField(max_length=255)
    content = RichTextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    image = models.ImageField(upload_to='shop/images', blank=True, null=True, default="")

    tags = models.ManyToManyField(to=Tag, blank=True)
    
    def __str__(self):
        return self.title
    
    

    
    
