
from django.urls import  re_path
from .views import CustomTokenObtainPairView
from djoser.urls.jwt import urlpatterns as djoserpatterns
from django.urls import path
from rest_framework_nested import routers
from . import views


custompatterns= [
    
    re_path(r"^jwt/create/?", CustomTokenObtainPairView.as_view(), name="jwt-create"),   
]

router = routers.DefaultRouter()
router.register('patients', views.PatientViewSet)
router.register('medications', views.MedicationProfileViewSet)


urlpatterns = custompatterns + djoserpatterns + router.urls