from django.db import models
from django.contrib.auth.models import User
import uuid
from datetime import datetime
# Create your models here.
class AuthenUser(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    uid = models.CharField(max_length=255)
    extra_data = models.TextField(blank=True)
    is_blacklist = models.BooleanField(default=False)

class AnonyVisitor(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_visit = models.DateTimeField(auto_now=True)
    visit_count = models.PositiveIntegerField(default=0)
    identity = models.ForeignKey(AuthenUser, on_delete=models.CASCADE, blank=True)


class Message(models.Model):
    author = models.ForeignKey(AuthenUser, on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    recieved_time = models.DateTimeField(auto_now_add=True)
    last_pub_time = models.DateTimeField(auto_now=True)
    pub_count = models.PositiveIntegerField(default=0)
    is_blacklist = models.BooleanField(default=False)

class CensorWord(models.Model):
    word = models.CharField(max_length=255)
    count = models.PositiveIntegerField(default=0)

class StreamStatistic(models.Model):
    record_time = models.DateTimeField(default = datetime.now)
    realtime_viewer = models.PositiveIntegerField(default=0)
    total_viewer = models.PositiveIntegerField(default=0)