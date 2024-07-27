# from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError

# ValidationError
from django.http import JsonResponse, Http404
from django.conf import settings
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response


class ResponseManager:
    def __init__(self, request):
        self.request = request
        self.headers = {}
        self.auth = {}
        self.debug = []

    def response(self, content, status_code, message=None):
        response_data = self.normalize_content(content, status_code, message)
        response = Response(data=response_data, status=status_code, headers=self.headers)

        return response
    def register_auth(self, auth):
        self.auth.update(auth)

    def normalize_content(self, content, status_code, message=None):
        schema = {
            "error": not self.is_successful_code(status_code),
            "message": message or self.get_default_message(status_code),
            "code": status_code,
            "data": content,
        }

        if settings.DEBUG:
            schema["debug"] = self.debug

        return schema

    def is_successful_code(self, status_code):
        return 200 <= status_code < 300

    def get_default_message(self, status_code):
        return {
            status.HTTP_200_OK: "OK",
            status.HTTP_201_CREATED: "Created",
            status.HTTP_400_BAD_REQUEST: "Bad Request",
            status.HTTP_404_NOT_FOUND: "Not Found",
            status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal Server Error",
        }.get(status_code, "")

    def catch(self, exception):
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        message = str(exception)
        content = None

        if isinstance(exception, Http404):
            status_code = status.HTTP_404_NOT_FOUND
            message = "Not Found"
        elif isinstance(exception, ValidationError):
            status_code = status.HTTP_400_BAD_REQUEST
            message = str(exception.detail)
            content = "exception.detail"
        elif isinstance(exception, ObjectDoesNotExist):
        # else:
            status_code = status.HTTP_404_NOT_FOUND
            message = "Object Not Found"

        if settings.DEBUG:
            self.debug = {
                "type": type(exception).__name__,
                # "message": str(exception['detail']),
                "args": exception,
            }

        return self.response(content, status_code, message)

    def stored(self, content, message=None):
            return self.response(content, status.HTTP_201_CREATED, message)

    def updated(self, content, message=None):
            return self.response(content, status.HTTP_202_ACCEPTED, message)

    def destroyed(self, content, message=None):
            return self.updated(content, message)

    def ok(self, content=None):
            return self.response(content, status.HTTP_200_OK)
