from django.utils import timezone
from rest_framework import permissions


# Permissions for MedicalCenter model
from rest_framework.permissions import BasePermission

from user.models import Subscription


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admin users to edit the medical center object.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff and request.user.is_authenticated


class IsAdminOrModerator(permissions.BasePermission):
    """
    Custom permission to only allow admin and moderator users of the medical center to edit the medical center object.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff or obj.team_members.filter(user=request.user, is_moderator=True).exists()


class IsAdminOrOwner(permissions.BasePermission):
    """
    Custom permission to only allow admin and owner of the medical center to edit the medical center object.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff or obj.admin == request.user


# Permissions for TeamMember model

class IsAdminOrTeamMember(permissions.BasePermission):
    """
    Custom permission to only allow admin and team members of the medical center to edit the team member object.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff or obj.user == request.user or obj.medical_center.team_members.filter(
            user=request.user, is_moderator=True).exists()


# Permissions for Favorites model

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owner of the favorite object to edit the favorite object.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class HasSubscription(BasePermission):
    message = "You must have an active subscription to access this resource."

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            # Check if the user has an active subscription
            now = timezone.now()
            active_subscription = Subscription.objects.filter(
                user=request.user,
                is_active=True,
                start_date__lte=now,
                end_date__gt=now,
            ).first()
            return active_subscription is not None
        return False
