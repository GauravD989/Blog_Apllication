from django.urls import path
from blog import views
from blog.views import *

urlpatterns = [
    path('home/', views.home, name='home'),

    path('signup/', views.signup, name='signup'),
    path('login/', views.handlelogin, name='handlelogin'),
    path('logout/', views.handlelogout, name='handlelogout'),
    path('activate/<uidb64>/<token>', views.ActivateAccountView.as_view(), name='activate'),

    path('readmore/<slug:slug>/', views.readmore, name='readmore'), # check
    path('addblog/', Addblog.as_view(), name='addblog'),

    path('tag-suggestions/', views.get_tag_suggestions, name='tag-suggestions'),

    path('editblog/<slug:slug>/', Editblog.as_view(), name='editblog'), #check
    path('deleteblog/<slug:slug>/', Deleteblog.as_view(), name='deleteblog'), #check

    path('restoreblog/<slug:slug>/', Restoreblog.as_view(), name='restoreblog'), #check

    path('category/<slug:slug>/blogs/', views.category_blogs, name='category_blogs'), #check
    path('myblogs/', views.my_blogs, name='my-blogs'),

    path('my_deleted_blogs/', views.my_deleted_blogs, name='my_deleted_blogs'),

    path("tags/<slug:slug>/", views.list_posts_by_tag, name="tag"), #check
    path('search/', views.search_blogs, name='search_blogs'),

    path('dashboard/', views.dashboard, name='dashboard'),

    path('addcategory/', Addcategory.as_view(), name='addcategory'),

    path('my-categories/', views.my_categories, name='my-categories'),

    path('edit-category/<slug:slug>/', views.edit_category, name='edit-category'), #check
    path('delete-category/<slug:slug>/', views.delete_category, name='delete-category'), #check


    path('save-comment/', views.save_comment, name='save-comment'),


]