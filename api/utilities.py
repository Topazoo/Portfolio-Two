
from django.http import JsonResponse
from django.conf import settings
from django.apps import apps
from .errors import API_Error
import logging, json

def api_response(content = {}, code = 400):
    ''' Format an API JSON response.

        --> (dict) content : A dictionary of JSON serializable objects to return. Optional.
        
        --> (int) code : The HTTP status code to return. Optional.
        
        <-- (JsonResponse) : The JSON formatted response. { <<content>>, "code": <<code>> }
    '''

    content['code'] = code
    return JsonResponse(content, status=code)

def log_error(message):
    ''' Logs an API error to /logs/api.log if LOG_ERRORS is True in settings.

        --> (string) message : The message to log.
    '''

    if settings.DEBUG:
        logger = logging.getLogger('api')
        logger.error(message)

def handle_unsupported_method(request):
    ''' Fallback to find query parameters for unsuported methods and encodings.
        Decodes the body of the request object and adds it to the request's POST
        field.

        --> (HttpRequest) request : The request sent to the API.
     '''

    if len(request.body) > 2:
        request.POST = dict(request.POST)
        request.POST.update(json.loads(request.body.decode('utf-8').replace('\'', '\"')))

def validate_fields(fields, model):
    ''' Ensure that the model fields passed to an API call exist for that model.
    
        --> (dict || list) fields : The fields passed to the request.
        
        --> (API_Model) model : A model derived from the base class defined in api/models.py.
    '''
    
    model_fields = [field.name for field in model._meta.fields]

    for field in fields:
        if field not in model_fields:
            raise API_Error('Field \'{}\' not found for model: \'{}\''.format(field, model.__name__), 400)


def parse_query_pairs(payload):
    ''' Parse out one or more key/value pairs from a query string
        (e.g. /api/?param=key:value || /api/?param=key1:value1+key2:value2).
    
        --> (str) payload : The arguments supplied with the parameter (The key value pairs in string form).

        <-- (dict) : The parsed key/value pairs.
    '''

    pairs = {}
    for pair_tuple in map(lambda pair: pair.split(':'), [pair for pair in payload.split('+')]):
        pairs[pair_tuple[0]] = pair_tuple[1]

    return pairs

def get_model(model_name):
    ''' Fetches a model type using a string. Allows far more Django model manager and 
        property access using a passed string.
    
        --> (str) model_name : The name of the model class to retrieve.

        <-- (type<API_Model> || None) : The actual class type with access to model methods. None if not found.
    '''
    
    try:
        norm_name = '_'.join([chunk.upper() for chunk in model_name.split('_')])

        return apps.get_model('api', norm_name)
    
    except LookupError as e:
        return None