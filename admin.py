from django.contrib import admin
from .models import Comment, ControlMeta, FbAuthenUser, StreamStatistic
# Register your models here.



class FbAuthenUserAdmin(admin.ModelAdmin):
    list_display = ('edit_link', 'nick_name', 'username', 'pic_thumb', 'is_blacklist')
    list_editable = ('is_blacklist',)

    list_display_links = None

    def edit_link(self,obj):
        return u'<button>%s</button>' % (obj.nick_name)
    edit_link.allow_tags = True
    edit_link.short_description = "EDIT"

    # def get_list_display_links(self, request, list_display):
    #     print('--------------', repr(reduce))
    #     return list_display

class MessageAdmin(admin.ModelAdmin):
    list_display = ('uid', 'get_author', 'body', 'recieved_time', 'pub_count', 'is_blacklist')
    list_editable = ('is_blacklist',)
    search_fields = ('author__nick_name',)
    # list_filter = ('author__nick_name', 'body',)

    def get_author(self, obj):
        return obj.author.nick_name
    get_author.short_description = 'Author'
    # get_author.admin_order_field = 'author__nick_name'


class ControlMetaAdmin(admin.ModelAdmin):
    list_display = ('name', 'viewer_scaler', 'viewer_offset', 'start_time', 'is_start')
    list_editable = ('viewer_scaler', 'viewer_offset', 'is_start')
    # list_filter = ('name', 'is_start')


class StreamStatisticAdmin(admin.ModelAdmin):
    list_display = ('realtime_viewer', 'total_viewer', 'record_time')

admin.site.register(Comment, MessageAdmin)
admin.site.register(ControlMeta, ControlMetaAdmin)
admin.site.register(FbAuthenUser, FbAuthenUserAdmin)
admin.site.register(StreamStatistic, StreamStatisticAdmin)