from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.db.models import Q

# Create your views here.
from account.models import Profile
from base.models import Post
from chef.models import Blog, Course, Enroll


def index(request):
    blogs = Blog.objects.all()[:8]
    courses = Course.objects.all()[:8]
    chefs = User.objects.filter(profile__role="chef")[:8]

    context = {
        'blogs': blogs,
        'courses': courses,
        'chefs': chefs
    }
    return render(request, 'base/index.html', context)


def courses(request):
    courses = Course.objects.all()
    return render(request, 'base/all_courses.html', {'courses': courses})


def chefs(request):
    chefs = User.objects.filter(profile__role='chef')
    return render(request, 'base/all_chefs.html', {'chefs': chefs})


def all_chefs(request):
    chefs = User.objects.filter(profile__role="chef")
    return render(request, 'base/chefs.html', {'chefs': chefs})


def students(request):
    students = User.objects.filter(profile__role='student')
    return render(request, 'base/all_students.html', {'students': students})


def course(request):
    course = Course.objects.get(id=request.GET.get('course_id'))
    is_enrolled = Enroll.objects.filter(course=course, student=request.user).first()
    total_enrolled = Enroll.objects.filter(course=course).count()
    return render(request, 'base/course.html', {'course': course,
                                                'is_enrolled': is_enrolled,
                                                'total_enrolled': total_enrolled
                                                })


def blogs(request):
    blogs = Blog.objects.all()
    return render(request, 'base/all_blogs.html', {'blogs': blogs})


def blog(request):
    blog = Blog.objects.get(id=request.GET.get('blog_id'))
    return render(request, 'base/blog.html', {'blog': blog})


def add_chef(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        restaurant = request.POST.get('restaurant')
        bio = request.POST.get('bio')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        cover = request.FILES.get('cover')
        exist = User.objects.filter(username=username).first()
        if password != confirm_password:
            messages.error(request, 'Password unmatched')
            return redirect('all_chefs')
        if exist:
            messages.error(request, 'Username already exists')
            return redirect('all_chefs')
        exist = User.objects.filter(email=email).first()
        if exist:
            messages.error(request, 'Email already exists')
            return redirect('all_chefs')
        user = User.objects.create_user(username=username, password=password, email=email)
        Profile.objects.create(user=user, bio=bio, role="chef", cover=cover, restaurant=restaurant)
        messages.success(request, 'Chef added successfully')
        return redirect('all_chefs')
    return redirect('all_chefs')


def update_chef(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        restaurant = request.POST.get('restaurant')
        cover = request.FILES.get('cover')
        bio = request.POST.get('bio')
        user = User.objects.filter(id=request.GET.get('chef_id')).first()
        user.username = username
        user.email = email
        user.save()
        user.profile.restaurant = restaurant
        user.profile.bio = bio
        user.profile.save()
        profile = Profile.objects.filter(user_id=request.GET.get('chef_id')).first()
        if cover:
            profile.cover = cover
            profile.save()
        messages.success(request, 'Chef updated successfully')
        return redirect('all_chefs')
    return redirect('all_chefs')


def delete_chef(request):
    chef = User.objects.filter(id=request.GET.get('chef_id')).first()
    chef.delete()
    messages.success(request, 'Chef deleted successfully')
    return redirect('all_chefs')


def add_student(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        exist = User.objects.filter(username=username).first()
        if password != confirm_password:
            messages.error(request, 'Password unmatched')
            return redirect('all_students')
        if exist:
            messages.error(request, 'Username already exists')
            return redirect('all_students')
        exist = User.objects.filter(email=email).first()
        if exist:
            messages.error(request, 'Email already exists')
            return redirect('all_students')
        user = User.objects.create_user(username=username, password=password, email=email)
        Profile.objects.create(user=user, role="student")
        messages.success(request, 'Student added successfully')
        return redirect('all_students')
    return redirect('all_students')


def update_student(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        student = User.objects.filter(id=request.GET.get('student_id')).first()
        student.username = username
        student.email = email
        student.save()
        messages.success(request, 'Student updated successfully')
        return redirect('all_students')
    return redirect('all_students')


def delete_student(request):
    student = User.objects.filter(id=request.GET.get('student_id')).first()
    student.delete()
    messages.success(request, 'Student deleted successfully')
    return redirect('all_students')


def enroll(request):
    if request.method == 'POST':
        course_id = request.GET.get('course_id')
        banking = request.POST.get('banking')
        txn_id = request.POST.get('txn_id')
        phone = request.POST.get('phone')
        print(course_id, banking, txn_id, phone)
        Enroll.objects.create(course_id=course_id, banking=banking, txn_id=txn_id, student_id=request.user.id,
                              phone=phone)
        messages.success(request, 'Successfully submitted enrollment form')
        return redirect('home')


def my_enrolls(request):
    enrolls = Enroll.objects.filter(student=request.user)
    return render(request, 'base/my_enrolls.html', {'enrolls': enrolls})


def chef_blogs(request):
    blogs = Blog.objects.filter(writer_id=request.GET.get('chef_id'))
    return render(request, 'base/all_blogs.html', {'blogs': blogs})


def chef_courses(request):
    print(request.GET.get('chef_id'))
    courses = Course.objects.filter(mentor_id=request.GET.get('chef_id'))
    return render(request, 'base/all_courses.html', {'courses': courses})


def search(request):
    query = request.GET.get('query')
    blogs = Blog.objects.filter(title__icontains=query)
    courses = Course.objects.filter(title__contains=query)
    chefs = User.objects.filter(
        Q(username__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(
            profile__role__icontains=query))
    context = {
        'query': query,
        'blogs': blogs,
        'courses': courses,
        'chefs': chefs,
    }
    return render(request, 'base/search.html', context)


def add_post(request):
    if request.method=='GET':
        return render(request, 'base/add_post.html')
    if request.method == 'POST':
        url = request.POST.get('url')
        Post.objects.create(url=url)
        messages.success(request, 'Vlog posted successfully')
        return redirect('all_posts')


def posts(request):
    posts = Post.objects.all()
    return render(request, 'base/all_posts.html', {'posts': posts})

def delete_post(request, id):
    posts = Post.objects.filter(id=id).first()
    posts.delete()
    return redirect('all_posts')
