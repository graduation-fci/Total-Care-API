
from django.urls import  re_path
from .views import CustomTokenObtainPairView 
from djoser.urls.jwt import urlpatterns as djoserpatterns
from django.urls import path
from rest_framework_nested import routers
from . import views
from django.urls import path, include
from .views import CustomUserViewSet

router = routers.DefaultRouter()


custompatterns= [
    
    re_path(r"^jwt/create/?", CustomTokenObtainPairView.as_view(), name="jwt-create"),  
]

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt'))
]

router.register(r'users', CustomUserViewSet)

urlpatterns += custompatterns + router.urls