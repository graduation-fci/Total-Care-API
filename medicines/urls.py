from django.urls import path
from rest_framework_nested import routers
from . import views


# URLConf

router = routers.DefaultRouter()
router.register('products', views.MedicineViewSet)
router.register('drugs', views.DrugViewSet)


urlpatterns = router.urls