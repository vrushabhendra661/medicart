"""
Utility functions for the pharmacy application.
"""
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
import logging

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Custom exception handler for REST Framework.
    Provides consistent error responses with logging.
    """
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)
    
    # Log the exception
    view = context.get('view', None)
    request = context.get('request', None)
    
    if view:
        view_name = view.__class__.__name__
    else:
        view_name = 'Unknown'
    
    if request:
        method = request.method
        path = request.path
    else:
        method = 'Unknown'
        path = 'Unknown'
    
    logger.error(
        f"Exception in {view_name} ({method} {path}): {str(exc)}",
        exc_info=True
    )
    
    # Handle Django ValidationError
    if isinstance(exc, ValidationError):
        if hasattr(exc, 'message_dict'):
            error_data = exc.message_dict
        elif hasattr(exc, 'messages'):
            error_data = {'detail': exc.messages}
        else:
            error_data = {'detail': str(exc)}
        
        return Response(
            error_data,
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # If response is None, it's an unhandled exception
    if response is None:
        return Response(
            {
                'detail': 'An unexpected error occurred.',
                'error': str(exc)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    # Customize the response data
    if hasattr(response, 'data'):
        custom_response_data = {
            'status': 'error',
            'message': response.data if isinstance(response.data, str) else response.data.get('detail', 'An error occurred'),
            'errors': response.data if isinstance(response.data, dict) else {}
        }
        response.data = custom_response_data
    
    return response

