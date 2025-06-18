from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, OTP, Profile
from .forms import ProfileForm
from django.utils.html import format_html


class ProfileInline(admin.StackedInline):
    model = Profile
    form = ProfileForm
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'
    extra = 0

    fieldsets = (
        (None, {
            'fields': (
            'profile_picture_preview', 'first_name', 'last_name', 'phone_number', 'address', 'bio', 'profile_picture')
        }),
    )
    readonly_fields = ('profile_picture_preview',)

    def profile_picture_preview(self, obj):
        if obj.profile_picture:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 100px; border-radius: 50%;" />',
                               obj.profile_picture.url)
        return "No image"

    profile_picture_preview.short_description = 'Profile Picture Preview'


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    list_display = ('email', 'is_verified', 'is_staff', 'date_joined')
    list_filter = ('is_verified', 'is_staff', 'is_superuser', 'date_joined')
    search_fields = ('email', 'profile__first_name', 'profile__last_name')
    ordering = ('-date_joined',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {
            'fields': ('is_active', 'is_verified', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_superuser'),
        }),
    )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super().get_inline_instances(request, obj)


class OTPAdmin(admin.ModelAdmin):
    list_display = ('user', 'otp', 'created_at', 'is_valid')
    list_filter = ('created_at',)
    search_fields = ('user__email', 'otp')
    readonly_fields = ('created_at', 'is_valid')

    def is_valid(self, obj):
        return obj.is_valid()

    is_valid.boolean = True


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'full_name', 'phone_number', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__email', 'first_name', 'last_name', 'phone_number')
    readonly_fields = ('created_at', 'updated_at', 'profile_picture_preview')
    fieldsets = (
        (None, {
            'fields': ('user', 'profile_picture_preview', 'profile_picture')
        }),
        ('Personal Info', {
            'fields': ('first_name', 'last_name', 'phone_number', 'address', 'bio')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def user_email(self, obj):
        return obj.user.email

    user_email.short_description = 'Email'
    user_email.admin_order_field = 'user__email'

    def full_name(self, obj):
        return obj.full_name

    full_name.short_description = 'Full Name'

    def profile_picture_preview(self, obj):
        if obj.profile_picture:
            return format_html('<img src="{}" style="max-height: 200px; max-width: 200px; border-radius: 5px;" />',
                               obj.profile_picture.url)
        return "No image"

    profile_picture_preview.short_description = 'Profile Picture Preview'


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(OTP, OTPAdmin)
admin.site.register(Profile, ProfileAdmin)