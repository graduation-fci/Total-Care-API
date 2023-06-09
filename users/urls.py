from rest_framework_nested import routers
from . import views



router = routers.DefaultRouter()
router.register('patients', views.PatientViewSet)
router.register('medications', views.MedicationProfileViewSet,basename="medications")
router.register('addresses', views.AddressViewSet,basename="addresses")
router.register('usersimages',views.ImageViewSet,basename="usersimages")
router.register('usersearchhistory', views.SearchHistoryViewSet, basename="usersearchhistory")

urlpatterns = router.urls