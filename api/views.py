from django.shortcuts import render
from django.http import QueryDict
from .utilities import api_response, log_error, handle_unsupported_method
import json

def GET(request):
    error_msg = ''

    if 'model' not in request.GET or 'filter' not in request.GET:
        if 'model' not in request.GET:
            error_msg = 'GET - No model supplied in query parameters! (param: model)'
        elif 'filter' not in request.GET:
            error_msg = 'GET - No model filter supplied in query parameters! (param: filter)'
        
        log_error(error_msg)
        return api_response({'msg': error_msg})

    try:
        model = request.GET['model'] 
        model_filter = request.GET['filter'] 
        model_sort = request.GET.get('sort', None)

        model_obj = {} # TODO - GET MODEL AND ADD TO JSON
        return api_response({'model': model_obj}, 200)

    except Exception as e:
        error_msg = 'GET - {}'.format(str(e))
        return api_response({'model': {}, 'msg': error_msg}, 404) #TODO - Seperate 404s and 500s

def POST(request):
    error_msg = ''

    if 'model' not in request.POST:
        error_msg = 'POST - No model supplied in POST body! (param: model)'
        
        log_error(error_msg)
        return api_response({'msg': error_msg})

    try:
        model = request.POST['model'] 
        model_attrs = request.POST.get('model_attrs', None)

        #TODO - Create the model with specified attributes
        return api_response(code=200)

    except Exception as e:
        error_msg = 'POST - {}'.format(str(e))
        return api_response({'msg': error_msg}, 500)

def PUT(request):
    error_msg = ''

    handle_unsupported_method(request)

    if 'model' not in request.POST or 'model_id' not in request.POST or 'model_attrs' not in request.POST:
        if 'model' not in request.POST:
            error_msg = 'PUT - No model supplied in PUT body! (param: model)'
        elif 'model_id' not in request.POST:
            error_msg = 'PUT - No model ID supplied in PUT body! (param: model_id)'
        elif 'model_attrs' not in request.POST:
            error_msg = 'PUT - No attributes to update supplied in PUT body! (param: model_attrs)'
        
        log_error(error_msg)
        return api_response({'msg': error_msg})

    try:
        model = request.POST['model'] 
        model_id = request.POST['model_id'] 
        model_attrs = request.POST['model_attrs'] 

        # TODO - Get model and replace attributes
        return api_response(code=200)

    except Exception as e:
        error_msg = 'PUT - {}'.format(str(e))
        log_error(error_msg)

        return api_response({'msg': error_msg}, 404) #TODO - Seperate 404s and 500s

def DELETE(request):
    error_msg = ''

    handle_unsupported_method(request)

    if 'model' not in request.POST or 'model_id' not in request.POST:
        if 'model' not in request.POST:
            error_msg = 'DELETE - No model supplied in DELETE body! (param: model)'    
        elif 'model_id' not in request.POST:
            error_msg = 'DELETE - No model ID supplied in DELETE body! (param: model_id)'
        
        log_error(error_msg)
        return api_response({'msg': error_msg})

    try:
        model = request.POST['model'] 
        model_filter = request.POST['model_id'] 

        # TODO - DELETE MODEL
        return api_response(code=200)

    except Exception as e:
        error_msg = 'DELETE - {}'.format(str(e))
        log_error(error_msg)
        
        return api_response({'msg': error_msg}, 404) #TODO - Seperate 404s and 500s

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
    
