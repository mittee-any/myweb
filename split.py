import zipfile
import os

# 定义文件内容
files_content = {
    "blogs/templates/blogs/base.html": """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}我的博客{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            padding-top: 60px;
            padding-bottom: 40px;
        }
        .post-meta {
            color: #6c757d;
            font-size: 0.9rem;
        }
        .post-card {
            margin-bottom: 20px;
            transition: transform 0.2s;
        }
        .post-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary fixed-top">
        <div class="container">
            <a class="navbar-brand" href="{% url 'blogs:index' %}">我的博客</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'blogs:index' %}">主页</a>
                    </li>
                    {% if user.is_authenticated %}
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'blogs:new_post' %}">写文章</a>
                        </li>
                        <li class="nav-item">
                            <span class="nav-link">你好，{{ user.username }}！</span>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'users:logout' %}">登出</a>
                        </li>
                    {% else %}
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'users:register' %}">注册</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'users:login' %}">登录</a>
                        </li>
                    {% endif %}
                </ul>
            </div>
        </div>
    </nav>

    <div class="container">
        {% block content %}{% endblock %}
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>""",

    "blogs/templates/blogs/index.html": """{% extends 'blogs/base.html' %}

{% block title %}主页 - 我的博客{% endblock %}

{% block content %}
<div class="row">
    <div class="col-lg-8 mx-auto">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h1>所有文章</h1>
            {% if user.is_authenticated %}
                <a href="{% url 'blogs:new_post' %}" class="btn btn-primary">写新文章</a>
            {% endif %}
        </div>

        {% if posts %}
            {% for post in posts %}
            <div class="card post-card">
                <div class="card-body">
                    <h2 class="card-title">
                        <a href="{% url 'blogs:post_detail' post.id %}" class="text-decoration-none">
                            {{ post.title }}
                        </a>
                    </h2>
                    <p class="post-meta">
                        由 <strong>{{ post.owner.username }}</strong> 发表于
                        {{ post.date_added|date:"Y年m月d日 H:i" }}
                    </p>
                    <p class="card-text">
                        {{ post.text|truncatewords:50|linebreaks }}
                    </p>
                    <a href="{% url 'blogs:post_detail' post.id %}" class="btn btn-sm btn-outline-primary">
                        阅读更多
                    </a>
                </div>
            </div>
            {% endfor %}
        {% else %}
            <div class="alert alert-info">
                <h4>还没有文章</h4>
                <p>
                    {% if user.is_authenticated %}
                        <a href="{% url 'blogs:new_post' %}">写第一篇文章</a>吧！
                    {% else %}
                        请<a href="{% url 'users:login' %}">登录</a>后开始写作。
                    {% endif %}
                </p>
            </div>
        {% endif %}
    </div>
</div>
{% endblock %}""",

    "blogs/templates/blogs/post_detail.html": """{% extends 'blogs/base.html' %}

{% block title %}{{ post.title }} - 我的博客{% endblock %}

{% block content %}
<div class="row">
    <div class="col-lg-8 mx-auto">
        <article>
            <h1 class="mb-3">{{ post.title }}</h1>
            <p class="post-meta mb-4">
                由 <strong>{{ post.owner.username }}</strong> 发表于
                {{ post.date_added|date:"Y年m月d日 H:i" }}
            </p>

            {% if user == post.owner %}
            <div class="mb-3">
                <a href="{% url 'blogs:edit_post' post.id %}" class="btn btn-sm btn-warning">编辑</a>
                <a href="{% url 'blogs:delete_post' post.id %}" class="btn btn-sm btn-danger">删除</a>
            </div>
            {% endif %}

            <div class="card">
                <div class="card-body">
                    {{ post.text|linebreaks }}
                </div>
            </div>

            <div class="mt-4">
                <a href="{% url 'blogs:index' %}" class="btn btn-secondary">返回主页</a>
            </div>
        </article>
    </div>
</div>
{% endblock %}""",

    "blogs/templates/blogs/new_post.html": """{% extends 'blogs/base.html' %}

{% block title %}写新文章 - 我的博客{% endblock %}

{% block content %}
<div class="row">
    <div class="col-lg-8 mx-auto">
        <h1 class="mb-4">写新文章</h1>

        <div class="card">
            <div class="card-body">
                <form method="post" action="{% url 'blogs:new_post' %}">
                    {% csrf_token %}

                    <div class="mb-3">
                        {{ form.title.label_tag }}
                        {{ form.title }}
                        {% if form.title.errors %}
                            <div class="text-danger">{{ form.title.errors }}</div>
                        {% endif %}
                    </div>

                    <div class="mb-3">
                        {{ form.text.label_tag }}
                        {{ form.text }}
                        {% if form.text.errors %}
                            <div class="text-danger">{{ form.text.errors }}</div>
                        {% endif %}
                    </div>

                    <button type="submit" class="btn btn-primary">发表文章</button>
                    <a href="{% url 'blogs:index' %}" class="btn btn-secondary">取消</a>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}""",

    "blogs/templates/blogs/edit_post.html": """{% extends 'blogs/base.html' %}

{% block title %}编辑文章 - 我的博客{% endblock %}

{% block content %}
<div class="row">
    <div class="col-lg-8 mx-auto">
        <h1 class="mb-4">编辑文章</h1>

        <div class="card">
            <div class="card-body">
                <form method="post" action="{% url 'blogs:edit_post' post.id %}">
                    {% csrf_token %}

                    <div class="mb-3">
                        {{ form.title.label_tag }}
                        {{ form.title }}
                        {% if form.title.errors %}
                            <div class="text-danger">{{ form.title.errors }}</div>
                        {% endif %}
                    </div>

                    <div class="mb-3">
                        {{ form.text.label_tag }}
                        {{ form.text }}
                        {% if form.text.errors %}
                            <div class="text-danger">{{ form.text.errors }}</div>
                        {% endif %}
                    </div>

                    <button type="submit" class="btn btn-primary">保存更改</button>
                    <a href="{% url 'blogs:post_detail' post.id %}" class="btn btn-secondary">取消</a>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}""",

    "blogs/templates/blogs/delete_post.html": """{% extends 'blogs/base.html' %}

{% block title %}删除文章 - 我的博客{% endblock %}

{% block content %}
<div class="row">
    <div class="col-lg-6 mx-auto">
        <h1 class="mb-4">删除文章</h1>

        <div class="alert alert-warning">
            <h4>确定要删除这篇文章吗？</h4>
            <p><strong>{{ post.title }}</strong></p>
            <p class="mb-0">此操作不可撤销！</p>
        </div>

        <form method="post" action="{% url 'blogs:delete_post' post.id %}">
            {% csrf_token %}
            <button type="submit" class="btn btn-danger">确认删除</button>
            <a href="{% url 'blogs:post_detail' post.id %}" class="btn btn-secondary">取消</a>
        </form>
    </div>
</div>
{% endblock %}""",

    "users/templates/registration/login.html": """{% extends 'blogs/base.html' %}

{% block title %}登录 - 我的博客{% endblock %}

{% block content %}
<div class="row">
    <div class="col-md-6 mx-auto">
        <h2 class="mb-4">登录</h2>

        {% if form.errors %}
        <div class="alert alert-danger">
            用户名或密码不正确，请重试。
        </div>
        {% endif %}

        <div class="card">
            <div class="card-body">
                <form method="post" action="{% url 'users:login' %}">
                    {% csrf_token %}
                    {{ form.as_p }}
                    <button type="submit" class="btn btn-primary">登录</button>
                    <input type="hidden" name="next" value="{% url 'blogs:index' %}" />
                </form>
            </div>
        </div>

        <p class="mt-3">
            还没有账号？<a href="{% url 'users:register' %}">点击注册</a>
        </p>
    </div>
</div>
{% endblock %}""",

    "users/templates/registration/register.html": """{% extends 'blogs/base.html' %}

{% block title %}注册 - 我的博客{% endblock %}

{% block content %}
<div class="row">
    <div class="col-md-6 mx-auto">
        <h2 class="mb-4">注册新账号</h2>

        <div class="card">
            <div class="card-body">
                <form method="post" action="{% url 'users:register' %}">
                    {% csrf_token %}
                    {{ form.as_p }}
                    <button type="submit" class="btn btn-primary">注册</button>
                </form>
            </div>
        </div>

        <p class="mt-3">
            已有账号？<a href="{% url 'users:login' %}">点击登录</a>
        </p>
    </div>
</div>
{% endblock %}"""
}

# 创建 zip 文件
zip_filename = "django_blog_templates.zip"
with zipfile.ZipFile(zip_filename, 'w') as zipf:
    for file_path, content in files_content.items():
        # 写入文件，zipfile 会自动处理路径
        zipf.writestr(file_path, content)

print(f"File {zip_filename} created.")