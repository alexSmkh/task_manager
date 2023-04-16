from django.contrib import admin

from main.models import Tag, Task
from django.contrib.auth.admin import UserAdmin

from .models import User


class TaskManagerAdminSite(admin.AdminSite):
    pass


task_manager_admin_site = TaskManagerAdminSite(name="Task manager admin")


@admin.register(Tag, site=task_manager_admin_site)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Task, site=task_manager_admin_site)
class TaskAdmin(admin.ModelAdmin):
    pass


task_manager_admin_site.register(User, UserAdmin)
