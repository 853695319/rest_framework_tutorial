"""tutorial URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('snippets.urls')),
    # 可浏览API的登录和注销视图
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
"""
rest_framework.urls
Login and logout views for the browsable API.
模式`api-auth`部分实际上可以是你要使用的任何URL。
唯一的限制是包含的URL必须使用`rest_framework`命名空间。
在Django1.9以上的版本中，REST框架将设置命名空间，因此你可以将其删除
"""
