from django.db import models
from django.contrib.auth.models import AbstractBaseUser
import uuid
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

# Create your models here.
class FbAuthenUser(AbstractBaseUser):
    nick_name = models.CharField(max_length=31)
    username = models.CharField(unique=True, max_length=127)
    picture = models.CharField(max_length=1023, blank=True)
    extra_data = models.TextField(blank=True)
    gender = models.CharField(max_length=31, blank=True)
    link = models.CharField(max_length=255)
    locale = models.CharField(max_length=31, blank=True)
    zone = models.IntegerField(default=1, blank=True)
    updated_time = models.CharField(max_length=31, blank=True)
    verified = models.BooleanField(default=False, blank=True)
    is_blacklist = models.BooleanField(default=False)
    password = models.UUIDField(default=uuid.uuid4)
    USERNAME_FIELD = 'username'
    # user = models.OneToOneField(
    #     User,
    #     on_delete=models.CASCADE,
    #     primary_key=True,
    # )
    def pic_thumb(self):
        return '<img src="%s" height="50" />' % (self.picture)
    pic_thumb.allow_tags = True
    pic_thumb.short_description = 'Image'
    def __str__(self):
        return '{}'.format(self.username)

    class Meta:
        verbose_name = _('FACEBOOK USER')
        verbose_name_plural = verbose_name

# class AnonyVisitor(models.Model):
#     uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
#     date_joined = models.DateTimeField(default = timezone.now)
#     last_visit = models.DateTimeField(default = timezone.now)
#     visit_count = models.PositiveIntegerField(default=0)
#     identity = models.ForeignKey(FbAuthenUser, on_delete=models.CASCADE, blank=True)


class Comment(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    author = models.ForeignKey(FbAuthenUser, on_delete=models.CASCADE)
    body = models.CharField(max_length=255)
    recieved_time = models.DateTimeField(default = timezone.now)
    last_pub_time = models.DateTimeField(default = timezone.now)
    pub_count = models.PositiveIntegerField(default=0)
    is_blacklist = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('COMMENT')
        verbose_name_plural = verbose_name

class CensorWord(models.Model):
    word = models.CharField(max_length=255)
    count = models.PositiveIntegerField(default=0)

class StreamStatistic(models.Model):
    record_time = models.DateTimeField(default = timezone.now)
    realtime_viewer = models.PositiveIntegerField(default=0)
    total_viewer = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = _('STATISTIC')
        verbose_name_plural = verbose_name

class ControlMeta(models.Model):
    source_name = models.CharField(max_length=31)
    stream_source = models.CharField(max_length=1023)
    thumbnail = models.CharField(max_length=1023)
    viewer_scaler = models.FloatField(default = 1.0)
    viewer_offset = models.FloatField(default = 0.0)
    start_time = models.DateTimeField(auto_now=True)
    is_start = models.BooleanField(default = False)

    class Meta:
        verbose_name = _('CONTROL META')
        verbose_name_plural = verbose_name