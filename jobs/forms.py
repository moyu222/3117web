from django import forms
from .models import Job


class JobForm(forms.ModelForm):
    """职位表单"""
    
    class Meta:
        model = Job
        fields = ['title', 'requirement', 'duty', 'salary']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入职位标题'
            }),
            'requirement': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': '请输入职位要求'
            }),
            'duty': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': '请输入职位职责'
            }),
            'salary': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入薪资（如：10k-20k）'
            }),
        }
        labels = {
            'title': '职位标题',
            'requirement': '职位要求',
            'duty': '职位职责',
            'salary': '薪资',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 所有字段都设为必填
        for field in self.fields.values():
            field.required = True
