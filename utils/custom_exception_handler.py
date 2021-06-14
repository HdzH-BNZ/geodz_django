from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException

class ServiceNotFound(APIException):
    status_code = 400
    default_detail = 'Service non trouvé'
    default_code = 'service_not_found'

def base_exception_handler(exc, context):
    handlers = {
        'ValidationError': _handle_generic_error,
        'Http404': _handle_generic_error
    }
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data = {
            'error' : 'Not found',
            'error_descriptions' : 'Aucun élément trouvé',
            'status_code' : response.status_code
        }
        response.data['status_code'] = response.status_code

    exception_class = exc.__class__.__name__

    if exception_class in handlers:
        return handlers[exception_class](exc, context, response)

    return response

def _handle_generic_error(exc, context, response):
    return response