from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters

User = get_user_model()

class UserFilter(filters.FilterSet):
    class Meta:
        model = User
        fields = {
            'email': ['exact', 'contains'],
            'first_name': ['exact', 'contains'],
            'last_name': ['exact', 'contains'],
            'is_active': ['exact'],
            'is_superuser': ['exact'],
            'is_staff': ['exact'],
        }
