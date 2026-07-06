from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('news/', include('news.urls')),
    path('articles/', include('news.urls_articles')),
    path('accounts/', include('allauth.urls')),
]