from django.shortcuts import render
from django.http import QueryDict
from .utilities import *
from .errors import *
import json, ast

#from django.views.decorators.csrf import csrf_exempt # TODO - Remove (DEBUG)

def GET(request):
    try:
        if 'model' not in request.GET:
            raise API_Error('No model supplied in query parameters! (param: model)', 400)

        model_name = request.GET['model'] 
        model_filter = request.GET.get('filter', None) 
        model_sort = request.GET.get('sort', None)

        model = get_model(model_name)
        if not model:
            raise API_Error('Model not found: \'{}\''.format(model_name), 404)

        if 'GET' not in model.supported_methods:
            raise API_Error('Method not supported for model: \'{}\''.format(model_name), 400)

        if model_filter:
            filter_params = parse_query_pairs(model_filter)
            validate_fields([param for param in filter_params], model)
            models = model.objects.filter(**filter_params)

        else:
            models = model.objects.all()

        if model_sort:
            sort_params = parse_query_params(model_sort)
            models = models.order_by(*sort_params)

        return api_response({'models': [model.to_json() for model in models]}, 200 if len(models) > 0 else 404)
    
    except Exception as e:
        error_msg = 'GET - {}'.format(str(e)) 
        log_error(error_msg)

        if type(e) == API_Error:
            return api_response({'msg': error_msg}, e.code)

        return api_response({'msg': error_msg}, 500)

def POST(request):
    if len(request.POST) == 0:
        handle_unsupported_method(request)

    try:
        if 'model' not in request.POST:
            raise API_Error('No model supplied in POST body! (param: model)', 400)

        model_name = request.POST['model'] 
        model_attrs = request.POST.get('model_attrs', None)

        model = get_model(model_name)
        if not model:
            raise API_Error('Model not found: \'{}\''.format(model_name), 404)

        if 'POST' not in model.supported_methods:
            raise API_Error('Method not supported for model: \'{}\''.format(model_name), 400)

        if model_attrs:
            if type(model_attrs) == str:
                model_attrs = parse_query_pairs(model_attrs)
            
            validate_fields([attr for attr in model_attrs], model)

            model(**model_attrs).save()
        
        else:
            model().save()
            
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

        model = get_model(model_name)
        if not model:
            raise API_Error('Model not found: \'{}\''.format(model_name), 404)

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

        model = get_model(model_name)
        if not model:
            raise API_Error('Model not found: \'{}\''.format(model_name), 404)

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

#@csrf_exempt # TODO - Remove (DEBUG)
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
    

