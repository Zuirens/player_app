from django.contrib import admin
from .models import Message, ControlMeta, AuthenUser, StreamStatistic
# Register your models here.


class AuthenUserAdmin(admin.ModelAdmin):
    list_display = ('uid', 'is_blacklist')

class MessageAdmin(admin.ModelAdmin):
    list_display = ('uid', 'content', 'recieved_time', 'pub_count', 'is_blacklist')


class ControlMetaAdmin(admin.ModelAdmin):
    list_display = ('source_name', 'viewer_scaler', 'viewer_offset', 'start_time', 'is_start')


admin.site.register(Message, MessageAdmin)
admin.site.register(ControlMeta, ControlMetaAdmin)
admin.site.register(AuthenUser, AuthenUserAdmin)
