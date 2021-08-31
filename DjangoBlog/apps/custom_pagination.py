from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return {
            'next' : self.get_next_link(),
            'previous' : self.get_previous_link(),
            'current_page' : self.get_page_number(self.request, self),
            'total_page' : self.page.paginator.num_pages,
            'results' : data,
        }