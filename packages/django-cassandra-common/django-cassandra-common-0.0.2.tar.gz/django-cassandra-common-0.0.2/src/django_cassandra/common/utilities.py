from django.conf import settings
from drf_yasg.generators import OpenAPISchemaGenerator
from rest_framework import serializers


class Enums:
    LIST_STATUS = ['ACTIVO', 'INACTIVO']
    ACTIVO = 'ACTIVO'
    INACTIVO = 'INACTIVO'
    SALE_ABIERTA = 'ABIERTA'
    SALE_ANULADA = 'ANULADA'
    SALE_CERRADA = 'CERRADA'
    LIST_SALE_STATUS = [SALE_ABIERTA, SALE_ANULADA, SALE_CERRADA]


class Constants:
    FORMAT_DATE_TIME = '%Y-%m-%d %H:%M:%S'
    FORMAT_DATE = '%Y-%m-%d'
    FORMAT_TIME = '%H:%M:%S'
    FORMAT_DATE_TIME_TIMEZONE = '%Y-%m-%dT%H:%M:%S.%fZ'


class DynamicFieldsSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        notfields = kwargs.pop('notfields', None)

        super(DynamicFieldsSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            existing = set(self.fields.keys())
            if not isinstance(fields, str):
                allowed = set(fields)
                for field_name in existing - allowed:
                    self.fields.pop(field_name)
            else:
                for field_name in existing:
                    if field_name != fields:
                        self.fields.pop(field_name)

        elif notfields is not None:
            existing = set(self.fields.keys())
            if not isinstance(notfields, str):
                disallowed = set(notfields)
                for field_name in disallowed:
                    if field_name in existing:
                        self.fields.pop(field_name)
            else:
                self.fields.pop(notfields)


class CustomOpenAPISchemaGenerator(OpenAPISchemaGenerator):

    def get_schema(self, *args, **kwargs):
        schema = super().get_schema(*args, **kwargs)
        base_path = getattr(settings, 'CUSTOM_SWAGGER', {})
        schema.basePath = base_path['BASE_PATH']
        return schema
