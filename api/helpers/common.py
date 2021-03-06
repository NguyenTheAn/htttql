from django.http import JsonResponse

def json_format(code = 200, message =" Default message", data =  None, errors = None):
    return JsonResponse({
        "code" : code,
        "data" : data,
        'message' : message,
        'errors' : errors
    }, status = code)