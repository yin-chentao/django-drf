from django.db import models


# Create your models here.
class Student(models.Model):
    """学生信息"""
    sexes = ((1, '男生'), (2, '女生'),)

    name = models.CharField(max_length=255, verbose_name="姓名")
    sex = models.IntegerField(verbose_name="性别", choices=sexes)
    age = models.IntegerField(verbose_name="年龄")
    classmate = models.CharField(max_length=5, verbose_name="班级编号")
    description = models.TextField(max_length=1000, verbose_name="个性签名")

    class Meta:
        db_table = "student"
        verbose_name = "学生"
        verbose_name_plural = verbose_name
    #
    # def __str__(self):
    #     return self.name
