from django.shortcuts import render
from django.http import HttpRequest, JsonResponse, QueryDict
from .utilities import *
from .errors import *
import json

from django.views.decorators.csrf import csrf_exempt # TODO - Remove (DEBUG)

def GET(request: HttpRequest) -> JsonResponse:
    ''' Fetch model data from the server or respond with the appropriate HTTP status code on error. 
    
        The request query string must supply the model's (class) name. It may also supply one or more optional 
        filter and sort parameters matching the parameters for Django's filter() and order_by() Queryset methods:
        https://docs.djangoproject.com/en/2.2/ref/models/querysets/#field-lookups
        https://docs.djangoproject.com/en/2.2/ref/models/querysets/#order-by

        --> request : The GET request sent to the server.

        <-- JSON containing the HTTP status code signifying the request's success or failure and
            a list of models matching the supplied parameters if the request did not fail.

            GET Request Formats:
                All - Get all models.
                    /api/?model=<<model>>
                    
                Filtering - Get all models of type (class) <<model>> with field(s) matching the provided value(s).
                    /api/?model=<<model>>&filter=<<field>>:<<value>>
                    /api/?model=<<model>>&filter=<<field1>>:<<value1>>,<<field2>>:<<value2>>
                                                                        
                Sorting - Get all models of type (class) <<model>> sorted by the provieded field(s). 
                    /api/?model=<<model>>&sort=<<field>>
                    /api/?model=<<model>>&sort=<<field1>>,<<field2>>

                Filtering + Sorting - Get all models of type (class) <<model>> with field(s) matching the provided 
                                      value(s) sorted by the provided field(s).
                    
                    /api/?model=<<model>>&filter=<<field1>>,<<field2>>:<<value>>&sort=<<field1>> 

            GET Response Format:
                {"models": [models], "code": <<code>>}            
    '''
    
    try:
        model_type = fetch_model_type('GET', request.GET)
        filtered_models = fetch_and_filter_models(model_type, request.GET)
        sorted_models = sort_models(model_type, filtered_models, request.GET)

        return api_response({'models': [model.to_json() for model in sorted_models]}, 200 if len(sorted_models) > 0 else 404)
    
    except Exception as exception:
        return api_error_response('GET', exception)


def POST(request: HttpRequest) -> JsonResponse:
    ''' Create a new model or respond with the appropriate HTTP status code on error. 
        
        The request body must supply the model's (class) name. It may also supply a dictionary of 
        one or more field/value pairs to create the model with.

        --> request : The POST request sent to the server.

        <-- JSON containing the HTTP status code signifying the request's success or failure.

            POST Body Formats:
                Empty - Create a new <<model>> with all fields empty.
                    {"model": <<model>>}

                With Fields - Create a new <<model>> with the provided fields set.
                    { "model": <<model>>, "fields": {<<field1>>: <<value1>>, <<field2>>: <<value2>>} }

            POST Response Format:
                {"code": <<code>>}            
    '''

    try:
        if len(request.POST) == 0:
            handle_unsupported_method(request)

        model_type = fetch_model_type('POST', request.POST)
        create_or_update_model(model_type, request_params=request.POST)

        return api_response(code=200)

    except Exception as exception:
        return api_error_response('POST', exception)


def PUT(request: HttpRequest) -> JsonResponse:
    ''' Update a model or respond with the appropriate HTTP status code on error. 
        
        The request body must supply the model's (class) name and a dictionary of 
        one or more field/value pairs to update the model with. It should also supply 
        one or more optional filter parameters matching the parameters for Django's 
        Queryset.filter() method. 
        
        *The filter parameters must match only the model being updated*
        
        --> request : The PUT request sent to the server.

        <-- JSON containing the HTTP status code signifying the request's success or failure.

            PUT Body Format:
                { 
                    "model": <<model>>, 
                    "filter": {<<field1>>: <<value1>>, <<field2>>: <<value2>>},
                    "fields": {<<field1>>: <<value1>>, <<field3>>: <<value3>>} 
                }

            PUT Response Format:
                {"code": <<code>>}            
    '''

    try:
        handle_unsupported_method(request)

        model_type = fetch_model_type('PUT', request.POST)
        model = fetch_and_filter_models(model_type, request.POST).get()

        create_or_update_model(model_type, model, request.POST)

        return api_response(code=200)

    except Exception as exception:
        return api_error_response('PUT', exception)


def DELETE(request: HttpRequest) -> JsonResponse:
    ''' Delete a model or respond with the appropriate HTTP status code on error. 
        
        The request body must supply the model's (class) name. It should also supply 
        one or more optional filter parameters (matching the parameters for Django's 
        Queryset.filter() method). 
        
        *The filter parameters must match only a single model*
        
        --> request : The DELETE request sent to the server.

        <-- JSON containing the HTTP status code signifying the request's success or failure.

            DELETE Body Format:
                { "model": <<model>>, "filter": {<<field1>>: <<value1>>, <<field2>>: <<value2>>} }

            DELETE Response Format:
                {"code": <<code>>}            
    '''

    try:
        handle_unsupported_method(request)

        model_type = fetch_model_type('DELETE', request.POST)
        model = fetch_and_filter_models(model_type, request.POST).get()

        model.delete()

        return api_response(code=200)

    except Exception as exception:
        return api_error_response('DELETE', exception)

@csrf_exempt # TODO - Remove (DEBUG)
def api(request: HttpRequest) -> JsonResponse:
    ''' Called when the /api/ endpoint is sent an HTTP request. Delegates 
        to the appropriate handler based on the request method or returns a JSON
        formatted error if the method is not supported.

        --> request : The HTTP request sent to the server.

        <-- JSON containing the HTTP status code signifying the request's success or failure and
            all other data returned from the server.
    '''
    
    if request.method == 'GET':
        return GET(request)

    if request.method == 'POST':
        return POST(request)

    if request.method == 'PUT':
        return PUT(request)

    if request.method == 'DELETE':
        return DELETE(request)

    return api_error_response('HTTP', API_Error('Invalid method: {}'.format(request.method), 405))
