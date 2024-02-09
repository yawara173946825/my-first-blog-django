from django.db.models import Count, Q
from django.http import Http404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404

from blog.models import Post, Category, Tag


# ブログ記事の詳細情報を表示するためのビュー
class PostDetailView(DetailView):
    model = Post

    # オーバーライドした get_object メソッド
    def get_object(self, queryset=None):
        # 親クラスの get_object メソッドを呼び出して基本的なオブジェクトの取得処理を行う
        obj = super().get_object(queryset=queryset)

        # オブジェクトの公開状態とユーザーの認証状態を確認し、適切な例外を発生させる
        if not obj.is_public and not self.request.user.is_authenticated:
            raise Http404

        # 処理が正常に完了した場合、取得したオブジェクトを返す
        return obj

    
# ブログ記事一覧を表示するためのビュー
class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'

# カテゴリ一覧（記事数）を表示するためのビュー
class CategoryListView(ListView):
    queryset = Category.objects.annotate(
        num_posts=Count('post', filter=Q(post__is_public=True))
    )


# タグ一覧（記事数）を表示するためのビュー
class TagListView(ListView):
    queryset = Tag.objects.annotate(num_posts=Count(
        'post', filter=Q(post__is_public=True)))


class CategoryPostView(ListView):
    model = Post
    template_name = 'blog/category_post.html'

    def get_queryset(self):
        category_slug = self.kwargs['category_slug']
        self.category = get_object_or_404(Category, slug=category_slug)
        qs = super().get_queryset().filter(category=self.category)
        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context
    
class TagPostView(ListView):
    model = Post
    template_name = 'blog/tag_post.html'

    def get_queryset(self):
        tag_slug = self.kwargs['tag_slug']
        self.tag = get_object_or_404(Tag, slug=tag_slug)
        qs = super().get_queryset().filter(tags=self.tag)
        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        return context