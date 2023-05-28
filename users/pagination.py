from rest_framework.pagination import PageNumberPagination

class SearchHistoryPagination(PageNumberPagination):
  page_size = 5