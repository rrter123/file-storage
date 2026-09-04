from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from account.models import Employee


class EmployeeAdmin(admin.ModelAdmin):
    pass


class EmployeeInline(admin.StackedInline):
    model = Employee
    can_delete = False
    extra = 1
    min_num = 1
    validate_min = True


class UserAdmin(BaseUserAdmin):
    inlines = [EmployeeInline]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
