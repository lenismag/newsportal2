from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django_filters.views import FilterView
from .models import Post, Author, Category
from .forms import PostForm
from .filters import PostFilter


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


class NewsCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'news/post_form.html'
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'news'
        post.author = Author.objects.get(user=self.request.user)
        return super().form_valid(form)


class NewsUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'news/post_form.html'

    def get_success_url(self):
        return reverse_lazy('news_detail', kwargs={'pk': self.object.pk})


class NewsDeleteView(LoginRequiredMixin, DeleteView):
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