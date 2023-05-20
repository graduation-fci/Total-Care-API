from rest_framework.pagination import PageNumberPagination

class DefaultPagination(PageNumberPagination):
  page_size = 10
  
  
class CategoriesPagination(PageNumberPagination):
  page_size = 12