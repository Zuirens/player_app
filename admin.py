from django.contrib import admin
from .models import Comment, ControlMeta, FbAuthenUser, StreamStatistic
# Register your models here.


class FbAuthenUserAdmin(admin.ModelAdmin):
    list_display = ('nick_name', 'username', 'pic_thumb', 'is_blacklist')

class MessageAdmin(admin.ModelAdmin):
    list_display = ('uid', 'body', 'recieved_time', 'pub_count', 'is_blacklist')


class ControlMetaAdmin(admin.ModelAdmin):
    list_display = ('source_name', 'viewer_scaler', 'viewer_offset', 'start_time', 'is_start')


class StreamStatisticAdmin(admin.ModelAdmin):
    list_display = ('realtime_viewer', 'total_viewer', 'record_time')

admin.site.register(Comment, MessageAdmin)
admin.site.register(ControlMeta, ControlMetaAdmin)
admin.site.register(FbAuthenUser, FbAuthenUserAdmin)
admin.site.register(StreamStatistic, StreamStatisticAdmin)