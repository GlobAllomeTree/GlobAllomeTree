
from django.contrib import admin

from globallometree.apps.base.models import TreeType

class TreeTypeAdmin(admin.ModelAdmin):
    list_display = ('Name', )

admin.site.register(TreeType, TreeTypeAdmin)
