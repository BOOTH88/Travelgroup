from django.db import models

# Create your models here.
class UserProfile(models.Model):
    username = models.CharField('用户名',max_length=11)
    nickname = models.CharField('昵称',max_length=30)
    email = models.CharField('邮箱', max_length=50, null=True)
    password = models.CharField('密码', max_length=32)

    class Meta:
        db_table = 'user_profile'