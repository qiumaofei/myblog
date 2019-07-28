from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

# 文章详情页
from articles.models import ArticleTag, Article, Tag, CommentInfo


def article_detail(request, aid):
	# 所有文章
	articles = Article.objects.all().order_by('-add_time')
	# 点击量
	click_articles = Article.objects.all().order_by('-click_num')[:6]
	# 评论量
	comment_articles = Article.objects.all().order_by('-comment_num')[:6]
	# 站长推荐（点赞数）
	love_articles = Article.objects.all().order_by('-love_num')[:6]

	# 查询标签
	tags = Tag.objects.all().order_by('-add_time')
	cursor = connection.cursor()
	cursor.execute("select distinct date_format(add_time,'%Y-%m') as col_date from article")
	rows = cursor.fetchall()
	# print(row)
	archives = [row[0].split('-') for row in rows]  # ['2018-02','2018-03']
	# 获取tagid
	tagid = request.GET.get('tagid', '')
	print('tagid:', tagid)
	# 标签云
	if tagid:
		article_tags = ArticleTag.objects.filter(tag_id=tagid)
		articles = [article_tag.article for article_tag in article_tags]
	# 获取年和月  归档
	year = request.GET.get('year', '')
	month = request.GET.get('month', '')
	print(year, month)

	if year and month:
		articles = Article.objects.filter(add_time__contains=year + '-' + month)

	# 获取文章
	article = Article.objects.get(pk=aid)
	article.click_num += 1
	article.save()

	# 评论的分页
	comments = article.commentinfo_set.all()

	# 设置每页的数量
	paginator = Paginator(comments, 4)
	# 传递页码数
	page_number = request.GET.get('cpage', 1)
	print('page_number', page_number)
	# 获取该页码的内容
	try:
		comments = paginator.page(page_number)
	except EmptyPage:
		comments = paginator.page(1)
	except PageNotAnInteger:
		comments = paginator.page(int(page_number))

	return render(request, 'article.html', context={'click_articles': click_articles,
													'comment_articles': comment_articles,
													'love_articles': love_articles, 'tags': tags,
													'archives': archives, 'article': article,
													'current_page': page_number, 'comments': comments})


# 文章评论
# @login_required
def comment(request):
	if request.method == 'POST':
		comment_content = request.POST.get('comment')
		articleid = request.POST.get('articleid')
		# print(request.user.id)
		comment = CommentInfo.objects.create(content=comment_content, comment_article_id=articleid,
											 comment_person_id=request.user.id)

		return redirect(reverse('articles:article_detail', kwargs={'aid': articleid}))


# 添加文章
def add_article(request):
	return HttpResponse('文章添加成功！')


# def test(request):
# 	print("------>test函数")
# 	aa = 1 / 0
# 	return render(request, 'test.html')

# 评论点赞的函数
def comment_love(request):
	comment_id = request.GET.get('commentid')
	comment = CommentInfo.objects.get(pk=comment_id)
	comment.love_num += 1
	comment.save()
	return JsonResponse({'status': '200', 'love': comment.love_num})
