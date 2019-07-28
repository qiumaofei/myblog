from django.contrib import admin

# Register your models here.
from articles.models import Article, ArticleCategory


# 方式二
@admin.register(ArticleCategory)
class ArticleCategoryAdmin(admin.ModelAdmin):
	list_display = ('id', 'name')
	list_filter = ('id',)
	search_fields = ('name',)


class ArticleAdmin(admin.ModelAdmin):
	list_display = ('title', 'desc', 'click_num', 'comment_num')
	list_filter = ('author', 'category')
	list_display_links = ('title', 'desc')
	search_fields = ('title',)
	list_editable = ('click_num', 'comment_num')
	list_per_page = 2


# 方式一
admin.site.register(Article, ArticleAdmin)
