from rest_framework import serializers

from .models import GymBranch
from accounts.models import User


class GymBranchSerializer(serializers.ModelSerializer):
    trainer_count = serializers.SerializerMethodField(read_only=True)
    member_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = GymBranch
        fields = [
            'id', 'name', 'location',
            'trainer_count', 'member_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'trainer_count', 'member_count']

    def get_trainer_count(self, obj):
        return User.objects.filter(branch=obj, role=User.ROLE_TRAINER).count()

    def get_member_count(self, obj):
        return User.objects.filter(branch=obj, role=User.ROLE_MEMBER).count()