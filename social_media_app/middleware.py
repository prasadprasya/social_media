import jwt
from social_media import settings
from .models import Users
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer


class JWTAuthentication:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        print("before")
        response = self.jwt_decode(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    def jwt_decode(self, request):
        current_url = request.path
        if current_url in ('/api/authenticate/', '/api/register/'):
            response = self.get_response(request)
        else:
            token = request.headers.get("token", None)
            if token:
                jwt_payload = jwt.decode(
                    token, settings.SECRET_KEY, algorithms=["HS256"])
                try:
                    user = Users.objects.get(id=jwt_payload['user_id'])
                    request.headers.user_id = user.id
                    response = self.get_response(request)
                except Users.DoesNotExist:
                    response = Response(
                        data="Invalid Authentication",
                        status=403
                    )
                    response.accepted_renderer = JSONRenderer()
                    response.accepted_media_type = "application/json"
                    response.renderer_context = {}
                    response.render()
            else:
                response_data = {"status": False, "response": "Provide Token in Headers For Authentication"}
                response = Response(
                    response_data
                    # data="Provide Token in Headers For Authentication",
                    # status=403
                )
                response.accepted_renderer = JSONRenderer()
                response.accepted_media_type = "application/json"
                response.renderer_context = {}
                response.render()
        return response
    # def jwt_decode(self, request):
    #     current_url = request.path
    #     if current_url in ('/api/authenticate/', '/api/register/'):
    #         response = self.get_response(request)
    #     else:
    #         token = request.Headers
    #         jwt_payload = jwt.decode(
    #             token, settings.SECRET_KEY, algorithms=["HS256"])
    #         try:
    #             user = Users.objects.get(u_uuid=jwt_payload['user_id'])
    #             request.user_id = user.u_uuid
    #             response = self.get_response(request)
    #         except Users.DoesNotExist:
    #             response = Response(
    #                 data="Invalid Authentication",
    #                 status=403
    #             )
    #             response.accepted_renderer = JSONRenderer()
    #             response.accepted_media_type = "application/json"
    #             response.renderer_context = {}
    #             response.render()
    #     return response
