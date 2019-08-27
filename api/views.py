from django.shortcuts import render
from django.http import QueryDict
from .utilities import api_response, log_error, handle_unsupported_method
from .errors import API_Error
from .api_models import api_models
import json, ast

def GET(request):
    try:
        if 'model' not in request.GET:
            raise API_Error('No model supplied in query parameters! (param: model)', 400)

        model_name = request.GET['model'] 
        model_filter = request.GET.get('filter', None) 
        model_sort = request.GET.get('sort', None)

        if model_name not in api_models:
            raise API_Error('Model not found: \'{}\''.format(model_name), 404)

        model = api_models[model_name]

        if 'GET' not in model.supported_methods:
            raise API_Error('Method not supported for model: \'{}\''.format(model_name), 400)

        if not model_filter:
            models = [model.to_json() for model in model.objects.all()]
            return api_response({'models': models}, 200)

        else:
            filter_params = model_filter.split(':')

            if len(filter_params) != 2:
                raise API_Error('Malformatted filter. Format: field:value', 400)

            if filter_params[0] not in [field.name for field in model._meta.fields]:
                raise API_Error('Field \'{}\' not found for model: \'{}\''.format(filter_params[0], model_name), 400)

            models = [model.to_json() for model in model.objects.filter(**{filter_params[0]: filter_params[1]})]

            return api_response({'models': models}, 200)
            
        # TODO - ADD SORT SUPPORT
    
    except Exception as e:
        error_msg = 'GET - {}'.format(str(e)) 
        log_error(error_msg)

        if type(e) == API_Error:
            return api_response({'msg': error_msg}, e.code)

        return api_response({'msg': error_msg}, 500)

def POST(request):
    try:
        if 'model' not in request.POST:
            raise API_Error('No model supplied in POST body! (param: model)', 400)

        model_name = request.POST['model'] 
        model_attrs = request.POST.get('model_attrs', None)

        if model_name not in api_models:
            raise API_Error('Model not found: \'{}\''.format(model_name), 404)

        model = api_models[model_name]

        if 'POST' not in model.supported_methods:
            raise API_Error('Method not supported for model: \'{}\''.format(model_name), 400)

        #TODO - Create the model with specified attributes
        return api_response(code=200)

    except Exception as e:
        error_msg = 'POST - {}'.format(str(e)) 
        log_error(error_msg)

        if type(e) == API_Error:
            return api_response({'msg': error_msg}, e.code)

        return api_response({'msg': error_msg}, 500)

def PUT(request):
    handle_unsupported_method(request)
    
    try:
        if 'model' not in request.POST or 'model_id' not in request.POST or 'model_attrs' not in request.POST:
            if 'model' not in request.POST:
                error_msg = 'No model supplied in PUT body! (param: model)'
            elif 'model_id' not in request.POST:
                error_msg = 'No model ID supplied in PUT body! (param: model_id)'
            elif 'model_attrs' not in request.POST:
                error_msg = 'No attributes to update supplied in PUT body! (param: model_attrs)'
            
            raise API_Error(error_msg, 400)

        model_name = request.POST['model'] 
        model_id = request.POST['model_id'] 
        model_attrs = request.POST['model_attrs'] 

        if model_name not in api_models:
            raise API_Error('Model not found: \'{}\''.format(model_name), 404)

        model = api_models[model_name]

        if 'PUT' not in model.supported_methods:
            raise API_Error('Method not supported for model: \'{}\''.format(model_name), 400)

        # TODO - Get model and replace attributes
        return api_response(code=200)

    except Exception as e:
        error_msg = 'PUT - {}'.format(str(e)) 
        log_error(error_msg)

        if type(e) == API_Error:
            return api_response({'msg': error_msg}, e.code)

        return api_response({'msg': error_msg}, 500)

def DELETE(request):
    handle_unsupported_method(request)

    try:
        if 'model' not in request.POST or 'model_id' not in request.POST:
            if 'model' not in request.POST:
                error_msg = 'No model supplied in DELETE body! (param: model)'    
            elif 'model_id' not in request.POST:
                error_msg = 'No model ID supplied in DELETE body! (param: model_id)'
            
            raise API_Error(error_msg, 400)

        model_name = request.POST['model'] 
        model_filter = request.POST['model_id'] 

        if model_name not in api_models:
            raise API_Error('Model not found: \'{}\''.format(model_name), 404)

        model = api_models[model_name]

        if 'DELETE' not in model.supported_methods:
            raise API_Error('Method not supported for model: \'{}\''.format(model_name), 400)

        # TODO - DELETE MODEL
        return api_response(code=200)

    except Exception as e:
        error_msg = 'DELETE - {}'.format(str(e)) 
        log_error(error_msg)

        if type(e) == API_Error:
            return api_response({'msg': error_msg}, e.code)

        return api_response({'msg': error_msg}, 500)

def http_dispatch(request):

    if request.method == 'GET':
        return GET(request)

    if request.method == 'POST':
        return POST(request)

    if request.method == 'PUT':
        return PUT(request)

    if request.method == 'DELETE':
        return DELETE(request)

    error_msg = 'HTTP - Invalid method: {}'.format(request.method)

    log_error(error_msg)
    return api_response({'msg': error_msg})
    

