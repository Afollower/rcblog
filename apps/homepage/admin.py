from django.contrib import admin
from .models import RC_Article, RC_Comments, RC_Article_Tag, RC_Article_Type

# Register your models here.


admin.site.site_header = "博客管理"


class articleAdmin(admin.ModelAdmin):
    search_fields = ('id', 'title', 'type_id', 'tag_id')
    list_display = ('id', 'title', 'updated', 'type_id', 'tag_id')
    list_display_links = ('id', 'title', 'updated')


class commentAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'user_name', 'parents_id', 'replied_user', 'count')
    list_display_links = ('id', 'number', 'user_name', 'parents_id')


class typeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'count', 'updated')
    list_display_links = ('id', 'title', 'count', 'updated')


class tagAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'count', 'updated')
    list_display_links = ('id', 'title', 'count', 'updated')


admin.site.register(RC_Article_Type, typeAdmin)
admin.site.register(RC_Article_Tag, tagAdmin)
admin.site.register(RC_Article, articleAdmin)
admin.site.register(RC_Comments, commentAdmin)
