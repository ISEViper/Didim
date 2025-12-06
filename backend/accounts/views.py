from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm

# Create your views here.
def index(request):
    return render(request, 'accounts/index.html')

def login(request):
    if request.user.is_authenticated:
        return redirect('accounts:index')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)

        if form.is_valid():
            auth_login(request, form.get_user())

            return redirect('accounts:index')
    else:
        form = AuthenticationForm()
    
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)

@login_required
def logout(request):
    auth_logout(request)
    return redirect('accounts:index')


def signup(request):
    if request.user.is_authenticated:
        return redirect('accounts:index')

    if request.method == 'POST':
        # 사용자 입력 데이터를 받기(UserCreationForm을 통해서)
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:index')
    else:
        # 회원가입 폼
        form = CustomUserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)

@login_required
def delete(request):
    # 누구를 탈퇴하는지에 대한 유저 조회는 불필요
    # 유저 객체 삭제
    request.user.delete()
    return redirect('accounts:index')
