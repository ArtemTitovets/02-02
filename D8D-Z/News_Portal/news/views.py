from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.core.cache import cache
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from datetime import datetime
from .models import Post, Category
from .filters import PostFilter
from .forms import PostForm
from .tasks import add_new_post_task



class PostList(LoginRequiredMixin, ListView):
    model = Post
    ordering = 'heading'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}',None)  # кэш очень похож на словарь, и метод get действует так же.
                                                           # Он забирает значение по ключу, если его нет, то забирает None.
                                                           # если объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)
        return obj

class PostSearch(LoginRequiredMixin, ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'news_search.html'
    context_object_name = 'news'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class ArticlesCreate(LoginRequiredMixin,PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'articles_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.save()
        add_new_post_task.delay(post.pk)
        return super().form_valid(form)


class NewsCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'news_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.save()
        add_new_post_task.delay(post.pk)
        return super().form_valid(form)


class ArticlesUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    model = Post
    fields = ['author', 'heading', 'text']
    template_name = 'articles_update.html'

    def form_valid(self, form):
        Post = form.save(commit=False)
        Post.post = 'AR'
        return super().form_valid(form)


class NewsUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    model = Post
    fields = ['author', 'heading', 'text']
    template_name = 'news_update.html'

    def form_valid(self, form):
        Post = form.save(commit=False)
        Post.post = 'NE'
        return super().form_valid(form)


class ArticlesDelete(LoginRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'articles_delete.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        Post = form.save(commit=False)
        Post.post = 'AR'
        return super().form_valid(form)


class NewsDelete(LoginRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        Post = form.save(commit=False)
        Post.post = 'NE'
        return super().form_valid(form)


class CategoryView(ListView):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category)
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # category = get_object_or_404(Category, id=self.kwargs['pk'])
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)
    message = 'Вы успешно подписались на категорию'

    return render(request, 'subscribe.html', {'category': category, 'message': message})

