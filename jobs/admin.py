from django.contrib import admin
from django.utils.html import format_html

from .models import JobCategory, Job, JobApplication


class JobCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description_short')
    search_fields = ('name', 'description')

    def description_short(self, obj):
        return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description

    description_short.short_description = 'Description'


class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'location', 'job_type', 'category', 'posted_by', 'posted_at', 'is_active')
    list_filter = ('job_type', 'category', 'posted_at', 'is_active')
    search_fields = ('title', 'company', 'location', 'description')
    list_editable = ('is_active',)
    raw_id_fields = ('posted_by', 'category')
    date_hierarchy = 'posted_at'

    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'company', 'location')
        }),
        ('Job Details', {
            'fields': ('job_type', 'category', 'salary', 'posted_by', 'is_active')
        }),
    )


class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'applicant', 'status', 'applied_at', 'resume_link')
    list_filter = ('status', 'applied_at')
    search_fields = ('job__title', 'applicant__email', 'cover_letter')
    raw_id_fields = ('job', 'applicant')
    date_hierarchy = 'applied_at'

    def resume_link(self, obj):
        if obj.resume:
            return format_html('<a href="{}" target="_blank">View Resume</a>', obj.resume.url)
        return "-"

    resume_link.short_description = 'Resume'


admin.site.register(JobCategory, JobCategoryAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(JobApplication, JobApplicationAdmin)