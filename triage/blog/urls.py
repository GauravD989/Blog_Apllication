from django.urls import path
from blog import views
from blog.views import *

urlpatterns = [
    path('', views.home, name='home'),

    path('signup/', views.signup, name='signup'),
    path('login/', views.handlelogin, name='handlelogin'),
    path('logout/', views.handlelogout, name='handlelogout'),

    path('readmore/<int:id>/', views.readmore, name='readmore'),
    path('addblog/', Addblog.as_view(), name='addblog'),

    path('editblog/<int:pk>/', Editblog.as_view(), name='editblog'),
    path('deleteblog/<int:pk>/', Deleteblog.as_view(), name='deleteblog'),

    path('category/<int:category_id>/blogs/', views.category_blogs, name='category_blogs'),
    path('myblogs/', views.my_blogs, name='my-blogs'),

    path("tags/<int:tag_id>/", views.list_posts_by_tag, name="tag"),
    path('search/', views.search_blogs, name='search_blogs'),
]