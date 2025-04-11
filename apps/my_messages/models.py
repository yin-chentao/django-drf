from django.db import models


class Message(models.Model):
    fromid = models.CharField(max_length=100, verbose_name="发送者ID")
    tolist = models.CharField(max_length=100, verbose_name="接收者ID")  # 注意：tolist 虽然叫列表，但实际只存一个值
    msgid = models.CharField(max_length=100, unique=True, verbose_name="消息ID")
    msgtime = models.DateTimeField(verbose_name="消息时间")
    content = models.TextField(verbose_name="消息内容")
    conversation_id = models.CharField(max_length=200, verbose_name="对话组ID",default=None)  # 新增字段，用于标识对话组

    class Meta:
        db_table = 'messages'
        ordering = ['msgtime']  # 默认按时间正序排列

    def save(self, *args, **kwargs):
        """自动生成 conversation_id：将 fromid 和 to 按字母顺序排序后拼接"""
        user1, user2 = sorted([self.fromid, self.tolist])
        self.conversation_id = f"{user1}_{user2}"
        super().save(*args, **kwargs)
