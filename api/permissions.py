from rest_framework.permissions import BasePermission


class IsAnonymous(BasePermission):
    def has_permission(self, request, view):
        # Allow anonymous users to POST requests
        if request.method == 'POST':
            return True
        # For other methods, check if the user is authenticated
        return request.user and request.user.is_authenticated