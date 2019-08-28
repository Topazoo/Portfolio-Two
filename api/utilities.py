
from django.http import JsonResponse, HttpRequest
from django.conf import settings
from django.apps import apps
from .errors import API_Error
from .models import API_Model
import logging, json

def api_response(content: dict = {}, code: int = 400) -> JsonResponse:
    ''' Format an API JSON response.

        --> content : A dictionary of JSON serializable objects to return. Optional.
        
        --> code : The HTTP status code to return. Optional.
        
        <-- The JSON formatted response. { <<content>>, "code": <<code>> }
    '''

    content['code'] = code
    return JsonResponse(content, status=code)

def log_error(message : str):
    ''' Logs an API error to /logs/api.log if DEBUG is True in settings.

        --> message : The message to log.
    '''

    if settings.DEBUG:
        logger = logging.getLogger('api')
        logger.error(message)

def handle_unsupported_method(request : HttpRequest):
    ''' Fallback to find query parameters for unsuported methods and encodings.
        Decodes the body of the request object and adds it to the request's POST
        field.

        --> request : The request sent to the API.
     '''

    if len(request.body) > 2:
        request.POST = dict(request.POST)
        request.POST.update(json.loads(request.body.decode('utf-8').replace('\'', '\"')))

def validate_fields(fields: [dict, list], model: API_Model):
    ''' Ensure that the model fields passed to an API call exist for that model.
    
        --> fields : The fields passed to the request.
        
        --> model : A model derived from the base class defined in api/models.py.
    '''
    
    model_fields = [field.name for field in model._meta.fields]

    for field in fields:
        if field not in model_fields:
            raise API_Error('Field \'{}\' not found for model: \'{}\''.format(field, model.__name__), 400)


def parse_query_pairs(payload: str) -> dict:
    ''' Parse out one or more key/value pairs from a query string
        (e.g. /api/?param=key:value || /api/?param=key1:value1,key2:value2).
    
        --> payload : The arguments supplied with the parameter (The key value pairs in string form).

        <-- The parsed key/value pairs.
    '''

    pairs = {}
    
    for pair_tuple in map(lambda pair: pair.split(':'), [pair for pair in payload.split(',')]):
        pairs[pair_tuple[0]] = pair_tuple[1]

    return pairs

def parse_query_params(payload: str) -> list:
    ''' Parse out one or more parameter values pairs from a query string
        (e.g. /api/?param=value || /api/?param=value1,value2).
    
        --> payload : The arguments supplied with the parameter (The values in string form).

        <-- The parsed values.
    '''

    return [value for value in payload.split(',')]

def get_model(model_name: str) -> API_Model:
    ''' Fetches a model type using a string. Allows far more Django model manager and 
        property access using a passed string.
    
        --> model_name : The name of the model class to retrieve.

        <-- The actual class type with access to model methods or None if not found.
    '''

    try:
        norm_name = '_'.join([chunk.upper() for chunk in model_name.split('_')])

        return apps.get_model('api', norm_name)
    
    except LookupError as e:
        return None