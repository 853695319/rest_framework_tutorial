from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', views.SnippetList.as_view()),
    path('<int:pk>/', views.SnippetDetail.as_view()),
    path('<int:pk>/highlight/', views.SnippetHighlight.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
