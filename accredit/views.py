from django.shortcuts import render, redirect
from accredit.models import User


# Create your views here.
def index(request):
    return render(request, "login/index.html", {})


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        if User.objects.filter(user_name=username).first() and User.objects.filter(password=password).first():
            return redirect('/index/')

    return render(request, 'login/login.html')


def register(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        user_name = request.POST.get('username', '')
        password = request.POST.get('password', '')
        print(email, user_name, password)
        if User.objects.filter(email=email).first():
            pass
        if User.objects.filter(user_name=user_name).first():
            pass
        user = User.objects.create(email=email, password=password, user_name=user_name)
        User.save(user)
    return render(request,'login/register.html')
