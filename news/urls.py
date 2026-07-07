from django.urls import path
from . import views

urlpatterns = [
    path('', views.NewsList.as_view(), name='news_list'),
    path('search/', views.SearchView.as_view(), name='news_search'),
    path('<int:pk>/', views.PostDetail.as_view(), name='news_detail'),
    path('create/', views.NewsCreateView.as_view(), name='news_create'),
    path('<int:pk>/edit/', views.NewsUpdateView.as_view(), name='news_edit'),
    path('<int:pk>/delete/', views.NewsDeleteView.as_view(), name='news_delete'),
    path('upgrade/', views.UpgradeToAuthor.as_view(), name='upgrade'),
    path('category/<int:category_id>/subscribe/', views.subscribe_to_category, name='subscribe'),
]