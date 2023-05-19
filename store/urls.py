from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()

router.register('carts', views.CartViewSet)
router.register('wishlists', views.WishListViewSet)
router.register('orders', views.OrderViewSet, basename='orders')
carts_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
carts_router.register('items', views.CartItemViewSet, basename='cart-items')

wishlists_router = routers.NestedDefaultRouter(router, 'wishlists', lookup='wishlist')
wishlists_router.register('items', views.WishListItemViewSet, basename='wishlistitems')

urlpatterns = router.urls + carts_router.urls