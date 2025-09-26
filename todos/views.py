from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Todo


@login_required(login_url='/login')
def home(req): 
    if req.method == 'POST':
        task = req.POST.get('task')
        if task:
            new_todo = Todo(user=req.user, todo_name=task)
            new_todo.save()
        return redirect('home')

    all_todos = Todo.objects.filter(user=req.user)
    return render(req, 'home.html', {'todos': all_todos})


def register(req):
    if req.method == 'POST':
        username = req.POST.get('username')
        email = req.POST.get('email')
        password = req.POST.get('password')
        confirm_password = req.POST.get('confirm_password')

        if not username or not email or not password or not confirm_password:
            messages.error(req, "All fields are required")
            return redirect('register')

        if len(password) < 5:
            messages.error(req, "Password must be at least 5 characters long")
            return redirect('register')
        
        if password != confirm_password:
            messages.error(req, "Passwords do not match")
            return redirect('register')
        
        if username.lower() == "admin":
            messages.error(req, "Username not allowed")
            return redirect('register')

        if User.objects.filter(Q(username=username) | Q(email=email.lower())).exists():
            messages.error(req, "Username or email already taken")
            return redirect('register')

        User.objects.create_user(username=username, email=email, password=password)

        messages.success(req, "Account created successfully! Please login.")
        return redirect('login')

    return render(req, 'register.html', {})


def login_view(req):
    if req.method == 'POST':
        username = req.POST.get('username')
        password = req.POST.get('password')

        if not username or not password:
            messages.error(req, "All fields are required")
            return redirect('login')

        user = authenticate(req, username=username, password=password)
        if user is not None:
            login(req, user)
            messages.success(req, f"Welcome back, {user.username}!")
            return redirect('home')
        else:
            messages.error(req, "Invalid credentials")
            return redirect('login')
    return render(req, 'login.html', {})

@login_required()
def logout_view(req):
    logout(req)
    messages.success(req, "Logged out successfully")
    return redirect('login')

@login_required()
def DeleteTask(req, id):
    get_todo = Todo.objects.filter(user=req.user, id = id).first()
    if get_todo:
        get_todo.delete()
    else:
        messages.error(req, "Task not found")
    return redirect('home')

@login_required()
def finish_task(req, id):
    todo_item = Todo.objects.filter(user = req.user,id=id).first()
    if todo_item:
        todo_item.status = True
        todo_item.save()
    else:
        messages.error(req, "Task not found")
    return redirect('home')