# news/urls_articles.py
from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.ArticleCreateView.as_view(), name='article_create'),
    path('<int:pk>/edit/', views.ArticleUpdateView.as_view(), name='article_edit'),
    path('<int:pk>/delete/', views.ArticleDeleteView.as_view(), name='article_delete'),
]