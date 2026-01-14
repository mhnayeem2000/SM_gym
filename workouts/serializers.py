from rest_framework import serializers
from .models import WorkoutPlan, WorkoutTask
from accounts.serializers import UserSerializer


class WorkoutPlanSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.email', read_only=True)
    branch_name = serializers.CharField(source='branch.name', read_only=True)

    class Meta:
        model = WorkoutPlan
        fields = [
            'id', 'title', 'description',
            'created_by', 'created_by_name',
            'branch', 'branch_name',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_by_name', 'branch_name', 'created_at', 'updated_at']


class WorkoutTaskSerializer(serializers.ModelSerializer):
    workout_plan_title = serializers.CharField(source='workout_plan.title', read_only=True)
    member_email = serializers.CharField(source='member.email', read_only=True)
    branch_name = serializers.CharField(source='workout_plan.branch.name', read_only=True)

    class Meta:
        model = WorkoutTask
        fields = [
            'id', 'workout_plan', 'workout_plan_title',
            'member', 'member_email',
            'status', 'due_date', 'notes',
            'branch_name',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'workout_plan_title', 'member_email', 'branch_name',
            'created_at', 'updated_at'
        ]


class WorkoutTaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutTask
        fields = ['status']
        extra_kwargs = {
            'status': {'required': True}
        }