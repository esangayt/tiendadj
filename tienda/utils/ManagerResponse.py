from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.http.response import HttpResponseBase
from django.utils.cache import cc_delim_re, patch_vary_headers
from django.utils.encoding import smart_str
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
import traceback
from rest_framework.views import set_rollback

from rest_framework import exceptions, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.schemas import DefaultSchema
from rest_framework.settings import api_settings
from rest_framework.utils import formatting
import sys


def custom_exception_handler(exc, context):
    """
    Returns the response that should be used for any given exception.

    By default we handle the REST framework `APIException`, and also
    Django's built-in `Http404` and `PermissionDenied` exceptions.

    Any unhandled exceptions may return `None`, which will cause a 500 error
    to be raised.
    """
    if isinstance(exc, Http404):
        exc = exceptions.NotFound(*(exc.args))
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied(*(exc.args))

    if isinstance(exc, exceptions.APIException):
        headers = {}
        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header
        if getattr(exc, 'wait', None):
            headers['Retry-After'] = '%d' % exc.wait

        if isinstance(exc.detail, (list, dict)):
            data = exc.detail
        else:
            data = {'detail': exc.detail}

        # print(exc.detail.get('type_invoce')[0])
        # print(exc.get_full_details())
        # print(exc.get_codes())
        # print(exc.with_traceback())
        # print(traceback.print_exc())
        # print(traceback.format_stack()
        # print(sys.exception())
        # print(traceback.format_list())
        # print(traceback.extract_stack(exc))
        # print(traceback.format_per())

        trace_list = traceback.format_exception(sys.exception(), limit=None, chain=True)

        schema = {
            "error": 200 >= exc.status_code < 300,
            "message": exc.get_full_details(),
            "code": exc.status_code,
            "data": None,
        }

        if settings.DEBUG:
            schema["debug"] = {
                "type": type(exc).__name__,
                "details": traceback.format_exception_only(sys.exception()),
                # "details": exc.get_full_details(),
                # "traceback": traceback.format_per(),
                "traceback": trace_list,
            }

        set_rollback()
        return Response(schema, status=exc.status_code, headers=headers)

    return None
