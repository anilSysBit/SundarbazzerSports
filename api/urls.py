
from django.urls import path,include
from django.conf import settings
from rest_framework.routers import DefaultRouter
from .views import TeamRequestViewSet,TeamViewSet

router = DefaultRouter()

router.register(r'team-requests',TeamRequestViewSet)
router.register(r'teams',TeamViewSet)

urlpatterns = [
    path('',include(router.urls))
]
