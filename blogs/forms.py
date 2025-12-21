# ==================== forms.py ====================
# blogs/forms.py

from django import forms
from .models import BlogPost


class BlogPostForm(forms.ModelForm):
    """创建和编辑博客文章的表单"""

    class Meta:
        model = BlogPost
        fields = ['title', 'text']
        labels = {
            'title': '标题',
            'text': '正文'
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '输入文章标题'
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': '输入文章内容'
            })
        }
