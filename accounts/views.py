from rest_framework import status, viewsets, serializers 
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from SM_gym.permissions import IsSuperAdmin, IsManager   

from .models import User
from .serializers import (
    UserSerializer,
    UserCreateSerializer,
    UserProfileSerializer
)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'list']:
            return [IsAuthenticated(), (IsSuperAdmin | IsManager)()]
        return super().get_permissions()

    def get_queryset(self):
        user = self.request.user
        if user.is_super_admin:
            return User.objects.all()
        if user.is_manager and user.branch:
            return User.objects.filter(branch=user.branch)
        return User.objects.none()

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        requesting_user = self.request.user

        if requesting_user.is_super_admin:
            serializer.save()
            return
        if not requesting_user.is_manager:
            raise serializers.ValidationError("You do not have permission to create users.")

        manager_branch = requesting_user.branch

        if manager_branch is None:
            raise serializers.ValidationError("Manager has no branch assigned.")

        if 'branch' in serializer.validated_data:
            if serializer.validated_data['branch'] != manager_branch:
                raise serializers.ValidationError(
                    {"branch": "Managers can only create users in their own branch."}
                )
        serializer.save(branch=manager_branch)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)