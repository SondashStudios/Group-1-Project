from django.db import models
from django.conf import settings


class ChecklistProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    module_item_id = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user.username} - {self.module_item_id}"