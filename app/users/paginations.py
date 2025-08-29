from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class CustomPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'
    max_pagge_size = 100 
    
    def get_paginated_response(self, data):
        return Response({
            'liks': {
                'next' : self.get_next_link(),
                'previous' : self.get_previous_link()
                },
            'count':self.page.paginator.count,
            'total_pages':self.page.paginator.num_pages,
            'current_page': self.page.number,
            'results': data
            
        })

class LargeResultsSetPagination(PageNumberPagination):
    page_size = 50
    max_page_size = 1000
    
class SmallResultsSetPagination(PageNumberPagination):
    page_size = 5
    max_page_size = 50