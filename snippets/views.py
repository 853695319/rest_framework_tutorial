"""
Request对象的核心功能是request.data属性，它与request.POST类似，但对于使用Web API更为有用。
request.POST  # 只处理表单数据  只适用于'POST'方法
request.data  # 处理任意数据  适用于'POST'，'PUT'和'PATCH'方法

REST框架还引入了一个Response对象，这是一种获取未渲染（unrendered）内容的TemplateResponse类型，并使用内容协商来确定返回给客户端的正确内容类型。
return Response(data)  # 渲染成客户端请求的内容类型。

注意，我们不再显式地将请求或响应绑定到给定的内容类型。
request.data可以处理传入的json请求，但它也可以处理其他格式。
同样，我们返回带有数据的响应对象，但允许REST框架将响应给我们渲染成正确的内容类型。

`ViewSet` 和 `View` 几乎相同，不同之处在于`ViewSet`提供诸如`read`或`update`之类的 *操作*，
而不是`get`或`put`等 *方法处理程序*
"""
from rest_framework import generics

from .models import Snippet
from .serializers import SnippetModelSerializer, UserModelSerializer

from django.contrib.auth.models import User
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from rest_framework import renderers

from rest_framework import viewsets
from rest_framework.decorators import action


class SnippetHighlight(generics.GenericAPIView):
    """高亮显示代码片段，HTML表示"""
    queryset = Snippet.objects.all()
    renderer_classes = [renderers.StaticHTMLRenderer]

    def get(self, request, *args, **kwargs):
        """返回对象实例的属性"""
        snippet = self.get_object()
        return Response(snippet.highlighted)


@api_view(['GET'])
def api_root(request, format=None):
    """API入口"""

    # 1 使用REST框架的`reverse`功能来返回完全限定的URL
    # 2 URL模式是通过方便的名称来标识的，需要在`snippets/urls.py`中声明
    return Response(data={
        'user': reverse('user-list', request=request, format=format),
        "snippets": reverse('snippet-list', request=request, format=format)
    })


class SnippetViewSet(viewsets.ModelViewSet):
    """此视图自动提供`list`, `create`, `retrieve`, `update`和`destroy`操作

    另外我们还提供了一个额外的`highlight`操作"""
    queryset = Snippet.objects.all()
    serializer_class = SnippetModelSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    # 使用`@action`装饰器创建一个名为`highlight`的自定义*操作*
    # 这个装饰器可用于条件不符合标准`create`/`update`/`delete`样式的任何自定义路径

    # 默认情况小，使用`@action`装饰器的自定义操作将响应`GET`请求。
    # 如果我们想要一个响应`POST`请求的动作，我们可以使用`method`参数

    # 默认情况下，自定义操作的URL取决于方法名称本身。
    # 如果要更改URL的构造方式，可以为装饰器设置url_path关键字参数
    @action(detail=True, renderer_class=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """只读 此视图自动提供`list`和`detail`操作"""
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
