from rest_framework.response import Response

def SuccessResponse(message, data=None, status=200):
    response_data = {
        'success': True,
        'message': message,
        'data': data if data else {},
        'status': status
    }
    return Response(response_data, status=status)




def ErrorResponse(message, errors=None, status=400):
    response_data = {
        'success': False,
        'message': message or "Some Error Occured",
        'errors': errors if errors else {},
        'status': status
    }
    return Response(response_data, status=status)