from rest_framework.response import Response

def api_response(message, status_flag, data=None, http_status=200):
    return Response({
        "message": message,
        "status": status_flag,
        "data": data
    }, status=http_status)