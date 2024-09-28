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

