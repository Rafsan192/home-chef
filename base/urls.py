from django.urls import path, re_path

from base import views

urlpatterns = [
    path('', views.index, name='home'),
    path('courses/', views.courses, name='all_courses'),
    re_path(r'^course/$', views.course, name='course'),
    path('blogs/', views.blogs, name='all_blogs'),
    re_path(r'^blog/$', views.blog, name='blog'),
    path('chefs/', views.chefs, name='all_chefs'),
    path('all-chefs/', views.all_chefs, name='chefs'),
    path('add-chef/', views.add_chef, name='add_chef'),
    re_path(r'^update-chef/$', views.update_chef, name='update_chef'),
    re_path(r'^delete-chef/$', views.delete_chef, name='delete_chef'),
    path('students/', views.students, name='all_students'),
    path('add-student/', views.add_student, name='add_student'),
    re_path(r'^update-student/$', views.update_student, name='update_student'),
    re_path(r'^delete-student/$', views.delete_student, name='delete_student'),
    re_path(r'^enroll/$', views.enroll, name='enroll'),
    path('my-enrolls/', views.my_enrolls, name='my_enrolls'),
    re_path(r'^chef-blogs/$', views.chef_blogs, name='chef_blogs'),
    re_path(r'^chef-courses/$', views.chef_courses, name='chef_courses'),
    path('search/', views.search, name='search'),
    path('add-vlog/', views.add_post, name='add_post'),
    path('delete-vlog/<int:id>/', views.delete_post, name='delete_post'),
    path('entertainment/', views.posts, name='all_posts'),
]
