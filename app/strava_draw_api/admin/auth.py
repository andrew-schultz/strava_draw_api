from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from strava_draw_api.models import Profile


class AdminCreationForm(UserCreationForm):
    email = forms.EmailField(help_text='Required')


class AdminChangeForm(UserChangeForm):
    email = forms.EmailField(help_text='Required')


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


class UserAdmin(BaseUserAdmin):
    form = AdminChangeForm
    add_form = AdminCreationForm
    list_display = (
        'email',
        'is_superuser',
        'is_staff',
        'is_active',
        'date_joined'
    )
    ordering = ['email']
    add_fieldsets = ((None, {
        'fields': ('username', 'email', 'password1', 'password2'),
        'classes': ('wide',)
    }),)
    inlines = (ProfileInline,)

    readonly_fields = ['is_superuser']

    def has_delete_permission(self, request, obj=None):
        # Dissallow. Admins should not delete admins
        return False

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = set(super().get_readonly_fields(request, obj))

        # Superusers can edit superuser status
        if request.user.is_superuser:
            readonly_fields.remove('is_superuser')

        return readonly_fields



class GroupAdmin(admin.ModelAdmin):
    filter_horizontal = ('permissions',)


__all__ = [
    'UserAdmin',
    'GroupAdmin',
]
