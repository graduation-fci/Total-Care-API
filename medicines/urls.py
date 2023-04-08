from django.urls import path
from rest_framework_nested import routers
from . import views


# URLConf

router = routers.DefaultRouter()
router.register('products', views.MedicineViewSet)
router.register('drugs', views.DrugViewSet)
router.register('interactions', views.InteractionsViewSet, basename='interactions')

urlpatterns = router.urls
