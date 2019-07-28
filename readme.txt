知识点：
1. 创建用户时，使用默认AbstractUser
   from django.contrib.auth.models import AbstractUser
   AbstractUser的特点是：
   具备了auth_user表中的所有字段

   class UserProfile(AbstractUser):
        添加自己的属性
注意：
# 如果不添加的话则会有冲突。跟原来的auth_user冲突
AUTH_USER_MODEL = 'users.UserProfile'

作用： 用当前的UserProfile替换原来的auth_user表


2.文件上传的使用：
在定义模型的时候，可以使用ImageField或者如果不是图片可以是FileField，
image = models.ImageField(upload_to='需要上传的文件路径',max_length=100,verbose_name="")
其中upload_to会使用MEDIA_ROOT,因此还需要在settings文件中配置MEDIA_ROOT。
 配置如下：
 # 如果要设置文件上传 步骤1
MEDIA_URL = '/static/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'static/media')

upload_to后面还支持使用，%Y %m  %d的格式表示年月日

如果设置ImageField则会在数据库中保存文件的路径，在指定的MEDIA_ROOT添加上传的图片

3.使用另一种forms定义：
如果使用表单，需要表单的渲染和验证。则需要定义Form。
model与form结合起来了。

class RegisterForm(forms.ModelForm):   -----> 必须继承自ModelForm

    --------   通过元类的定义form中的字段     ------
	class Meta:
		model = UserProfile   ----》 表示form引用的模型是UserProfile
		# fields='__all__'   将模型中所有的字段都拿过来应用在Form中
		fields = ['username', 'email', 'phone', 'password']   ----》指定model中的部分字段应用在form中
		-----》指定form的中部分字段使用组件
		widgets = {
			'password': widgets.PasswordInput,   -----》表示password字段使用的是PasswordInput
			                                     -----》其中PasswordInput对应的表单是：<input type='password' name='password'/>
			'email': widgets.EmailInput   -----》 表示email字段使用的是EmailInput,是:<input type='email' name='password'/>
		}
    # 还可以自定义函数，使用正则表达式。
	# 自定义验证函数，函数的名字必须如下的定义方式： clean_字段(self)
	def clean_phone(self):
		# 此函数中就可以使用正则表达式
		phone = self.cleaned_data['phone']
		regex = r'^1[358]\d{9}$|^176\d{8}$'
		reg_obj = re.compile(regex)
		if reg_obj.match(phone):   -----》 如果验证成功则返回原来的phone
			return phone
		else:
			raise forms.ValidationError(u'手机号码格式不正确')    ------》否则抛出异常

4. model模型没有继承AbstractUser，密码加密就可以使用：make_password,  检查密码：check_password
   但是如果model继承AbstractUser，在AbstractUser中就自带了一个加密的方法set_password,检查密码的方法:check_password

5. 因为用户model继承了AbstractUser,所以在登录时候：
     user = authenticate(username=username,password=password)   ---> 鉴定函数,鉴定用户名和密码是否正确，如果正确的返回一个user对象

     匹配使用的还有：login()  logout()
     1. login(request,user)   ----> 相当于将user对象保存到session对象中

       在模板页面获取是否被认证过，
       {% if request.user.is_authenticated %}
            欢迎! {{ request.user.username }}
            <a href="{% url 'users:userlogout' %}">退出</a>
        {% else %}
            <a href="{% url 'users:login' %}">登录</a>&nbsp; &nbsp;
            <a href="{% url 'users:register' %}">注册</a>
        {% endif %}
     2. logout():退出
       logout(request)

    自定义后端：默认的authenticate只能验证username和password，如果还想验证其他的则需要自定义。

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

    然后再settings.py文件中添加（注意顺序）:

    AUTHENTICATION_BACKENDS = ['users.views.MyBackend',
						   'django.contrib.auth.backends.ModelBackend']


6.admin界面操作：
    # 方式一（推荐）
@admin.register(ArticleCategory)
class ArticleCategoryAdmin(admin.ModelAdmin):
	list_display = ('id', 'name')
	list_filter = ('id',)
	search_fields = ('name',)



