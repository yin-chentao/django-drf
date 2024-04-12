from django.db import models


# Create your models here.

class BookInfo(models.Model):
    lend_status = ((0, '未借出'), (1, '已借出'),)
    name = models.CharField(max_length=40, unique=True, verbose_name='书名')
    author = models.CharField(max_length=30, verbose_name='作者')
    lend = models.IntegerField(choices=lend_status, verbose_name='是否借出')
    description = models.TextField(max_length=200, default=None, blank=True, verbose_name="描述")
    createby = models.CharField(max_length=30, default='system', verbose_name='创建人')
    editby = models.CharField(max_length=30, default=None, verbose_name='修改人', blank=True, null=True)

    class Meta:
        db_table = "BookInfo"
        verbose_name = "书籍"
        verbose_name_plural = verbose_name


class BookFile(models.Model):
    name = models.CharField(max_length=20, verbose_name='文件名')
    file = models.FileField()
    createby = models.CharField(max_length=30, default='system', verbose_name='创建人')
    editby = models.CharField(max_length=30, default=None, verbose_name='修改人', blank=True, null=True)

    class Meta:
        db_table = 'file'
        verbose_name = '文件'
        verbose_name_plural = verbose_name

