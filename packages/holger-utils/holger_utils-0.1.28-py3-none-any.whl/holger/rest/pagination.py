from rest_framework import pagination
from django.http import JsonResponse
import json


class Pagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        return JsonResponse({
            "count": self.page.paginator.count,
            'current': self.page.number,
            "data": json.loads(json.dumps(data))
        })
