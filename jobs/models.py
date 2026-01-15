from django.db import models
from users.models import User


class Job(models.Model):
    """职位模型"""
    
    company_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='jobs',
        verbose_name='公司用户',
        help_text='发布职位的公司用户'
    )
    
    title = models.CharField(
        max_length=200,
        verbose_name='职位标题'
    )
    
    requirement = models.TextField(
        verbose_name='职位要求'
    )
    
    duty = models.TextField(
        verbose_name='职位职责'
    )
    
    salary = models.CharField(
        max_length=100,
        verbose_name='薪资',
        help_text='薪资范围或金额'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间'
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='更新时间'
    )
    
    class Meta:
        db_table = 'jobs'
        verbose_name = '职位'
        verbose_name_plural = '职位'
        ordering = ['-created_at']  # 按创建时间倒序
        indexes = [
            models.Index(fields=['company_user']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return f'{self.title} - {self.company_user.nickname}'
