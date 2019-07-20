from django.urls import path
from . import views

urlpatterns = [
    path('', views.SnippetList.as_view(), name='snippet-list'),
    path('<int:pk>/', views.SnippetDetail.as_view(), name='snippet-detail'),
    path('<int:pk>/highlight/', views.SnippetHighlight.as_view(), name='snippet-highlight')
]

