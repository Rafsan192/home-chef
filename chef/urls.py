from django.urls import path, re_path

from chef import views

urlpatterns = [
    path('', views.index),
    path('my-blogs/', views.my_blogs, name='my_blogs'),
    path('my-courses/', views.my_courses, name='my_courses'),
    path('my-students/', views.my_students, name='my_students'),
    re_path(r'^update-course/$', views.update_course, name='update_course'),
    re_path(r'^delete-course/$', views.delete_course, name='delete_course'),
    re_path(r'^update-blog/$', views.update_blog, name='update_blog'),
    re_path(r'^delete-blog/$', views.delete_blog, name='delete_blog'),
    re_path(r'^update-enrollment/$', views.update_enroll, name='update_enrollment'),
]
