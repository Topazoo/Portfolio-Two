from django.shortcuts import render
from django.http import QueryDict
from .utilities import *
from .errors import *
import json, ast

from django.views.decorators.csrf import csrf_exempt # TODO - Remove (DEBUG)

def GET(request):
    try:
        model_type = fetch_model_type('GET', request.GET)
        filtered_models = fetch_and_filter_models(model_type, request.GET)
        sorted_models = sort_models(model_type, filtered_models, request.GET)

        return api_response({'models': [model.to_json() for model in sorted_models]}, 200 if len(sorted_models) > 0 else 404)
    
    except Exception as exception:
        return api_error_response('GET', exception)


def POST(request):
    try:
        if len(request.POST) == 0:
            handle_unsupported_method(request)

        model_type = fetch_model_type('POST', request.POST)

        create_or_update_model(model_type, request_params=request.POST)

        return api_response(code=200)

    except Exception as exception:
        return api_error_response('POST', exception)


def PUT(request):
    try:
        handle_unsupported_method(request)

        model_type = fetch_model_type('PUT', request.POST)
        model = fetch_and_filter_models(model_type, request.POST).get()

        create_or_update_model(model_type, model, request.POST)

        return api_response(code=200)

    except Exception as exception:
        return api_error_response('PUT', exception)


def DELETE(request):
    try:
        handle_unsupported_method(request)

        model_type = fetch_model_type('DELETE', request.POST)
        model = fetch_and_filter_models(model_type, request.POST).get()

        model.delete()

        return api_response(code=200)

    except Exception as exception:
        return api_error_response('DELETE', exception)

@csrf_exempt # TODO - Remove (DEBUG)
def api(request):

    if request.method == 'GET':
        return GET(request)

    if request.method == 'POST':
        return POST(request)

    if request.method == 'PUT':
        return PUT(request)

    if request.method == 'DELETE':
        return DELETE(request)

    return api_error_response('HTTP', API_Error('Invalid method: {}'.format(request.method), 405))
