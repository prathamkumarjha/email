
import math

from django.http import JsonResponse
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext
from django.core.exceptions import PermissionDenied
from django.http import Http404
from rest_framework import exceptions, status
from rest_framework.response import Response
from rest_framework import status
from rest_framework.utils.serializer_helpers import ReturnDict, ReturnList
from django.db import connections, models
from fixflight.apps.utilities.logger_flight import get_logger
from rest_framework.views import exception_handler as drf_exception_handler
import traceback
import sys
logger = get_logger()

def set_rollback():
    for db in connections.all():
        if db.settings_dict["ATOMIC_REQUESTS"] and db.in_atomic_block:
            db.set_rollback(True)

def custom_exception_handler(exc, context):
    response = drf_exception_handler(exc, context)
    trace = traceback.format_exc()
        
    # Log the detailed traceback with line number, filename, etc.
    logger.error(f"Exception occurred: {exc.__class__.__name__}")
    logger.error(f"Traceback: {trace}")
    if response is not None:
        custom_response_data = {
            "statusCode": response.status_code,
            "message": response.data.get("detail", "An error occurred"),
        }

        if isinstance(response.data, dict):
            custom_response_data["error"] = response.data

        response.data = custom_response_data
    else:
        response = Response(
            {
                "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "Internal Server Error",
                "error": str(exc),
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    set_rollback()
    return response