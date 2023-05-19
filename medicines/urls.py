from django.urls import path
from rest_framework_nested import routers
from . import views


# URLConf

router = routers.DefaultRouter()
router.register('products', views.MedicineViewSet,  basename='products')
router.register('drugs', views.DrugViewSet)
router.register('categories', views.CategoryViewSet)
router.register('general_categories', views.GeneralCategoryViewSet)
router.register('images', views.ImageViewSet)
router.register('simple_meds', views.SimpleMedicineViewSet, basename='simple_meds')
router.register('interactions', views.InteractionsViewSet, basename='interactions')

# urlpatterns = [
#     path('medicine/products/bulk_create/', views.MedicineViewSet.as_view({'post': 'bulk_create'}), name='medicine-bulk-create'),
#     path('medicine/products/bulk_patch/<int:id>/', views.MedicineViewSet.as_view({'patch': 'bulk_patch'})),
#     path('medicine/products/bulk_delete/', views.MedicineViewSet.as_view({'delete': 'bulk_delete'}), name='medicine-bulk-delete'),
# ]

urlpatterns = router.urls
