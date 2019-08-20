from django.shortcuts import render
from django.http import JsonResponse
from . import logger

def GET(request):
    if request.method != 'GET' or 'model' not in request.GET or 'filter' not in request.GET:
        if 'model' not in request.GET:
            logger.error('GET - No model supplied in query parameters!')
        if 'filter' not in request.GET:
            logger.error('GET - No model filter supplied in query parameters!')
        
        return JsonResponse({'model': {}, 'code': 400}, status=400)

    try:
        response = {'model':{}, 'code': 200}

        model = request.GET['model'] 
        model_filter = request.GET['filter'] 

        # TODO - GET MODEL AND ADD TO JSON

        return JsonResponse(response, status=200)

    except Exception as e:
        logger.error('GET - {}'.format(str(e)))
        return JsonResponse({'model': {}, 'code': 404}, status=404)


    
