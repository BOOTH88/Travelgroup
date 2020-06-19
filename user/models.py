from django.db import models


# Create your models here.
class UserProfile(models.Model):
    username = models.CharField('用户名', max_length=11, primary_key=True)
    nickname = models.CharField('昵称', max_length=30)
    email = models.CharField('邮箱', max_length=50, null=True)
    password = models.CharField('密码', max_length=32)
    sign = models.CharField('个性签名', max_length=50)
    info = models.CharField('个人描述', max_length=150)
    avatar = models.ImageField('头像', upload_to='avatar/')

    class Meta:
        db_table = 'user_profile'
        verbose_name = '用户信息表'
        verbose_name_plural = verbose_name
