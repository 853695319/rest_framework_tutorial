from django.urls import path, include
from rest_framework.routers import DefaultRouter
from snippets import views


# 创建路由器并注册我们的视图。
router = DefaultRouter()
router.register(prefix=r'snippets', viewset=views.SnippetViewSet)
router.register(prefix=r'users', viewset=views.UserViewSet)

# API URL现在有路由器自动确定
urlpatterns = [
    path('', include(router.urls)),
]