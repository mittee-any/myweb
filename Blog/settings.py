import os
from pathlib import Path

# 项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent

# 安全密钥（开发环境可保留默认，生产环境需修改）
SECRET_KEY = 'django-insecure-随便写的密钥（保持默认即可）'

# 调试模式（开发环境设为 True）
DEBUG = True

ALLOWED_HOSTS = ["*",]

# 应用列表（保持你原来的，已包含 blogs、users）
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 自定义应用
    'blogs',
    'users',
]

# 关键：补充完整的中间件（解决 admin 报错）
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',  # admin 必需
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # admin 必需
    'django.contrib.messages.middleware.MessageMiddleware',  # admin 必需
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Blog.urls'

# 关键：补充模板配置（解决 admin.E403 报错）
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',  # admin 必需
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # 可选：全局模板目录
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Blog.wsgi.application'

# 数据库配置（默认 SQLite，无需修改）
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 认证相关配置
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# 语言和时区
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_TZ = True

# 静态文件配置
STATIC_URL = 'static/'

# 解决主键警告：设置默认主键类型
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 登录/登出重定向
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'