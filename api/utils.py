from rest_framework.response import Response
from rest_framework.views import exception_handler

def ErrorResponse(status,message,data=None):

    responseObj = {
        "success":False,
        "status":status,
        "message":message
    }

    if(data):
        responseObj['data'] = data
    
    return Response(responseObj)


def team_permission(request):
    if request.user.groups.filter(name='TeamGroup').exists() and not request.user.is_staff:
        return True
    return False
    