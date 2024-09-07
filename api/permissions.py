from rest_framework.permissions import BasePermission,SAFE_METHODS

class IsAnonymous(BasePermission):
    def has_permission(self, request, view):
        # Allow anonymous users to POST requests
        if request.method == 'POST':
            return True
        # For other methods, check if the user is authenticated
        return request.user and request.user.is_authenticated
    



class HasTeamGroupPermission(BasePermission):
    """
    Custom permission to only allow users with 'teamGroup' to perform non-safe actions.
    Safe actions (like viewing) are allowed for everyone.
    """

    def has_permission(self, request, view):
        # Allow safe methods (GET, HEAD, OPTIONS) for any user
        if request.method in SAFE_METHODS:
            return True
        
        # Check if the user belongs to the 'teamGroup'
        return request.user.groups.filter(name='TeamGroup').exists()


class HasEventOrganizerGroupPermission(BasePermission):
    """
    Custom permission to only allow users with 'teamGroup' to perform non-safe actions.
    Safe actions (like viewing) are allowed for everyone.
    """

    def has_permission(self, request, view):
        # Allow safe methods (GET, HEAD, OPTIONS) for any user
        if request.method in SAFE_METHODS:
            return True
        
        # Check if the user belongs to the 'teamGroup'
        return request.user.groups.filter(name='EventOrganizer').exists()


