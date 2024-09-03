
from django.urls import path,include
from django.conf import settings
from rest_framework.routers import DefaultRouter
from .views import TeamRequestViewSet,TeamViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

router = DefaultRouter()

router.register(r'team-requests',TeamRequestViewSet,basename='teamrequest')
router.register(r'teams',TeamViewSet,basename='teams')

urlpatterns = [
    path('',include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
