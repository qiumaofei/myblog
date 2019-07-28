# _*_coding:utf-8_*_
import re

from django import forms
from django.forms import widgets

# class RegisterForm(forms.Form):
# 	pass
from users.models import UserProfile


class RegisterForm(forms.ModelForm):
	# 添加自定义的属性
	repassword = forms.CharField(widget=forms.PasswordInput, max_length=12, min_length=6, label='确认密码')

	# 通过元类引用模型属性
	class Meta:
		model = UserProfile
		# fields='__all__'   将模型中所有的字段都拿过来应用在Form中  往往结合exclude=['isdelete',]
		fields = ['username', 'email', 'phone', 'password']

		widgets = {
			'password': widgets.PasswordInput,
			'email': widgets.EmailInput
		}
		error_messages = {
			'username': {'max_length': '用户长度6~12之间', 'required': '用户名必须填写'},

		}

	# 自定义验证函数，函数的名字必须如下的定义方式： clean_字段(self)
	def clean_phone(self):
		# 此函数中就可以使用正则表达式
		phone = self.cleaned_data['phone']
		regex = r'^1[358]\d{9}$|^176\d{8}$'
		reg_obj = re.compile(regex)
		if reg_obj.match(phone):
			return phone
		else:
			raise forms.ValidationError(u'手机号码格式不正确')


class LoginForm(forms.Form):
	# class Meta:
	# 	model = UserProfile
	# 	fields = ['username', 'password']
	# 	widgets = {'password': widgets.PasswordInput, }
	username = forms.CharField(max_length=12, required=True,
							   error_messages={'max_length': '最长12位', 'required': '用户名必须填写'})
	password = forms.CharField(widget=forms.PasswordInput, max_length=12, min_length=6, required=True,
							   error_messages={'max_length': '最长12位', 'min_length': '至少6位', 'required': '用户名必须填写'})
