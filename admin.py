from django.contrib import admin
from .models import *
# Register your models here.



class MessageAdmin(admin.ModelAdmin):
    pass




admin.site.register(AuthenUser)
admin.site.register(AnonyVisitor)
admin.site.register(Message)
admin.site.register(CensorWord)