'''from django.contrib import admin
from django.db import models
from userpanel.models import Menu, Projects

class CustomAdminProjects(admin.ModelAdmin):
    model = Projects
    list_display = ['id', 'user_id', 'project_name', 'date_started',]
    search_fields = ('user_id',)
    readonly_fields = ('date_started',)
    formfield_overrides = {
        models.DateField: {'input_formats': ('%m/%d/%Y',)},
    }

admin.site.register(Projects, CustomAdminProjects)


class MenuInLineAdmin(admin.TabularInline):
    model = Menu


admin.site.register(Menu)'''


from simple_history.admin import SimpleHistoryAdmin
from django.contrib import admin
from .models import AddOns, ImageUploader, Projects, Menu, Choicesprod, SecurityProducts, SitePages, StoragePlans, SupportPlans, UserSecurity, UserStorage, UserSupport
from django.db import models


class MenuInLineAdmin(admin.TabularInline):
    model = Menu


# class SitePagesInLineAdmin(admin.TabularInline):
#     model = SitePages


class ProjectsAdmin(SimpleHistoryAdmin, admin.ModelAdmin):
    inlines = [MenuInLineAdmin, ]
    model = Projects
    list_display = ['id', 'user_id', 'project_name', 'date_started', ]
    search_fields = ('user_email',)
    readonly_fields = ('date_started',)
    formfield_overrides = {
        models.DateField: {'input_formats': ('%m/%d/%Y',)}}
    history_list_display = ["status"]


admin.site.register(Projects, ProjectsAdmin)

admin.site.register(Menu)
# admin.site.register(SitePages)
admin.site.register(StoragePlans)
admin.site.register(SupportPlans)
admin.site.register(Choicesprod)
admin.site.register(AddOns)
admin.site.register(UserSupport)
admin.site.register(UserStorage)
admin.site.register(SecurityProducts)
admin.site.register(UserSecurity)
@admin.register(ImageUploader)
class AdminImageUploader(admin.ModelAdmin):
        list_display = ['id','image_name','image','user','user_profile','date']

