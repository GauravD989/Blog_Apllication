from django.urls import path
from blog import views
from blog.views import *

urlpatterns = [
    path('home/', views.home, name='home'),

    path('signup/', views.signup, name='signup'),
    path('login/', views.handlelogin, name='handlelogin'),
    path('logout/', views.handlelogout, name='handlelogout'),

    path('readmore/<int:id>/', views.readmore, name='readmore'),
    path('addblog/', Addblog.as_view(), name='addblog'),

    path('tag-suggestions/', views.get_tag_suggestions, name='tag-suggestions'),

    path('editblog/<int:pk>/', Editblog.as_view(), name='editblog'),
    path('deleteblog/<int:pk>/', Deleteblog.as_view(), name='deleteblog'),

    path('restoreblog/<int:pk>/', restore_blog, name='restore-blog'),

    path('category/<int:category_id>/blogs/', views.category_blogs, name='category_blogs'),
    path('myblogs/', views.my_blogs, name='my-blogs'),

    path("tags/<int:tag_id>/", views.list_posts_by_tag, name="tag"),
    path('search/', views.search_blogs, name='search_blogs'),

    path('dashboard/', views.dashboard, name='dashboard'),

    path('addcategory/', Addcategory.as_view(), name='addcategory'),

    path('my-categories/', views.my_categories, name='my-categories'),

    path('edit-category/<int:pk>/', views.edit_category, name='edit-category'),
    path('delete-category/<int:pk>/', views.delete_category, name='delete-category'),
]