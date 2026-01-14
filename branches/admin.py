from django.contrib import admin

from .models import GymBranch


@admin.register(GymBranch)
class GymBranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'created_at', 'trainer_count_display')
    search_fields = ('name', 'location')
    readonly_fields = ('created_at', 'updated_at')
    list_filter = ('created_at',)

    def trainer_count_display(self, obj):
        return obj.trainer_count()
    trainer_count_display.short_description = "Trainers"