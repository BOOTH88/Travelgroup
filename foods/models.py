from django.db import models

# Create your models here.
from user.models import UserProfile


class Food (models.Model):
    username = models.ForeignKey(UserProfile)
    title = models.CharField('文章标题',max_length=50)
    info = models.CharField('文章简介',max_length=90)
    content = models.TextField('文章内容')
    location = models.CharField('所属地理位置',max_length=80)
    image = models.ImageField('美食图片',upload_to='img/')

    class Meta:
        db_table = 'food'
        verbose_name = '美食表'
        verbose_name_plural = verbose_name