from django.contrib import admin
from django.contrib.sessions.models import Session


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):

    """SessionAdmin"""

    list_display = (
        'session_key',
        '_session_data',
        'expire_date')

    readonly_fields = (
        'session_key',
        '_session_data',
        'expire_date')

    def _session_data(self, obj):
        return obj.get_decoded()
