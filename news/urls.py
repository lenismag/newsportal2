from django.urls import path
from . import views

urlpatterns = [
    path('', views.NewsList.as_view(), name='news_list'),
    path('search/', views.SearchView.as_view(), name='news_search'),
    path('<int:pk>/', views.PostDetail.as_view(), name='news_detail'),
    path('create/', views.NewsCreateView.as_view(), name='news_create'),
    path('<int:pk>/edit/', views.NewsUpdateView.as_view(), name='news_edit'),
    path('<int:pk>/delete/', views.NewsDeleteView.as_view(), name='news_delete'),
]