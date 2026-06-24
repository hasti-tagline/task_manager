from rest_framework.renderers import JSONRenderer
                                        
class CustomRenderer(JSONRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):

        response = renderer_context["response"]

        if response.exception:
            message = "Error"

            if isinstance(data, dict):
                message = data.get("detail") or data.get("message") or "Error"

            response_data = {
                "message": message,
                "status": False,
                "status_code": response.status_code,
                "data": None
            }

        else:
            response_data = {
                "message": "Success",
                "status": True,
                "status_code": response.status_code,
                "data": data
            }

        return super().render(response_data, accepted_media_type, renderer_context)