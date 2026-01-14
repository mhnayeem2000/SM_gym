from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from SM_gym.permissions import IsSuperAdmin
from .models import GymBranch
from .serializers import GymBranchSerializer


class GymBranchViewSet(viewsets.ModelViewSet):
    queryset = GymBranch.objects.all()
    serializer_class = GymBranchSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        if instance.users.exists():
            return Response(
                {"detail": "Cannot delete branch that still has users assigned."},
                status=status.HTTP_400_BAD_REQUEST
            )
        instance.delete()