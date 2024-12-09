from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from django.db.models.query import prefetch_related_objects
from rest_framework.pagination import PageNumberPagination
from rest_framework.settings import api_settings

class KtModelViewSet(viewsets.ModelViewSet):
    """
    A custom ModelViewSet that extends the default functionality.
    """

    def get_object(self):
        """
        Override the get_object method to use the custom manager's get_object method.
        """
        queryset = self.filter_queryset(self.get_queryset())
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            f'Expected view {self.__class__.__name__} to be called with a URL keyword argument '
            f'named "{lookup_url_kwarg}". Fix your URL conf, or set the `.lookup_field` '
            f'attribute on the view correctly.'
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = queryset.model.objects.get_object(**filter_kwargs)
        self.check_object_permissions(self.request, obj)
        return obj

    def list(self, request, *args, **kwargs):
        """
        List all objects.
        """
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        Create a new object.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        """
        Save the new object.
        """
        serializer.save()

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a single object.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        """
        Update an object.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        """
        Save the updated object.
        """
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        """
        Partially update an object.
        """
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
    def destroy(self, request, *args, **kwargs):
        """
        Override the destroy method to handle soft deletes.
        """
        instance = self.get_object()
        manager_name = type(instance)._default_manager.__class__.__name__
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        """
        Perform the destroy action using the custom manager's delete method.
        """
        manager = type(instance)._default_manager
        manager.soft_delete(instance)


from rest_framework.pagination import PageNumberPagination


class KtPagination(PageNumberPagination):
    page_size = 30

    def get_next(self):
        if not self.page.has_next():
            return None
        page_number = self.page.next_page_number()
        return page_number

    def get_previous(self):
        if not self.page.has_previous():
            return None
        page_number = self.page.previous_page_number()
        return page_number
    def get_paginated_response(self, data, message):

        return Response(
            {
                "recordLength": self.page.paginator.count,
                "total": self.page.paginator.num_pages,
                'next': self.get_next(),
                'previous': self.get_previous(),
                "payload": data,
                "message": message,
                "statusCode": status.HTTP_201_CREATED,
            }
        )


class CreateModelMixin:
    """
    Create a model instance.
    """

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        message = self.get_message()
        return Response(
            {
                "payload": serializer.data,
                "message": message,
                "statusCode": status.HTTP_201_CREATED,
            },
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    def get_message(self, *args, **kwargs):
        """
        Returns a default success message for create operations.
        """
        return f"{self.model_name} Created Successfully"

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {"Location": str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


class ListModelMixin:
    """
    List a queryset.
    """

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        message = self.get_message()
        return Response(
            {
                "payload": serializer.data,
                "message": message,
                "recordLength": queryset.count(),
                "statusCode": status.HTTP_200_OK,
            },
            status=status.HTTP_200_OK,
        )

    def get_message(self, *args, **kwargs):
        """
        Returns a default success message for list operations.
        """
        return f"{self.model_name} listed Successfully"


class RetrieveModelMixin:
    """
    Retrieve a model instance.
    """

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        message = self.get_message()
        return Response(
            {
                "payload": serializer.data,
                "message": message,
                "statusCode": status.HTTP_200_OK,
            },
            status=status.HTTP_200_OK,
        )

    def get_message(self, *args, **kwargs):
        """
        Returns a default success message for list operations.
        """
        return f"{self.model_name} listed Successfully"


class UpdateModelMixin:
    """
    Update a model instance.
    """

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        queryset = self.filter_queryset(self.get_queryset())
        if queryset._prefetch_related_lookups:
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance,
            # and then re-prefetch related objects
            instance._prefetched_objects_cache = {}
            prefetch_related_objects([instance], *queryset._prefetch_related_lookups)
        message = self.get_message()
        return Response(
            {
                "payload": serializer.data,
                "message": message,
                "statusCode": status.HTTP_200_OK,
            },
            status=status.HTTP_200_OK,
        )

    def get_message(self, *args, **kwargs):
        """
        Returns a default success message for list operations.
        """
        return f"{self.model_name} updated Successfully"

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)


class DestroyModelMixin:
    """
    Destroy a model instance.
    """

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        message = self.get_message()
        return Response(
            {
                "message": message,
                "statusCode": status.HTTP_204_NO_CONTENT,
            },
            status=status.HTTP_204_NO_CONTENT,
        )

    def get_message(self, *args, **kwargs):
        """
        Returns a default success message for list operations.
        """
        return f"{self.model_name} deleted Successfully"

    def perform_destroy(self, instance):
        instance.delete()


class ModelViewSet(
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
):
    """
    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.
    """

    pass
