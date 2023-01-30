import logging

from django.db.utils import IntegrityError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

from reebelo.core.api.result import ErrorCode

logger = logging.getLogger(__name__)


def api_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response:
        return response
    elif isinstance(exc, IntegrityError):

        data = {
            "message": """Data integrity error.  Possibly due to duplicate \
            entry or missing a required related field. Please review \
            your request and try again.""",
            "error_code": ErrorCode.UNIQUE_OR_REQUIRED_FIELD,
        }
        return Response(data, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
