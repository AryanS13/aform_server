from rest_framework.permissions import IsAuthenticated, BasePermission

class IsAuthenticatedUser(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request=request, view=view)

class BasePermissions(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        data = request.data

        if not data.get('organization', None):
            return True # Remove this as soon as possible 

        if user.organization_id == data.get('organization', None):
            return True
        
        return False