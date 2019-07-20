from django.urls import path
from . import views
from rest_framework import renderers

snippet_list = views.SnippetViewSet.as_view(actions={'get': 'list', 'post': 'create'})
snippet_detail = views.SnippetViewSet.as_view(actions={
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
snippet_highlight = views.SnippetViewSet.as_view(
    actions={'get': 'highlight'},
    renderer_classes=[renderers.StaticHTMLRenderer]
)


urlpatterns = [
    path('', snippet_list, name='snippet-list'),
    path('<int:pk>/', snippet_detail, name='snippet-detail'),
    path('<int:pk>/highlight/', snippet_highlight, name='snippet-highlight')
]

