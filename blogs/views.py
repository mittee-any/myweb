# ==================== views.py ====================
# blogs/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .models import BlogPost
from .forms import NewPostForm,EditPostForm


def index(request):
    """主页 - 显示所有博客文章"""
    posts = BlogPost.objects.all()
    context = {'posts': posts}
    return render(request, 'blogs/index.html', context)


def post_detail(request, post_id):
    """文章详情页"""
    post = get_object_or_404(BlogPost, id=post_id)
    context = {'post': post}
    return render(request, 'blogs/post_detail.html', context)


@login_required
def new_post(request):
    """创建新文章"""
    if request.method != 'POST':
        # 显示空表单
        form = NewPostForm()
    else:
        # 处理提交的数据
        form = NewPostForm(data=request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.owner = request.user
            new_post.save()
            return redirect('blogs:index')

    context = {'form': form}
    return render(request, 'blogs/new_post.html', context)


@login_required
def edit_post(request, post_id):
    """编辑现有文章"""
    post = get_object_or_404(BlogPost, id=post_id)

    # 确保用户正在编辑自己的文章
    if post.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # 显示包含当前文章内容的表单
        form = EditPostForm(instance=post)
    else:
        # 处理提交的数据
        form = EditPostForm(instance=post, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('blogs:post_detail', post_id=post.id)

    context = {'post': post, 'form': form}
    return render(request, 'blogs/edit_post.html', context)


@login_required
def delete_post(request, post_id):
    """删除文章"""
    post = get_object_or_404(BlogPost, id=post_id)

    # 确保用户正在删除自己的文章
    if post.owner != request.user:
        raise Http404

    if request.method == 'POST':
        post.delete()
        return redirect('blogs:index')

    context = {'post': post}
    return render(request, 'blogs/delete_post.html', context)

