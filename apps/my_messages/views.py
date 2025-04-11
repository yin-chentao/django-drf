import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from .models import Message
from .ser import MessageSerializer
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework import status
from django.conf import settings
import pandas as pd
from io import BytesIO
from django.utils import timezone


class ExcelUploadAPI(APIView):
    parser_classes = (MultiPartParser, FileUploadParser)

    def post(self, request, *args, **kwargs):
        # 1. 安全验证：检查文件是否存在
        if 'file' not in request.data:
            return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        excel_file = request.data['file']

        # 2. 验证文件类型
        if not excel_file.name.endswith(('.xlsx', '.xls')):
            return Response({"error": "Invalid file type. Only Excel files are allowed"},
                            status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

        # 3. 验证文件大小（限制为10MB）
        max_size = getattr(settings, 'MAX_EXCEL_UPLOAD_SIZE', 10 * 1024 * 1024)
        if excel_file.size > max_size:
            return Response({"error": f"File too large. Max size is {max_size / 1024 / 1024}MB"},
                            status=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)

        try:
            # 4. 使用 pandas 读取 Excel，并手动指定引擎
            if excel_file.name.endswith('.xlsx'):
                df = pd.read_excel(BytesIO(excel_file.read()), engine='openpyxl')
            else:
                df = pd.read_excel(BytesIO(excel_file.read()), engine='xlrd')

            # 5. 验证必要字段
            required_columns = {'fromid', 'tolist', 'msgid', 'msgtime', 'content'}
            if not required_columns.issubset(df.columns):
                missing = required_columns - set(df.columns)
                return Response({"error": f"Missing columns: {', '.join(missing)}"},
                                status=status.HTTP_422_UNPROCESSABLE_ENTITY)

            # 6. 数据导入处理
            success_count = 0
            errors = []
            for _, row in df.iterrows():
                try:
                    # 处理时间戳
                    msgtime_timestamp = row['msgtime']
                    msgtime = datetime.datetime.fromtimestamp(msgtime_timestamp)
                    msgtime = timezone.make_aware(msgtime)

                    # 确保 msgid 是整数类型
                    try:
                        msgid = int(row['msgid'])
                    except ValueError:
                        errors.append({"row": _ + 2, "error": f"Invalid msgid value: {row['msgid']}",
                                       "msgid": row.get('msgid', 'N/A')})
                        continue

                    # 处理 tolist 数据
                    tolist_str = row['tolist']
                    # 去除方括号和引号
                    tolist = tolist_str.strip("[]'")

                    # 创建记录（自动生成 conversation_id）
                    Message.objects.create(fromid=row['fromid'], tolist=tolist, msgid=msgid, msgtime=msgtime,
                                           content=row['content'])
                    success_count += 1
                except Exception as e:
                    errors.append({"row": _ + 2,  # Excel 行号从2开始
                                   "error": str(e), "msgid": row.get('msgid', 'N/A')})

            # 7. 返回结果
            result = {"total_rows": len(df), "success_count": success_count, "error_count": len(errors),
                      "errors": errors}
            return Response(result, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": f"File processing failed: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ConversationAPI(APIView):
    def get(self, request):
        fromid = request.query_params.get('fromid')

        if fromid:
            # 查询与 fromid 相关的所有对话组
            messages = Message.objects.filter(Q(fromid=fromid) | Q(tolist=fromid)).order_by('msgtime')
            conversations = {}
            for msg in messages:
                conv_id = msg.conversation_id
                if conv_id not in conversations:
                    conversations[conv_id] = {"conversation_id": conv_id,
                                              "participants": sorted([msg.fromid, msg.tolist]), "messages": []}
                conversations[conv_id]["messages"].append(MessageSerializer(msg).data)
            return Response({"conversations": list(conversations.values())})

        else:
            # 返回所有对话组，按时间正序排列:
            all_messages = Message.objects.all().order_by('msgtime')
            conversations = {}
            for msg in all_messages:
                conv_id = msg.conversation_id
                if conv_id not in conversations:
                    conversations[conv_id] = {"conversation_id": conv_id,
                                              "participants": sorted([msg.fromid, msg.tolist]), "messages": []}
                conversations[conv_id]["messages"].append(MessageSerializer(msg).data)
            return Response({"conversations": list(conversations.values())})
