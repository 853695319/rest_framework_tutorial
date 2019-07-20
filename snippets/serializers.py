"""
a Serializer class which gives you a powerful, generic way to control the output of your responses,
a ModelSerializer class which provides a useful shortcut for creating serializers that deal with model instances and querysets.
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES


class SnippetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    code = serializers.CharField(style={'base_template': 'textarea.html'})
    linenos = serializers.BooleanField(required=False)
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
    style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')

    def create(self, validated_data):
        """根据提供的验证过的数据创建并返回一个新的`Snippet`实例"""
        return Snippet.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """根据提供的验证过的数据更新并返回一个已经存在的`Snippet`实例"""
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('style', instance.style)
        instance.save()
        return instance


"""
>>> from snippets.models import Snippet
>>> from snippets.serializers import SnippetSerializer
>>> from rest_framework.renderers import JSONRenderer
>>> from rest_framework.parsers import JSONParser
>>> snippet = Snippet(code='foo = "bar"\n')
>>> snippet.save()
>>> snippet = Snippet(code='print "hello, world"\n')
>>> snippet.save()
# 序列化
>>> serializer = SnippetSerializer(snippet)
>>> serializer.data
{'id': 2, 'title': '', 'code': 'print "hello, world"\n', 'linenos': False, 'language': 'python', 'style': 'friendly'}
# 将模型实例转换为Python原生数据类型
>>> content = JSONRenderer().render(serializer.data)
>>> content
b'{"id":2,"title":"","code":"print \\"hello, world\\"\\n","linenos":false,"language":"python","style":"friendly"}'
# 反序列化
# 将一个流（stream)解析为python原生数据类型
>>> import io
>>> stream = io.BytesIO(content)
>>> data = JSONParser().parse(stream)
>>> serializer = SnippetSerializer(data=data)
>>> serializer.is_valid()
True
>>> serializer.validated_data
OrderedDict([('title', ''), ('code', 'print "hello, world"'), ('linenos', False), ('language', 'python'), ('style', 'friendly')])
>>> serializer.save()

# 序列化查询结果集（querysets）而不是模型实例
>>> serializer = SnippetSerializer(Snippet.objects.all(), many=True)
>>> serializer.data
"""


class SnippetModelSerializer(serializers.ModelSerializer):
    """ModelSerializer类并不会做任何特别神奇的事情， 他们只是创建序列化器类的快捷方式：
    1. 一组自动确定的字段
    2. 默认简单实现的create()和update()方法"""

    owner = serializers.ReadOnlyField(source='owner.username')
    """
    `source` 参数控制哪个属性用于填充字段，并且可以指向序列化实例上的任何属性。
    它可以采用如上所示点加下划线的方式
    在这种情况下，它将以与Django模板语言一起使用的相似方式遍历给定的属性。
    
    `ReadOnlyField`区别于其他类型字段（如`CharField`, `BooleanField`等）。
    无类型的`ReadOnlyField`始终是只读的，只能用于序列化表示，不能用于在反序列化时更新模型。
    我们也可以在这里使用`CharField(read_only=True)`
    """

    class Meta:
        model = Snippet
        fields = ('id', 'title', 'code', 'linenos', 'language', 'style', 'owner')


class UserModelSerializer(serializers.ModelSerializer):
    snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())
    # !! 由于`snippets`在用户模型中是一个反向关联的关系。在使用`ModelSerializer`类时它默认不会被包含，
    # 所以我们需要为它添加一个显式字段
    # 定义model时，可以在ForeignKey 定义时设置related_name 参数来覆盖FOO_set 的名称

    class Meta:
        model = User
        fields = ('id', 'username', 'snippets')  # ForeignKey.related_name=snippets


if __name__ == "__main__":
    import doctest
    doctest.testmod()
