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
from .models import Snippet
from .serializers import SnippetModelSerializer
from rest_framework import mixins, generics


class SnippetList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    """列出所有code snippet，或创建一个新的snippet。"""
    queryset = Snippet.objects.all()
    serializer_class = SnippetModelSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)  # mixins.ListModelMixin

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)  # mixins.CreateModelMixin


class SnippetDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    """获取，更新或删除一个 code snippet。"""
    queryset = Snippet.objects.all()
    serializer_class = SnippetModelSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)  # mixins.RetrieveModelMixin

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)  # mixins.UpdateModelMixin

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)  # mixins.DestroyModelMixin
