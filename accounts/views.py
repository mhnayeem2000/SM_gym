from rest_framework import status, viewsets
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
    #Usr Profile Informations
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
            return [IsAuthenticated(), IsManager() | IsSuperAdmin()]
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

    def perform_create(self, serializer):
        user = self.request.user

        if user.is_manager:
            if 'branch' in serializer.validated_data:
                if serializer.validated_data['branch'] != user.branch:
                    raise serializer.ValidationError(
                        {"branch": "Managers can only create users in their own branch"}
                    )
            else:
                serializer.save(branch=user.branch)
        else:
            serializer.save()

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)