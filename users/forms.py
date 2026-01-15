from django import forms
from .models import User


class LoginForm(forms.Form):
    """登录表单"""
    
    login_id = forms.CharField(
        max_length=150,
        label='登录ID',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '请输入登录ID'
        })
    )
    
    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '请输入密码'
        })
    )
    
    remember_me = forms.BooleanField(
        required=False,
        label='记住我',
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )


class RegisterForm(forms.Form):
    """注册表单"""
    
    login_id = forms.CharField(
        max_length=150,
        label='登录ID',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '请输入登录ID（唯一）'
        }),
        help_text='用于登录的唯一标识'
    )
    
    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '请输入密码',
            'id': 'register_password'
        }),
        min_length=6,
        help_text='密码至少6位'
    )
    
    password_confirm = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '请再次输入密码',
            'id': 'register_password_confirm'
        })
    )
    
    nickname = forms.CharField(
        max_length=150,
        label='昵称',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '请输入昵称'
        })
    )
    
    email = forms.EmailField(
        label='邮箱',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': '请输入邮箱地址'
        })
    )
    
    type = forms.ChoiceField(
        choices=User.USER_TYPE_CHOICES,
        label='用户类型',
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input'
        }),
        help_text='请选择您的用户类型'
    )
    
    profile_image = forms.ImageField(
        required=False,
        label='头像',
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*'
        }),
        help_text='可选，上传您的头像图片'
    )
    
    def clean_login_id(self):
        """验证 login_id 是否已存在"""
        login_id = self.cleaned_data.get('login_id')
        if User.objects.filter(login_id=login_id).exists():
            raise forms.ValidationError('该登录ID已被使用，请选择其他ID。')
        return login_id
    
    def clean_email(self):
        """验证 email 是否已存在"""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('该邮箱已被注册，请使用其他邮箱。')
        return email
    
    def clean(self):
        """验证两次密码是否一致"""
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password and password_confirm:
            if password != password_confirm:
                raise forms.ValidationError({
                    'password_confirm': '两次输入的密码不一致，请重新输入。'
                })
        
        return cleaned_data
