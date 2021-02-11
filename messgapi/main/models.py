from django.db import models


class Message(models.Model):
    text = models.CharField(max_length=160, blank=True, null=True)
    counter = models.IntegerField(default=0)


class APIKey(models.Model):
    key = models.UUIDField()
