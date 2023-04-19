from rest_framework_nested import routers
from . import views



router = routers.DefaultRouter()
router.register('patients', views.PatientViewSet)
router.register('medications', views.MedicationProfileViewSet,basename="medications")
router.register('addresses', views.AddressViewSet,basename="addresses")

urlpatterns = router.urls