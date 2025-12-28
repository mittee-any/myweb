# ==================== forms.py ====================
# blogs/forms.py

from django import forms
from .models import BlogPost

class NewPostForm(forms.ModelForm):
    """用于发布新文章的表单"""
    class Meta:
        model = BlogPost
        fields = ['title', 'text']
        labels = {'title': '标题', 'text': '正文'}
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '输入文章标题'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'placeholder': '输入文章内容'}),
        }

class EditPostForm(forms.ModelForm):
    """用于编辑现有文章的表单（绑定 instance 进行预填充与更新）"""
    class Meta(NewPostForm.Meta):
        pass

