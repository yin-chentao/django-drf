from django.db import models


# Create your models here.

class BookInfo(models.Model):
    lend_status = ((0, '未借出'), (1, '已借出'),)
    name = models.CharField(max_length=40, verbose_name='书名', unique=True)
    author = models.CharField(max_length=30, verbose_name='作者')
    lend = models.IntegerField(choices=lend_status, verbose_name='是否借出')
    description = models.TextField(max_length=200, verbose_name="描述", default=None, blank=True)

    class Meta:
        db_table = "BookInfo"
        verbose_name = "书籍"
        verbose_name_plural = verbose_name
