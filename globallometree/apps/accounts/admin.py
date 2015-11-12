from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe
from django.core import urlresolvers
from django.contrib.auth.models import User

from . import models

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'institution_name', 'location_country',  'data_may_provide')
    search_fields  = ['user__username', 'institution_name','address', 'location_country__Common_name', 'region']
    list_filter = ['institution_name', 'location_country__Common_name']
    readonly_fields = ['user_link']
    raw_id_fields = ('user',)
    exclude = ('country',)

    def user_link(self, obj):
        change_url = urlresolvers.reverse('admin:auth_user_change', args=(obj.user.id,))
        return mark_safe('<a href="%s">%s</a>' % (change_url, change_url))
    user_link.short_description = 'Django User Link'
    user_link.allow_tags = True


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'institution', 'institution_phone', 'subject' 'country', 'date_joined', 'profile' )

    def institution(self, obj):
        return obj.get_profile().institution_name

    def institution_phone(self, obj):
        return obj.get_profile().institution_phone

    def subject(self, obj):
        return obj.get_profile().field_subject

    def country(self, obj):
        if obj.get_profile().location_country:
            return obj.get_profile().location_country.Formal_name
        else:
            return obj.get_profile().country

    def profile(self, obj):
        return '<a href="/admin/accounts/userprofile/%s/">Profile&nbsp;&gt;</a>' % obj.get_profile().pk

    profile.allow_tags = True



admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)   
admin.site.register(models.UserProfile, UserProfileAdmin)


