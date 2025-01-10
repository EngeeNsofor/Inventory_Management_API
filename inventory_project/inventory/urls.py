from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InventoryItemViewSet, register_page, login_page, register, home, login_view, InventoryLogListView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'items', InventoryItemViewSet)

urlpatterns = [
    path('', home, name='home'),  # Root URL
    # API Endpoints (JWT)
    path('api/', include(router.urls)),
    path('api/register/', register),
    path('api/login/', login_view, name='login'),
    path('api/logs/', InventoryLogListView.as_view(), name='user-logs'),  # All logs for the user
    path('api/logs/<int:item_id>/', InventoryLogListView.as_view(), name='item-logs'),  # Logs for a specific item
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Token endpoint
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh endpoint
    # UI endpoints (HTML forms)
    path('register/', register_page, name='register_page'),
    path('login/', login_page, name='login_page'),
]
