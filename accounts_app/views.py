from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

def home(request):
    return render(request, 'home.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['ID']
        password = request.POST['PW']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            context = {'error':'존재하지 않는 회원이거나 비밀번호를 확인해주세요!'}
            return render(request, 'login.html', context)
    elif request.method == 'GET':
        return render(request, 'login.html')

@login_required
def logout(request):
    auth.logout(request)
    return redirect('home')

def signup(request):
    if request.method == "POST":
        username = request.POST['ID']
        try:
            find_user = User.objects.get(username=username)
            context = {'error':'이미 존재하는 username입니다. 다른 username을 사용해주세요!', 'ID':username}
            return render(request, 'signup.html', context)
        except ObjectDoesNotExist:
            password1 = request.POST['PW1']
            password2 = request.POST['PW2']
            if password1 == password2:
                user = User.objects.create_user(username=username, password=password1)
                return render(request, 'signup_congratulation.html')
            else:
                context = {'error':'password 입력과 password 확인 입력을 다시 확인해주세요!'}
                return render(request, 'signup.html', context)
    else:
        return render(request, 'signup.html')