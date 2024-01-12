from django.contrib import admin
from django.db import models
from .models import Profile

from users.models import CustomUser
from django.contrib.auth.admin import UserAdmin
from users.forms import UserCreationForm, UserUpdateForm
from users.models import GuestIP, UserAgent

admin.site.register(Profile)


class CustomAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserUpdateForm
    model = CustomUser
    list_display = ['email', 'ip_address', 'is_staff', ]
    fieldsets = UserAdmin.fieldsets + (  # New
        (None, {'fields': ('ip_address', 'phone_numbers',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('email',)
    readonly_fields = ('ip_address', 'date_joined',)
    formfield_overrides = {
        models.DateField: {'input_formats': ('%m/%d/%Y',)},
    }


class GuestIPAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'user_ip_address', 'time')
    list_filter = ('time', 'user_id',)
    readonly_fields = ('user_id', 'time', 'user_ip_address',)


admin.site.register(GuestIP, GuestIPAdmin)

admin.site.register(CustomUser, CustomAdmin)


class UserAgentAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'user_ip_address', 'time',
                    'browser',
                    'os',
                    'device',
                    'device_brand',
                    'device_model',
                    )
    list_filter = ('time', 'user_id', 'browser', 'os')
    readonly_fields = ('user_id', 'time', 'user_ip_address', 'browser',
                       'broswer_id', 'os', 'os_id', 'device', 'device_brand', 'device_model')


admin.site.register(UserAgent, UserAgentAdmin)
