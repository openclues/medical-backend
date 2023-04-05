from rest_framework import permissions


# Permissions for MedicalCenter model

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
