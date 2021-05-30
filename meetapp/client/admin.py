from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Member
from .api.models import Match


class CustomUserAdmin(UserAdmin):
    model = Member
    list_display = ['id', 'email', 'username', ]


admin.site.register(Member, CustomUserAdmin)
admin.site.register(Match)
