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
    
class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.timestamp}"
    
class DeletedBlog(models.Model):
    title = models.CharField(max_length=255)
    content = RichTextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='shop/images', blank=True, null=True, default="")

    deleted_at = models.DateTimeField(auto_now_add=True)
    is_restored = models.BooleanField(default=False)

    tags = models.ManyToManyField(to=Tag, blank=True)

    def restore(self):
        # Create a new entry in the Blog model using the data from DeletedBlog
        Blog.objects.create(
            title=self.title,
            content=self.content,
            category=self.category,
            author=self.author,
            image=self.image,
            tags=self.tags.all()
        )
        
        # Mark the deleted blog as restored and save
        self.is_restored = True
        self.save()
    
    def __str__(self):
        return self.title

    
    

    
    
