from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class UserProfile(AbstractUser):
	nick_name = models.CharField(max_length=20, null=True, blank=True, verbose_name='用户昵称')
	phone = models.CharField(max_length=11, verbose_name='手机号码', unique=True, default='13800001111')

	def __str__(self):
		return self.username

	class Meta:
		db_table = 'userprofile'
		verbose_name = '用户信息表'
		verbose_name_plural = verbose_name
