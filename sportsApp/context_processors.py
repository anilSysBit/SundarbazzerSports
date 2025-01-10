def permissions_processor(request):
    # Initialize default permissions
    permissions = {
        "is_organizer": False,
        "is_staff": False,
    }

    

    # Update permissions based on the authenticated user
    if request.user.is_authenticated:

        if request.user.is_staff:
            permissions['is_organizer'] = True
        elif request.user.groups.filter(name='TeamGroup').exists():
             permissions["is_team"] = True
        
    return {"permissions": permissions}
