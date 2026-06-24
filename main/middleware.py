from django.http import JsonResponse

class ApiExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)

            if response.status_code == 404 :
                return JsonResponse({
                    "message": "Not Found",
                    "status": False,
                    "status_code": 404,
                    "data": None
                }, status=404)
            
            return response

        except Exception as e:
    
                return JsonResponse({
                    "message": str(e),
                    "status": False,
                    "status_code": 500,
                    "data": None
                }, status=500)

          