

graph TB
    %% =======================
    %% 客户端层
    %% =======================
    subgraph Client["🌐 客户端层"]
        Browser["🖥️ 浏览器<br/>用户交互"]
    end

    %% 用明确节点替代空 subgraph，避免渲染不稳定
    HTTPGateway(("📡 HTTP<br/>Request / Response"))

    %% =======================
    %% Django 应用层
    %% =======================
    subgraph Django["🎯 Django 应用层"]
        subgraph Main["主项目配置（config/ 或 Blog/）"]
            Settings["⚙️ settings.py<br/>全局配置"]
            MainURLs["📍 urls.py<br/>主路由"]
            WSGI["🔌 wsgi.py<br/>生产服务器入口"]
            ASGI["🔌 asgi.py<br/>异步服务器入口"]
            Manage["🛠️ manage.py<br/>管理命令（项目根目录）"]
        end

        %% Django Admin（注意：/admin/ 的入口不是 blogs/admin.py）
        subgraph AdminSys["🛡️ Django Admin"]
            AdminSite["🧩 admin.site.urls<br/>后台路由入口"]
        end

        subgraph BlogsApp["📝 blogs 应用"]
            BlogsURLs["📍 blogs/urls.py<br/>博客路由"]
            BlogsViews["🎪 blogs/views.py<br/>视图集合"]
            BlogsModels["📊 blogs/models.py<br/>BlogPost 模型"]
            BlogsForms["📋 blogs/forms.py<br/>BlogPostForm"]
            BlogsAdmin["⚙️ blogs/admin.py<br/>注册模型到后台"]
        end

        subgraph UsersApp["👤 users 应用"]
            UsersURLs["📍 users/urls.py<br/>用户路由"]
            UsersViews["🎪 users/views.py<br/>register 视图"]
            AuthURLs["🔐 django.contrib.auth.urls<br/>login/logout/reset 等"]
        end

        subgraph Templates["🎨 模板层"]
            BaseHTML["📄 base.html<br/>基础模板"]
            BlogsTemplates["📄 blogs/templates/...<br/>index/post_detail/new/edit/delete"]
            AuthTemplates["📄 templates/registration/...<br/>login/register/password_reset 等"]
        end
    end

    %% =======================
    %% 数据库层
    %% =======================
    subgraph Database["🗄️ 数据库层"]
        BlogTable["📋 blogs_blogpost<br/>id, title, text<br/>date_added, owner_id"]
        UserTable["👥 auth_user<br/>id, username, password<br/>email, is_staff..."]
        SessionTable["🔑 django_session<br/>session_key, session_data"]
        AdminTable["📑 django_admin_log<br/>后台操作日志"]
    end

    %% =======================
    %% 视图函数详解（可选）
    %% =======================
    subgraph ViewFunctions["🔧 视图函数详解"]
        subgraph BlogViews["blogs 应用视图"]
            Index["index()<br/>显示所有文章"]
            PostDetail["post_detail()<br/>显示文章详情"]
            NewPost["new_post()<br/>创建新文章<br/>@login_required"]
            EditPost["edit_post()<br/>编辑文章<br/>@login_required<br/>权限检查"]
            DeletePost["delete_post()<br/>删除文章<br/>@login_required<br/>权限检查"]
        end

        subgraph UserViews["users 应用视图"]
            Register["register()<br/>用户注册<br/>UserCreationForm"]
            DjangoAuth["Django Auth Views<br/>login/logout/password_reset..."]
        end
    end

    %% =======================
    %% 请求链路：客户端 -> 路由
    %% =======================
    Browser -->|发送请求| HTTPGateway
    HTTPGateway -->|路由匹配| MainURLs

    %% 主路由分派
    MainURLs -->|/| BlogsURLs
    MainURLs -->|/users/| UsersURLs
    MainURLs -->|/admin/| AdminSite

    %% =======================
    %% blogs 应用内部路由 -> 视图
    %% =======================
    BlogsURLs -->|index| Index
    BlogsURLs -->|post/<id>/| PostDetail
    BlogsURLs -->|new_post/| NewPost
    BlogsURLs -->|edit_post/<id>/| EditPost
    BlogsURLs -->|delete_post/<id>/| DeletePost

    %% 视图与 forms/models
    Index -.->|读取列表| BlogsModels
    PostDetail -.->|查询详情| BlogsModels
    NewPost -.->|表单校验/保存| BlogsForms
    EditPost -.->|表单校验/更新| BlogsForms
    DeletePost -.->|删除| BlogsModels

    BlogsForms -->|save() / is_valid()| BlogsModels

    %% models -> DB
    BlogsModels -->|CRUD| BlogTable
    BlogsModels -->|ForeignKey owner| UserTable

    %% =======================
    %% users 应用内部路由 -> 视图
    %% =======================
    UsersURLs -->|register/| Register
    UsersURLs -->|login/| DjangoAuth
    UsersURLs -->|logout/| DjangoAuth

    Register -.->|调用| UsersViews
    DjangoAuth -.->|由 auth.urls 提供| AuthURLs

    %% 认证相关会读写 session/user
    DjangoAuth -->|登录态| SessionTable
    DjangoAuth -->|用户认证| UserTable

    %% =======================
    %% 视图 -> 模板 -> 返回响应
    %% =======================
    Index -->|render| BaseHTML
    Index -->|render| BlogsTemplates
    PostDetail -->|render| BaseHTML
    PostDetail -->|render| BlogsTemplates
    NewPost -->|render| BaseHTML
    NewPost -->|render| BlogsTemplates
    EditPost -->|render| BaseHTML
    EditPost -->|render| BlogsTemplates
    DeletePost -->|render| BaseHTML
    DeletePost -->|render| BlogsTemplates

    Register -->|render| BaseHTML
    Register -->|render| AuthTemplates
    DjangoAuth -->|render| BaseHTML
    DjangoAuth -->|render| AuthTemplates

    BaseHTML -->|返回 HTML| HTTPGateway
    BlogsTemplates -->|返回 HTML| HTTPGateway
    AuthTemplates -->|返回 HTML| HTTPGateway
    HTTPGateway -->|展示页面| Browser

    %% =======================
    %% Admin：入口、注册、日志
    %% =======================
    BlogsAdmin -->|register(ModelAdmin)| AdminSite
    AdminSite -->|管理 BlogPost| BlogsModels
    AdminSite -->|查询/修改| BlogTable
    AdminSite -->|记录操作| AdminTable

    %% =======================
    %% Settings 配置关系
    %% =======================
    Settings -->|INSTALLED_APPS| BlogsApp
    Settings -->|INSTALLED_APPS| UsersApp
    Settings -->|DATABASES| Database
    Settings -->|TEMPLATES| Templates
    Manage -->|读取配置| Settings

    %% =======================
    %% 样式（仅给节点上 class，更稳）
    %% =======================
    classDef client fill:#e3f2fd,stroke:#1565c0,stroke-width:2px,color:#000
    classDef http fill:#fff3e0,stroke:#e65100,stroke-width:2px,color:#000
    classDef config fill:#f3e5f5,stroke:#512da8,stroke-width:2px,color:#000
    classDef app fill:#fce4ec,stroke:#c2185b,stroke-width:2px,color:#000
    classDef views fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,color:#000
    classDef template fill:#e0f2f1,stroke:#00695c,stroke-width:2px,color:#000
    classDef database fill:#f1f5f9,stroke:#424242,stroke-width:2px,color:#000

    class Browser client
    class HTTPGateway http
    class Settings,MainURLs,WSGI,ASGI,Manage config
    class BlogsApp,UsersApp,BlogsURLs,UsersURLs,BlogsViews,UsersViews,BlogsForms,BlogsModels,BlogsAdmin,AuthURLs app
    class Index,PostDetail,NewPost,EditPost,DeletePost,Register,DjangoAuth views
    class BaseHTML,BlogsTemplates,AuthTemplates template
    class BlogTable,UserTable,SessionTable,AdminTable database
