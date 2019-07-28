from django.contrib.auth.backends import ModelBackend
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from django.db import connection  # 数据库的连接对象
# Create your views here.
from articles.models import Article, Tag, ArticleTag
from users.forms import RegisterForm, LoginForm
from users.models import UserProfile
from django.contrib.auth import authenticate, login, logout


# 自定义后端
class MyBackend(ModelBackend):
	def authenticate(self, request, username=None, password=None, phone=None):
		if username and password:
			user = super(MyBackend, self).authenticate(request, username=username, password=password)
			if user:
				return user
			else:
				if phone and password:
					user = UserProfile.objects.filter(phone=phone).first()
					if user:
						if user.check_password(password):
							return user
						else:
							raise Exception('密码错误')
					else:
						raise Exception('不存在此手机号码')
		raise Exception('用户登录失败')


def index(request):
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

	# 归档查询  select id,date_format(add_time,'%%Y-%%m') as date from article order by add_time
	# 方式一： id + distinct冲突  不可用
	# lists = Article.objects.raw("select id, distinct date_format(add_time,'%%Y-%%m') as col_date from article order by add_time")
	# # print(lists)
	# for l in lists:
	# 	print(l.col_date)
	cursor = connection.cursor()
	cursor.execute("select distinct date_format(add_time,'%Y-%m') as col_date from article")
	rows = cursor.fetchall()
	# print(row)
	archives = [row[0].split('-') for row in rows]  # ['2018-02','2018-03']
	print(archives)
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

	# 分页操作
	# 1. 构建一个分页器
	paginator = Paginator(articles, 3)
	# 2. paginator对象
	print(paginator.num_pages)  # 一共分的页码数
	print(paginator.count)  # 总条目数
	print(paginator.page_range)  # 页码的范围range(1,4)  --->1,2,3
	# 3. 获取当前的页码数

	page_number = request.GET.get('page', 1)
	print('page_number:', type(page_number))
	try:
		page_object = paginator.page(page_number)
	except EmptyPage:  # 已经是第一页了还想获取上一页
		page_object = paginator.page(1)
	except PageNotAnInteger:
		page_object = paginator.page(int(page_number))

	# print(page_object.has_next())
	# print(page_object.has_previous())
	# print(page_object.next_page_number())
	# print(page_object.previous_page_number())

	return render(request, 'index.html',
				  context={'articles': page_object, 'click_articles': click_articles,
						   'comment_articles': comment_articles,
						   'love_articles': love_articles, 'tags': tags, 'archives': archives,
						   'current_page': page_number, 'tagid': tagid, 'year': year, 'month': month})


# 用户注册
def register(request):
	if request.method == 'GET':
		return render(request, 'reg.html')
	else:
		reg_form = RegisterForm(request.POST)
		print(reg_form)
		if reg_form.is_valid():
			# 获取数据
			datas = reg_form.cleaned_data
			username = datas.get('username')
			email = datas.get('email')
			phone = datas.get('phone')
			password = datas.get('password')
			repassword = datas.get('repassword')

			# 查询数据库根据username
			user = UserProfile.objects.filter(username=username)
			if user:
				return render(request, 'reg.html', context={'msg': '此用户名已被注册'})
			else:
				if password == repassword:
					# 数据库的注册
					user = UserProfile()
					user.username = username
					user.email = email
					user.phone = phone
					user.set_password(password)
					user.save()
					return redirect(reverse('index'))
				else:
					return render(request, 'reg.html', context={'msg': '两次密码不一致'})

		else:
			return render(request, 'reg.html', context={'reg_form': reg_form})


# 登录
def user_login(request):
	if request.method == 'GET':
		return render(request, 'login.html')
	else:
		login_form = LoginForm(request.POST)
		print(login_form)
		if login_form.is_valid():
			datas = login_form.cleaned_data
			username = datas.get('username')
			password = datas.get('password')
			# 验证 用户默认继承的是AbstractUser  ---> auth_user
			# 默认使用username和password登录
			user = authenticate(username=username, password=password, phone=username)
			print("user:", user)
			if user:
				# request.session['username']=username
				login(request, user)  # 表示用户登录了，向session中添加用户名
				return redirect(reverse('index'))
		else:
			return render(request, 'login.html', context={'login_form': login_form})


# 退出用户
def user_logout(request):
	logout(request)
	return redirect(reverse('index'))
