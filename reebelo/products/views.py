import urllib.parse
from collections import namedtuple

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import CursorPagination
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from reebelo.core.exceptions import NotFoundError
from reebelo.products.exceptions import InsufficientQuantity

from .serializers import (
    CreateProductSerializer,
    ProductSerializer,
    UpdateProductSerializer,
)
from .service import ProductService

Cursor = namedtuple("Cursor", ["offset", "reverse", "position"])


class CursorSetPagination(CursorPagination):
    page_size = 50
    page_size_query_param = "page_size"
    ordering = "name"

    def get_paginated_response(self, data):
        next_link = self.get_next_link()
        parsed = urllib.parse.urlparse(next_link)
        query_params = urllib.parse.parse_qs(parsed.query)
        next_cursor = query_params.get("cursor", [None])[0]

        return Response(
            {
                "next": next_link,
                "previous": self.get_previous_link(),
                "next_cursor": next_cursor,
                "results": data,
            }
        )


class ProductViewSet(CursorSetPagination, ViewSet):
    pagination_class = CursorSetPagination
    serializer_class = ProductSerializer

    def create(self, request):
        try:
            serializer = CreateProductSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            data = serializer.validated_data
            product = ProductService.create(
                name=data["name"],
                quantity=data["quantity"],
                price=data["price"],
            )
            response_serializer = ProductSerializer(product)
            return Response(response_serializer.data)
        except ValidationError as e:
            errors = {}
            for k, v in e.detail.items():
                errors[k] = map(lambda detail: detail.title(), v)
            return Response(errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def list(self, request):
        params = request.query_params
        search = params.get("search", "")
        queryset = ProductService.list(search=search)
        page = self.paginate_queryset(queryset=queryset, request=request)
        if page is not None:
            serializer = ProductSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        try:
            serializer = UpdateProductSerializer(data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)

            data = serializer.validated_data
            product = ProductService.update(id=pk, **data)
            response_serializer = ProductSerializer(product)
            return Response(response_serializer.data)
        except ValidationError as e:
            errors = {}
            for k, v in e.detail.items():
                errors[k] = map(lambda detail: detail.title(), v)
            return Response(errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except InsufficientQuantity as e:
            error = {"error_code": e.error.code, "message": e.error.message}
            return Response(error, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def delete(self, request, pk: int):
        try:
            ProductService.delete(pk)
            return Response(status=status.HTTP_200_OK)
        except NotFoundError:
            return Response(status=status.HTTP_404_NOT_FOUND)
