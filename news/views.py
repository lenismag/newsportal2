from django.shortcuts import render, get_object_or_404
from .models import Post

def news_list(request):
    # Только новости, сортировка по дате (свежие сверху)
    news = Post.objects.filter(type='news').order_by('-created_at')
    return render(request, 'news/news_list.html', {'news': news})

def news_detail(request, pk):
    # Ищем новость по id, если не найдена или не является новостью — покажем 404
    post = get_object_or_404(Post, pk=pk, type='news')
    return render(request, 'news/news_detail.html', {'post': post})