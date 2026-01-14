from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from SM_gym.permissions import (
    IsSuperAdmin, IsManager, IsTrainer, IsMember,
    IsTrainerOfBranch, IsMemberOwnerOfTask
)
from accounts.models import User
from .models import WorkoutPlan, WorkoutTask
from .serializers import (
    WorkoutPlanSerializer,
    WorkoutTaskSerializer,
    WorkoutTaskUpdateSerializer
)


class WorkoutPlanViewSet(viewsets.ModelViewSet):
    queryset = WorkoutPlan.objects.all()
    serializer_class = WorkoutPlanSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsTrainer()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user

        if user.role == User.ROLE_ADMIN:
            return WorkoutPlan.objects.all()

        if user.branch:
            return WorkoutPlan.objects.filter(branch=user.branch)

        return WorkoutPlan.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        if user.role != User.ROLE_TRAINER:
            raise PermissionDenied("Only trainers can create workout plans.")

        serializer.save(
            created_by=user,
            branch=user.branch
        )

    def perform_update(self, serializer):
        if self.request.user != self.get_object().created_by and not self.request.user.is_super_admin:
            raise PermissionDenied("You can only edit your own plans.")
        serializer.save()


class WorkoutTaskViewSet(viewsets.ModelViewSet):
    queryset = WorkoutTask.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update'] and self.request.user.role == User.ROLE_MEMBER:
            return WorkoutTaskUpdateSerializer
        return WorkoutTaskSerializer

    def get_queryset(self):
        user = self.request.user

        if user.role == User.ROLE_ADMIN:
            return WorkoutTask.objects.all().select_related('workout_plan', 'member', 'workout_plan__branch')

        if user.role == User.ROLE_MEMBER:
            return WorkoutTask.objects.filter(member=user).select_related('workout_plan', 'workout_plan__branch')

        if user.branch:
            return WorkoutTask.objects.filter(
                Q(workout_plan__branch=user.branch) | Q(member__branch=user.branch)
            ).select_related('workout_plan', 'member', 'workout_plan__branch')

        return WorkoutTask.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        if user.role != User.ROLE_TRAINER:
            raise PermissionDenied("Only trainers can assign tasks.")

        member = serializer.validated_data['member']
        plan = serializer.validated_data['workout_plan']

        if member.branch != user.branch or plan.branch != user.branch:
            raise ValidationError("Cannot assign task to member from another branch.")

        if user.branch.trainer_count() > 3:
            raise ValidationError("This branch already has the maximum of 3 trainers.")

        serializer.save()

    def perform_update(self, serializer):
        user = self.request.user
        instance = self.get_object()

        if user.role == User.ROLE_MEMBER:
            if instance.member != user:
                raise PermissionDenied("You can only update your own tasks.")
            serializer.save(status=serializer.validated_data.get('status'))

        elif user.role == User.ROLE_TRAINER:
            if instance.workout_plan.branch != user.branch:
                raise PermissionDenied("You can only update tasks in your branch.")
            serializer.save()

        else:
            serializer.save()

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated, IsManager | IsSuperAdmin])
    def branch_summary(self, request):
        branch = request.user.branch
        if not branch and not request.user.is_super_admin:
            return Response({"detail": "No branch assigned."}, status=403)

        if request.user.is_super_admin:
            pass

        total_plans = WorkoutPlan.objects.filter(branch=branch).count()
        total_tasks = WorkoutTask.objects.filter(workout_plan__branch=branch).count()
        completed = WorkoutTask.objects.filter(workout_plan__branch=branch, status=WorkoutTask.STATUS_COMPLETED).count()

        return Response({
            "branch": branch.name,
            "total_workout_plans": total_plans,
            "total_tasks": total_tasks,
            "completed_tasks": completed,
        })