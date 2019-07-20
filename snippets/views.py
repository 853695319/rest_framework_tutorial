"""
Request对象的核心功能是request.data属性，它与request.POST类似，但对于使用Web API更为有用。
request.POST  # 只处理表单数据  只适用于'POST'方法
request.data  # 处理任意数据  适用于'POST'，'PUT'和'PATCH'方法

REST框架还引入了一个Response对象，这是一种获取未渲染（unrendered）内容的TemplateResponse类型，并使用内容协商来确定返回给客户端的正确内容类型。
return Response(data)  # 渲染成客户端请求的内容类型。

注意，我们不再显式地将请求或响应绑定到给定的内容类型。
request.data可以处理传入的json请求，但它也可以处理其他格式。
同样，我们返回带有数据的响应对象，但允许REST框架将响应给我们渲染成正确的内容类型。
"""
from rest_framework import generics

from .models import Snippet
from .serializers import SnippetModelSerializer, UserModelSerializer

from django.contrib.auth.models import User
from rest_framework import permissions


class SnippetList(generics.ListCreateAPIView):
    """列出所有code snippet，或创建一个新的snippet。"""
    queryset = Snippet.objects.all()
    serializer_class = SnippetModelSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        """修改实例保存方法，并处理传入请求或请求URL中隐含的任何信息"""
        serializer.save(owner=self.request.user)
        # 序列化器的`create()`方法现在讲被传递一个附加的`owner`字段以及来自请求的验证数据。


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    """获取，更新或删除一个 code snippet。"""
    queryset = Snippet.objects.all()
    serializer_class = SnippetModelSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class UserList(generics.ListAPIView):
    """用户展示为只读视图"""
    queryset = User.objects.all()
    serializer_class = UserModelSerializer


class UserDetail(generics.RetrieveAPIView):
    """用户展示为只读视图"""
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
