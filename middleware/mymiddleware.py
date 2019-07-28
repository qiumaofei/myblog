# _*_coding:utf-8_*_
import re

from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render, redirect, reverse
from django.utils.deprecation import MiddlewareMixin


class M1(MiddlewareMixin):
	# 处理请求
	def process_request(self, request):
		print('中间件M1...process_request')
		address = request.META['REMOTE_ADDR']
		black_list = ['10.0.121.245', '10.0.121.248', '10.0.121.230']
		if address in black_list:
			return HttpResponse('O(∩_∩)O哈哈~就不让你看....')

	def process_view(self, request, callback, callback_args, callback_kwargs):
		print('------------------>M1的process_view', callback)

	# 响应
	def process_response(self, request, response):
		# print("++++++++>哈哈哈")
		# response = HttpResponse("哈哈哈哈...")
		# return response
		response.set_cookie('a1', 'helloworld')
		print('process_response+++++++++++嘿嘿')
		return response

auth_path = ['/article/comment/', '/article/add/',]

class M2(MiddlewareMixin):
	# 处理请求
	def process_request(self, request):
		print('中间件M2...process_request')
		# 验证用户登录
		# 获取路由：
		print(request.path)  # /article/detail/7/
		for path in auth_path:
			if re.match(path, request.path):
				# 需要验证用户的登录情况
				if not request.user.is_authenticated:
					return redirect(reverse('users:login'))

	def process_view(self, request, callback, callback_args, callback_kwargs):

		print('------------------>M2的process_view', callback)

	# def process_template_response(self, request, response):
	# 	print(response.template_name, response.context_data)
	# 	print('=============>M2的process_template_response')

	# 请求的路径中有错误
	def process_exception(self, request, exception):
		return render(request, 'failure.html', context={'reason': exception})

	# 响应
	def process_response(self, request, response):
		# print("++++++++>哈哈哈")
		# response = HttpResponse("哈哈哈哈")
		# return response
		response.set_cookie('a1', 'helloworld')
		print('process_response+++++++++++哈哈哈')
		return response
