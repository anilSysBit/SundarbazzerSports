from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError
from .response import ErrorResponse

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        # Validation Errors
        if isinstance(exc, ValidationError):
            return ErrorResponse("Validation failed.", errors=response.data, status=response.status_code)

        # For other types of errors
        return ErrorResponse(str(exc), errors=response.data, status=response.status_code)

    return response