from django.urls import path
from .views import (PostList, PostDetail, PostSearch, ArticlesCreate, NewsCreate, ArticlesUpdate, NewsUpdate,
                    ArticlesDelete, NewsDelete, CategoryView, subscribe)
from django.views.decorators.cache import cache_page

urlpatterns = [path('', cache_page(60*1) (PostList.as_view()), name='post_list'),
               path('<int:pk>', PostDetail.as_view(), name='news_detail'),
               path('search/', PostSearch.as_view(), name='news_search'),
               path('articles/create/', ArticlesCreate.as_view(), name='articles_create'),
               path('news/create/', NewsCreate.as_view(), name='news_create'),
               path('articles/<int:pk>/update/', ArticlesUpdate.as_view(), name='articles_update'),
               path('news/<int:pk>/update/', NewsUpdate.as_view(), name='news_update'),
               path('articles/<int:pk>/delete/', ArticlesDelete.as_view(), name='articles_delete'),
               path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
               path('categories/<int:pk>/', CategoryView.as_view(), name='category_list'),
               path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
               ]
