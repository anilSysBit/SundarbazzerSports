
from django.urls import path,include
from django.conf import settings
from rest_framework.routers import DefaultRouter
from .views import TeamRequestViewSet,TeamViewSet

router = DefaultRouter()

router.register(r'team-requests',TeamRequestViewSet,basename='teamrequest')
router.register(r'teams',TeamViewSet,basename='teams')

urlpatterns = [
    path('',include(router.urls))
]
