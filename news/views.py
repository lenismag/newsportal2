from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.contrib import messages
from django.contrib.auth.models import Group
from django.http import JsonResponse
from django_filters.views import FilterView
from .models import Post, Author, Category
from .forms import PostForm
from .filters import PostFilter


# ==================== ПРОВЕРКА ПРАВ ====================

class AuthorRequiredMixin(PermissionRequiredMixin):
    """Миксин для проверки, что пользователь в группе authors"""
    permission_required = 'news.add_post'

    def has_permission(self):
        return self.request.user.groups.filter(name='authors').exists()


# ==================== СПИСОК НОВОСТЕЙ (ГЛАВНАЯ) ====================

@method_decorator(cache_page(60), name='dispatch')  # кэш на 1 минуту
class NewsList(ListView):
    model = Post
    template_name = 'news/news_list.html'
    context_object_name = 'news'
    paginate_by = 10
    queryset = Post.objects.filter(post_type='news').order_by('-created_at')


# ==================== ДЕТАЛЬНАЯ НОВОСТЬ ====================

@method_decorator(cache_page(300), name='dispatch')  # кэш на 5 минут
class PostDetail(DetailView):
    model = Post
    template_name = 'news/news_detail.html'
    context_object_name = 'post'

    def get_queryset(self):
        # Можно смотреть и статьи, и новости
        return Post.objects.all()


# ==================== ПОИСК ====================

class SearchView(FilterView):
    model = Post
    template_name = 'news/search.html'
    filterset_class = PostFilter
    paginate_by = 10
    queryset = Post.objects.order_by('-created_at')


# ==================== СОЗДАНИЕ НОВОСТИ ====================

class NewsCreateView(LoginRequiredMixin, AuthorRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'news/post_form.html'
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'news'
        post.author = Author.objects.get(user=self.request.user)
        return super().form_valid(form)


# ==================== РЕДАКТИРОВАНИЕ НОВОСТИ ====================

class NewsUpdateView(LoginRequiredMixin, AuthorRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'news/post_form.html'

    def get_success_url(self):
        return reverse_lazy('news_detail', kwargs={'pk': self.object.pk})


# ==================== УДАЛЕНИЕ НОВОСТИ ====================

class NewsDeleteView(LoginRequiredMixin, AuthorRequiredMixin, DeleteView):
    model = Post
    template_name = 'news/post_confirm_delete.html'
    success_url = reverse_lazy('news_list')


# ==================== СОЗДАНИЕ СТАТЬИ ====================

class ArticleCreateView(LoginRequiredMixin, AuthorRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'news/post_form.html'
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'article'
        post.author = Author.objects.get(user=self.request.user)
        return super().form_valid(form)


# ==================== РЕДАКТИРОВАНИЕ СТАТЬИ ====================

class ArticleUpdateView(LoginRequiredMixin, AuthorRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'news/post_form.html'

    def get_success_url(self):
        return reverse_lazy('news_detail', kwargs={'pk': self.object.pk})


# ==================== УДАЛЕНИЕ СТАТЬИ ====================

class ArticleDeleteView(LoginRequiredMixin, AuthorRequiredMixin, DeleteView):
    model = Post
    template_name = 'news/post_confirm_delete.html'
    success_url = reverse_lazy('news_list')


# ==================== ПОВЫШЕНИЕ ДО АВТОРА ====================

@method_decorator(login_required, name='dispatch')
class UpgradeToAuthor(TemplateView):
    template_name = 'news/upgrade.html'

    def post(self, request):
        user = request.user
        authors_group = Group.objects.get(name='authors')
        user.groups.add(authors_group)
        messages.success(request, 'Теперь вы автор!')
        return redirect('news_list')


# ==================== ПОДПИСКА НА КАТЕГОРИЮ ====================

@login_required
def subscribe_to_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    user = request.user

    if user in category.subscribers.all():
        category.subscribers.remove(user)
        subscribed = False
    else:
        category.subscribers.add(user)
        subscribed = True

    return JsonResponse({'subscribed': subscribed})