class ArticleAdmin(admin.ModelAdmin):
	list_display = ('title', 'desc', 'click_num', 'comment_num')  ---》 显示的列
	list_filter = ('author', 'category')  ---》 过滤内容
	list_display_links = ('title', 'desc')  ---》可以点击的链接
	search_fields = ('title',) ---->搜索项
	list_editable = ('click_num', 'comment_num')  ----》可编辑的列
	list_per_page = 2   ----》分页操作，每页的数量
# 方式二
admin.site.register(Article, ArticleAdmin)


7.数据库查询，使用原始数据，
# 归档查询  select id,date_format(add_time,'%%Y-%%m') as date from article order by add_time
	# 方式一： id + distinct冲突  不可用
	# lists = Article.objects.raw("select id, distinct date_format(add_time,'%%Y-%%m') as col_date from article order by add_time")
	# # print(lists)
	# for l in lists:
	# 	print(l.col_date)
	# 方式二：
	cursor = connection.cursor()
	cursor.execute("select distinct date_format(add_time,'%Y-%m') as col_date from article")
	rows = cursor.fetchall()
	# print(row)
	archives = [row[0].split('-') for row in rows]  # ['2018-02','2018-03']
	print(archives)

	# 方式三：
	class ArticleManager(models.Manager):
        def distinct_date(self):
            distinct_date_list = []
            date_list = self.values('date_publish')
            for date in date_list:
                date = date['date_publish'].strftime('%Y/%m文章存档')
                if date not in distinct_date_list:
                    distinct_date_list.append(date)
            return distinct_date_list

    在Article中添加
    class Article(models.Model):
        .....

        objects= ArticleManager()

    在views.py中直接通过如下代码获取：
    archives = Article.objects.distinct_date()


    1 2018-02
    2 2018-02
    3 2018-03
    4 2018-02

  8.文件上传图片在template中使用：
  <img src="{{ MEDIA_URL }}{{ article.image }}">

  MEDIA_URL : settings.py文件中配置
  article.image: 引用的是数据库中保存的图片路径

  static/media/article/2019/02/15/s1231643.jpg

  9.分页：
    当前的页码数： current_page=2   ---->admin/?p=0
    每页的个数： per_page=2
    总条目数： 7

    有没有下一页
    有没有上一页

    两个对象：
    paginator = Paginator（articles,2） ----》分页器对象
        print(paginator.num_pages)  # 一共分的页码数
        print(paginator.count)  # 总条目数
        print(paginator.page_range)  # 页码的范围range(1,4)  --->1,2,3

    page_obj = paginator.page(1)  ----> 获取的是第一页的数据
         print(page_object.has_next())  ---》是否有下一页
         print(page_object.has_previous()) ---》是否有上一页
         print(page_object.next_page_number()) ---》获取下一页的值
         print(page_object.previous_page_number()) ----》取上一页的值

    渲染：
     page_object

     在模板中就可以使用
         print(page_object.has_next())  ---》是否有下一页
         print(page_object.has_previous()) ---》是否有上一页
         print(page_object.next_page_number()) ---》获取下一页的值
         print(page_object.previous_page_number()) ----》取上一页的值

     page_object.paginator.num_pages   --->通过page对象还可以获取分页器对象

  10.中间件
     1. 定义中间件在一个middleware的文件夹中为：mymiddleware.py

     2. 然后定义一个类继承自MiddlewareMixin

     3. 重写里面的方法：
            process_request(self,request)


     4. 激活中间件：
         在settings.py文件中的：
         MIDDLEWARE = [
            'django.middleware.security.SecurityMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
            # 激活中间件
            'middleware.mymiddleware.M1',
            'middleware.mymiddleware.M2',
        ]


11.ajax的使用：
    1. 添加jquery.min.js
    2. 自定义一个外部样式 article.js
    3. 填充
      {% block  myjs%} 引用articl.js
         <script src="{% static 'js/article.js' %}"></script>
       {%endblock%}
    4. 在article.js中添加点击动作：
        $('.love').click(function () {
//  添加ajax动作
    comment_id = $(this).attr('tag');
    a_obj = $(this)
    $.getJSON('/article/clove/', {commentid: comment_id}, function (data) {
        console.log(data);
        if (data.status == 200) {

            // console.log(a.prev())
            a_obj.prev().text('(' + data.love + ')');
        } else {
            alert('点赞失败')
        }
     });
    });

12. 富文本 缓存  手机号码  邮箱验证  xadmin 日志
    