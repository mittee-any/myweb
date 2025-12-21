# ==================== models.py ====================
# blogs/models.py

from django.db import models
from django.contrib.auth.models import User


class BlogPost(models.Model):
    """博客文章模型"""
    title = models.CharField(max_length=200, verbose_name='标题')
    text = models.TextField(verbose_name='正文')
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='添加日期')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')

    class Meta:
        verbose_name = '博客文章'
        verbose_name_plural = '博客文章'
        ordering = ['-date_added']

    def __str__(self):
        return self.title if len(self.title) <= 50 else f"{self.title[:50]}..."

