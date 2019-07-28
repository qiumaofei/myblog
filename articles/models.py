from datetime import datetime

from django.db import models

# Create your models here.
from users.models import UserProfile


class ArticleCategory(models.Model):
	name = models.CharField(max_length=50, verbose_name='文章类别')

	def __str__(self):
		return self.name

	class Meta:
		db_table = 'category'
		verbose_name = '文章分类表'
		verbose_name_plural = verbose_name


# 文章模型
class Article(models.Model):
	title = models.CharField(max_length=50, verbose_name='文章标题')
	desc = models.CharField(max_length=200, verbose_name='文章简介')
	content = models.TextField(verbose_name='文章内容')
	click_num = models.IntegerField(default=0, verbose_name='点击量')
	comment_num = models.IntegerField(default=0, verbose_name='评论数')
	love_num = models.IntegerField(default=0, verbose_name='点赞数')
	image = models.ImageField(max_length=100, upload_to='article/%Y/%m/%d', verbose_name='文章图片')
	add_time = models.DateTimeField(default=datetime.now, verbose_name='发表时间')
	# 建立关系模型
	author = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE)
	category = models.ForeignKey(to=ArticleCategory, on_delete=models.CASCADE)

	def __str__(self):
		return self.title

	class Meta:
		db_table = 'article'
		verbose_name = '文章表'
		verbose_name_plural = verbose_name


# 标签
class Tag(models.Model):
	name = models.CharField(max_length=20, verbose_name='标签名')
	add_time = models.DateTimeField(default=datetime.now, verbose_name='标签添加时间')

	def __str__(self):
		return self.name

	class Meta:
		db_table = 'tag'
		verbose_name = '标签表'
		verbose_name_plural = verbose_name


# 自定义关系表
class ArticleTag(models.Model):
	article = models.ForeignKey(to=Article, on_delete=models.CASCADE)  # article就是一个对象
	tag = models.ForeignKey(to=Tag, on_delete=models.CASCADE)

	def __str__(self):
		return self.article.title

	class Meta:
		unique_together = ('article', 'tag',)
		db_table = 'article_tag'
		verbose_name = '文章标签信息表'
		verbose_name_plural = verbose_name


# 评论的模型
class CommentInfo(models.Model):
	comment_person = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE)
	comment_article = models.ForeignKey(to=Article, on_delete=models.CASCADE)
	content = models.TextField(verbose_name='评论内容')
	add_time = models.DateTimeField(default=datetime.now, verbose_name='评论时间')
	love_num = models.IntegerField(default=0, verbose_name='点赞数')

	def __str__(self):
		return self.content

	class Meta:
		db_table = 'comment'
		verbose_name = '评论表'
		verbose_name_plural = verbose_name
