from django.contrib import admin
from .models import WorkoutPlan, WorkoutTask


@admin.register(WorkoutPlan)
class WorkoutPlanAdmin(admin.ModelAdmin):
    list_display = ('title', 'branch', 'created_by', 'created_at')
    list_filter = ('branch', 'created_by')
    search_fields = ('title', 'description', 'created_by__email')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(WorkoutTask)
class WorkoutTaskAdmin(admin.ModelAdmin):
    list_display = ('workout_plan', 'member', 'status', 'due_date', 'created_at')
    list_filter = ('status', 'workout_plan__branch', 'due_date')
    search_fields = ('workout_plan__title', 'member__email')
    readonly_fields = ('created_at', 'updated_at')