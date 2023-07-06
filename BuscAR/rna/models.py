from django.db import models
from django.conf import settings


class ARN(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE, related_name="user_rna")
    containerName = models.CharField(max_length=250)
    dataRnaUrl = models.CharField(max_length=250)
    configRnaUrl = models.CharField(max_length=250)

    def __str__(self):
        return self.user
