from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied


class IsSuperAdmin(permissions.BasePermission):
    message = "Super Admin access required."

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'


class IsManager(permissions.BasePermission):
    message = "Gym Manager access required."

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'manager'


class IsTrainer(permissions.BasePermission):
    message = "Trainer access required."

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'trainer'


class IsMember(permissions.BasePermission):
    message = "Member access required."

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'member'


def same_branch(user, obj):
    if user.role == 'admin':
        return True
    if not user.branch or not hasattr(obj, 'branch'):
        return False
    return user.branch == obj.branch


class IsInSameBranchAsObject(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return same_branch(request.user, obj)


class IsTrainerOfBranch(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'trainer'

    def has_object_permission(self, request, view, obj):
        return same_branch(request.user, obj)


class IsMemberOwnerOfTask(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role != 'member':
            return False
        return obj.member == request.user