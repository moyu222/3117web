from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist
from .forms import LoginForm, RegisterForm
from .models import User


def get_current_user(request):
    """从 session 中获取当前登录的用户"""
    user_id = request.session.get('user_id')
    if user_id:
        try:
            return User.objects.get(id=user_id)
        except ObjectDoesNotExist:
            return None
    return None


@require_http_methods(["GET", "POST"])
def login_view(request):
    """登录视图"""
    # 如果已登录，重定向到首页（中间件已处理过期检查）
    user_id = request.session.get('user_id')
    if user_id:
        try:
            User.objects.get(id=user_id)
            return redirect('home')
        except (User.DoesNotExist, ValueError):
            pass
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            login_id = form.cleaned_data['login_id']
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data.get('remember_me', False)
            
            try:
                # 查找用户
                user = User.objects.get(login_id=login_id)
                
                # 验证密码
                if user.check_password(password):
                    # 将用户 ID 存入 session
                    request.session['user_id'] = user.id
                    
                    # 根据 remember_me 设置 session 过期时间
                    if remember_me:
                        # 设置 30 天过期（逻辑过期）
                        request.session.set_expiry(30 * 24 * 3600)  # 30天
                    else:
                        # 未勾选记住我时，设置为 2 小时过期
                        request.session.set_expiry(2 * 3600)  # 2小时
                    
                    messages.success(request, f'欢迎回来，{user.nickname}！')
                    return redirect('home')
                else:
                    messages.error(request, '登录ID或密码错误，请重试。')
            except ObjectDoesNotExist:
                messages.error(request, '登录ID或密码错误，请重试。')
    else:
        form = LoginForm()
    
    return render(request, 'users/login.html', {'form': form})


@require_http_methods(["POST"])
def logout_view(request):
    """登出视图"""
    # 清除 session 中的用户信息
    if 'user_id' in request.session:
        del request.session['user_id']
    # 清除所有 session 数据
    request.session.flush()
    messages.success(request, '您已成功登出。')
    return redirect('users:login')


@require_http_methods(["GET", "POST"])
def register_view(request):
    """注册视图"""
    # 如果已登录，重定向到首页
    user_id = request.session.get('user_id')
    if user_id:
        try:
            User.objects.get(id=user_id)
            return redirect('home')
        except (User.DoesNotExist, ValueError):
            pass
    
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            # 创建新用户
            user = User()
            user.login_id = form.cleaned_data['login_id']
            user.set_password(form.cleaned_data['password'])  # 使用 PBKDF2 哈希（加盐）存储
            user.nickname = form.cleaned_data['nickname']
            user.email = form.cleaned_data['email']
            user.type = form.cleaned_data['type']
            
            # 处理头像上传
            if 'profile_image' in request.FILES:
                user.profile_image = request.FILES['profile_image']
            
            user.save()
            
            messages.success(request, f'注册成功！欢迎加入，{user.nickname}！请登录。')
            return redirect('users:login')
    else:
        form = RegisterForm()
    
    return render(request, 'users/register.html', {'form': form})


def home_view(request):
    """首页视图"""
    # 获取当前用户（通过上下文处理器，模板中可以直接使用 user）
    return render(request, 'home.html')
