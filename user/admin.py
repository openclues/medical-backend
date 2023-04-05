from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import UserAccount, TeamMember, Specialty, MedicalCenter, Address, Plan, Subscription, Interest, \
    Transaction, Doctor, CustomField


class TeamMemberInline(admin.TabularInline):
    model = TeamMember


class SpecialtyInline(admin.TabularInline):
    model = MedicalCenter.specialities.through


class AddressInline(admin.TabularInline):
    model = Address


class DoctorsInLine(admin.TabularInline):
    model = Doctor


class CustomFieldsInline(admin.TabularInline):
    model = CustomField


class MedicalCenterAdmin(admin.ModelAdmin):
    inlines = [TeamMemberInline, SpecialtyInline, DoctorsInLine, CustomFieldsInline]
    fieldsets = (
        (None, {
            'fields': ('admin', 'title', 'overview', 'phone', 'email', 'url', 'is_promoted', 'logo', 'cover')
        }),
        ('Address', {
            'fields': ('addresses',),
        }),
    )


admin.site.register(UserAccount, UserAdmin)
admin.site.register(TeamMember)
admin.site.register(Specialty)
admin.site.register(Plan)
admin.site.register(Transaction)
admin.site.register(Subscription)
admin.site.register(Interest)
admin.site.register(Address)
admin.site.register(MedicalCenter, MedicalCenterAdmin)
