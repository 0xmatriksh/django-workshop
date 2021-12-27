from django.urls import path
from django.urls import path
from .views import home,about,loginpage,post_details,create_post,logoutpage,registerpage,editprofile,mypost

urlpatterns = [
    path('',home,name='home'),
    path('about',about,name='about'),
    path('login',loginpage,name='login'),
    path('post-detail/<str:pk>',post_details,name='post-detail'),
    path('create-post',create_post,name='create-post'),
    path('logout',logoutpage,name='logout'),
    path('register',registerpage,name='register'),
    path('edit-profile',editprofile,name="edit-profile"),
    path('mypost',mypost,name="mypost"),
    ]