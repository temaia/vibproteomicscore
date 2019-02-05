# -*- coding: utf-8 -*-

#from requests.models import Customer, Analysis
from django.contrib.auth import get_user_model
from requests.models import Analysis
from django.contrib import admin
from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import User, Profile#, Specimen_SG
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

User = get_user_model()

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'admin')
    list_filter = ('admin','staff','active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ()}),
        ('Permissions', {'fields': ('admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

#### Remove Group Model from admin. We're not using it.
####admin.site.unregister(Group)   


class UserAdmin(admin.ModelAdmin):
	search_fields = ['email']
	form = UserAdminChangeForm
	add_form = UserAdminCreationForm
	class Meta:
		model=User

#Register your models here.

#admin.site.register(Customer)

#admin.site.register(Sample)

class ProfileInline(admin.StackedInline):
    model=Profile
    can_delete=False
    verbose_name_plural='Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines=(ProfileInline,)
    list_display = ('email', 'admin')
    list_select_related = ('profile', )
    def get_location(self, instance):
        return instance.profile.get.location
    get_location.short_description = 'Location'

    def get_inline_instances(self,request,obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

#dmin.site.register(User, UserAdmin)
#admin.site.unregister(User)

admin.site.register(User,CustomUserAdmin)
#admin.site.register(Analysis)
#admin.site.register(Specimen_SG)