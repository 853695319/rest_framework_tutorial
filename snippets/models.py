from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
# 保存模型时，使用`pygments`代码高亮显示库填充要高亮显示的字段
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight


LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])


class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)
    # 你可以在ForeignKey 定义时设置related_name 参数来覆盖FOO_set 的名称。
    # 关联其他应用的模型 'app_name.model_name'
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='snippets')
    highlighted = models.TextField()

    class Mate:
        ordering = ['created']

    def __str__(self):
        return f"title:{self.title}, language:{self.language}"

    def save(self, *args, **kwargs):
        """使用`pygments`库创建一个高亮显示的HTML表示代码段。"""
        lexer = get_lexer_by_name(self.language)
        """
        linenos = (True and 'table') or False => or 前的语句为True,所以不执行 or 后的语句 => linenos = 'table' 
        linenos = (False and 'table') or False => or 前的语句为False,所以执行 or 后的语句 => linenos = False
        """
        linenos = self.linenos and 'table' or False
        options = self.title and {'title': self.title} or {}
        formatter = HtmlFormatter(style=self.style, linenos=linenos, full=True, **options)
        self.highlighted = highlight(self.code, lexer, formatter)
        super().save(*args, **kwargs)
