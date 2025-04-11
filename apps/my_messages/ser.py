from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
        extra_kwargs = {
            'msgid': {'validators': []}  # 禁用唯一性验证（假设导入时处理）
        }
