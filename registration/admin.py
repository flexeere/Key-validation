from django.contrib import admin
from .models import Company, ValidationKey

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_name', 'email', 'gst_number', 'is_verified', 'created_at')
    list_filter = ('is_verified', 'created_at')
    search_fields = ('name', 'email', 'gst_number')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

@admin.register(ValidationKey)
class ValidationKeyAdmin(admin.ModelAdmin):
    list_display = ('company', 'is_used', 'expires_at', 'created_at')
    list_filter = ('is_used', 'expires_at')
    search_fields = ('company__name',)
    readonly_fields = ('token',) # Make token strictly read-only for security

    def get_readonly_fields(self, request, obj=None):
        if obj: # Editing an existing object
            return self.readonly_fields + ('company',)
        return self.readonly_fields
