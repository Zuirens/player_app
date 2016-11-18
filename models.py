from django.db import models
from django.contrib.auth.models import User
import uuid
from datetime import datetime
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class AuthenUser(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    extra_data = models.TextField(blank=True)
    is_blacklist = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('AUTHEN-USER')
        verbose_name_plural = verbose_name

class AnonyVisitor(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_visit = models.DateTimeField(auto_now=True)
    visit_count = models.PositiveIntegerField(default=0)
    identity = models.ForeignKey(AuthenUser, on_delete=models.CASCADE, blank=True)


class Message(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    author = models.ForeignKey(AuthenUser, on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    recieved_time = models.DateTimeField(auto_now_add=True)
    last_pub_time = models.DateTimeField(auto_now=True)
    pub_count = models.PositiveIntegerField(default=0)
    is_blacklist = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('MESSAGE')
        verbose_name_plural = verbose_name

class CensorWord(models.Model):
    word = models.CharField(max_length=255)
    count = models.PositiveIntegerField(default=0)

class StreamStatistic(models.Model):
    record_time = models.DateTimeField(default = datetime.now)
    realtime_viewer = models.PositiveIntegerField(default=0)
    total_viewer = models.PositiveIntegerField(default=0)

class ControlMeta(models.Model):
    source_name = models.CharField(max_length=31)
    stream_source = models.CharField(max_length=1023)
    thumbnail = models.CharField(max_length=1023)
    viewer_scaler = models.FloatField(default = 1.0)
    viewer_offset = models.FloatField(default = 0.0)
    start_time = models.DateTimeField(auto_now=True)
    is_start = models.BooleanField(default = False)


    class Meta:
        verbose_name = _('CONTROL-META')
        verbose_name_plural = verbose_name