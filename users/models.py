from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class User(models.Model):
    """用户模型 - 完全自定义，不继承任何基类"""
    
    USER_TYPE_CHOICES = [
        ('company', '公司'),
        ('individual', '个人'),
    ]
    
    login_id = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='登录ID',
        help_text='用于登录的唯一标识'
    )
    
    password = models.CharField(
        max_length=128,
        verbose_name='密码'
    )
    
    nickname = models.CharField(
        max_length=150,
        verbose_name='昵称'
    )
    
    email = models.EmailField(
        unique=True,
        verbose_name='邮箱'
    )
    
    type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        verbose_name='用户类型'
    )
    
    profile_image = models.ImageField(
        upload_to='profile_images/',
        null=True,
        blank=True,
        verbose_name='头像'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间'
    )
    
    class Meta:
        db_table = 'users'
        verbose_name = '用户'
        verbose_name_plural = '用户'
        indexes = [
            models.Index(fields=['login_id']),
            models.Index(fields=['email']),
        ]
    
    def __str__(self):
        return f'{self.login_id} ({self.nickname})'
    
    def set_password(self, raw_password):
        """设置密码（使用 Django 的 PBKDF2 哈希）"""
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        """验证密码"""
        return check_password(raw_password, self.password)
    
    def is_company(self):
        """判断是否为公司用户"""
        return self.type == 'company'
    
    def is_individual(self):
        """判断是否为个人用户"""
        return self.type == 'individual'
    
    # 为了兼容 Django 的认证系统，添加这些属性
    @property
    def is_authenticated(self):
        """用于检查用户是否已认证"""
        return True
    
    @property
    def is_anonymous(self):
        """用于检查用户是否匿名"""
        return False