from django.db import models

class Task(models.Model):
    task = models.CharField(max_length=100)
    # 登録日時
    created_at = models.DateTimeField(auto_now_add=True)
    # 更新日時
    updated_at = models.DateTimeField(auto_now=True)

