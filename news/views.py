from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth.models import Group
from django_filters.views import FilterView
from .models import Post, Author, Category
from .forms import PostForm
from .filters import PostFilter


class AuthorRequiredMixin(PermissionRequiredMixin):
    permission_required = 'news.add_post'

    def has_permission(self):
        # Проверяем, что пользователь в группе authors
        return self.request.user.groups.filter(name='authors').exists()

@method_decorator(login_required, name='dispatch')
class UpgradeToAuthor(TemplateView):
    template_name = 'news/upgrade.html'

    def post(self, request):
        user = request.user
        authors_group = Group.objects.get(name='authors')
        user.groups.add(authors_group)
        messages.success(request, 'Теперь вы автор!')
        return redirect('news_list')


class NewsList(ListView):
    model = Post
    template_name = 'news/news_list.html'
    context_object_name = 'news'
    paginate_by = 10
    queryset = Post.objects.filter(post_type='news').order_by('-created_at')


class PostDetail(DetailView):
    model = Post
    template_name = 'news/news_detail.html'
    context_object_name = 'post'


class SearchView(FilterView):
    model = Post
    template_name = 'news/search.html'
    filterset_class = PostFilter
    paginate_by = 10
    queryset = Post.objects.order_by('-created_at')


class NewsCreateView(AuthorRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'news/post_form.html'
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'news'
        post.author = Author.objects.get(user=self.request.user)
        return super().form_valid(form)


class NewsUpdateView(AuthorRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'news/post_form.html'

    def get_success_url(self):
        return reverse_lazy('news_detail', kwargs={'pk': self.object.pk})


class NewsDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'news.delete_post'
    model = Post
    template_name = 'news/post_confirm_delete.html'
    success_url = reverse_lazy('news_list')


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'news/post_form.html'
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'article'
        post.author = Author.objects.get(user=self.request.user)
        return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'news/post_form.html'

    def get_success_url(self):
        return reverse_lazy('news_detail', kwargs={'pk': self.object.pk})


class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'news/post_confirm_delete.html'
    success_url = reverse_lazy('news_list')