# ==================== urls.py ====================
# blogs/urls.py

from django.urls import path
from . import views

app_name = 'blogs'
urlpatterns = [
    # 主页
    path('', views.index, name='index'),
    # 文章详情
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    # 创建新文章
    path('new_post/', views.new_post, name='new_post'),
    # 编辑文章
    path('edit_post/<int:post_id>/', views.edit_post, name='edit_post'),
    # 删除文章
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
]

