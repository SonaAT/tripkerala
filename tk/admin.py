from django.contrib import admin
from .models import Journal, JournalImage

@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    list_display = ('user', 'journal_text', 'created_at')

@admin.register(JournalImage)
class JournalImageAdmin(admin.ModelAdmin):
    list_display = ('journal', 'image')
