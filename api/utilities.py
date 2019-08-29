
from django.http import JsonResponse, HttpRequest, QueryDict
from django.db.models.query import QuerySet
from django.conf import settings
from django.apps import apps
from .errors import API_Error
from .models import API_Model
from typing import Type
import logging, json

def api_response(content: dict = {}, code: int = 400) -> JsonResponse:
    ''' Format an API JSON response.

        --> content [dict] : A dictionary of JSON serializable objects to return. Optional.
        
        --> code [int]: The HTTP status code to return. Optional.
        
        <-- The JSON formatted response. { <<content>>, "code": <<code>> }
    '''

    content['code'] = code
    
    return JsonResponse(content, status=code)


def api_error_response(method: str, exception: Exception) -> JsonResponse:
    ''' Format an API JSON response.

        --> method : The HTTP request method that generated the error (e.g. POST).
        
        --> exception : The error generated.
        
        <-- A JSON formatted error response : { "msg" <<error_message>>, "code": <<code>> }.
    '''

    error_msg = '{} - {}'.format(method, str(exception)) 
    error_code = exception.code if type(exception) == API_Error else 500
    
    log_error(error_msg)

    return api_response({'msg': error_msg}, error_code)


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


def validate_fields(fields: [dict, list], model_type: API_Model):
    ''' Ensure that the model fields passed to an API call exist for that model.
    
        --> fields : A list or dictionary (from GET querystring or a request body) of
                     the fields passed to the request.
        
        --> model_type Type[API_Model] : The type (class) of the model (must be derived from the 
                                         base API model class defined in api/models.py).
    '''
    
    model_fields = [field.name for field in model_type._meta.fields]
    for field in fields:
        if field not in model_fields:
            raise API_Error('Field \'{}\' not found for model: \'{}\''.format(field, model_type.__name__), 400)


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


def get_model(model_name: str) -> Type[API_Model]:
    ''' Fetches a model type using a string. Allows far more Django model manager and 
        property access using a passed string.
    
        --> model_name : The name of the model class to retrieve.

        <-- The actual class type with access to model methods or None if not found.
    '''

    try:
        norm_name = '_'.join([chunk.upper() for chunk in model_name.split('_')])

        return apps.get_model('api', norm_name)
    
    except LookupError as e: pass


def fetch_model_type(method: str, request_params: dict) -> Type[API_Model]:
    ''' Ensures the request references a defined model and fetches that model type if the request method
        is allowed for that model.
    
        --> method : The method of the HTTP request (e.g. POST).

        --> request_params : The parameters sent with the request (in querystring or body).

        <-- The actual class type with access to model methods or None if not found.
    '''

    if 'model' not in request_params:
        raise API_Error('No model supplied in query parameters! (param: model)', 400)

    model_name = request_params['model'] 
    model_type = get_model(model_name)
        
    if not model_type:
        raise API_Error('Model not found: \'{}\''.format(model_name), 404)

    if method not in model_type.supported_methods and 'ALL' not in model_type.supported_methods:
        raise API_Error('Method not supported for model: \'{}\''.format(model_name), 405)

    return model_type


def fetch_and_filter_models(model_type: API_Model, request_params: dict) -> QuerySet:
    ''' Fetch models from the database matching a filter supplied in an HTTP request.
        Ensure fields supplied in the filter exist for the model. If no filter is supplied
        all objects are retrived.
    
        --> model_type Type[API_Model] : The type (class) of the model being updated. Used 
                                         to validate the filter parameters.

        --> request_params : The parameters sent with the request (in querystring or body).

        <-- A queryset containing the models matching the supplied filter or all objects of the
            supplied model.
    '''

    model_filter = request_params.get('filter', {}) 
    if model_filter != {}:
        if type(model_filter) == str:
            model_filter = parse_query_pairs(model_filter)
            
        validate_fields([param.split('_')[0] for param in model_filter], model_type)

        return model_type.objects.filter(**model_filter)

    return model_type.objects.all()
    
def sort_models(model_type: API_Model, models: QuerySet, request_params: dict) -> QuerySet:
    ''' Sorts a queryset of models according to the parameters sent in an HTTP request.
        Ensure fields supplied in the sort exist for the model.

        --> model_type Type[API_Model] : The type (class) of the model being updated. Used 
                                         to validate the sort parameters.

        --> models : The queryset of models to apply the sort to.
    
        --> request_params : The parameters sent with the request (in querystring or body).

        <-- A queryset containing the sorted models.
    '''

    model_sort = request_params.get('sort', {})

    if model_sort != {}:
        if type(model_sort) == str:
            model_sort = parse_query_params(model_sort)

        validate_fields([param if param[0] != '-' else param[1::] for param in model_sort], model_type)

        return models.order_by(*model_sort)

    return models

def create_or_update_model(model_type: API_Model, model: API_Model = None, request_params: dict = {}) -> QuerySet:
    ''' Create or update a model with the parameters sent in an HTTP request.
        Ensure fields to update exist for the model.

        --> model_type Type[API_Model] : The type (class) of the model being updated. Used 
                                         to validate the fields being updated.

        --> model [API_Model] : The model to update. Optional - A new model is created if not set.
    
        --> request_params [dict] : The parameters sent with the request (in querystring or body).
    '''

    model_fields = request_params.get('fields', {})

    if model_fields != {}:
        validate_fields([field for field in model_fields], model_type)

        if type(model_fields) == str:
            model_fields = parse_query_pairs(model_fields)

        if model:
            [model.__setattr__(field, model_fields[field]) for field in model_fields]

    if not model:
        model = model_type(**model_fields)

    model.save()
