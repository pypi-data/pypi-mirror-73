from django_cassandra.common.messages import Messages
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'paginator': {
                'count': self.page.paginator.count,
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'status': True,
            'message': Messages.SUCCESSFUL_MESSAGE,
            'data': data
        })
