from django.contrib import admin

from main.models import Tag, Task, User


class TaskManagerAdminSite(admin.AdminSite):
    pass


task_manager_admin_site = TaskManagerAdminSite(name="Task manager admin")


@admin.register(Tag, site=task_manager_admin_site)
class TagAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(Task, site=task_manager_admin_site)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'state',
        'author',
        'assigned',
        'created_at',
        'updated_at',
        'deadline',
        'priority',
    )


@admin.register(User, site=task_manager_admin_site)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'role']
