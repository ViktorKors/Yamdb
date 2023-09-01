from django.contrib import admin

from .models import User



class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'role', 'password')


admin.site.register(User, UserAdmin)