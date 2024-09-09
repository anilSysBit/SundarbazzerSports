
from django.urls import path,include
from django.conf import settings
from rest_framework.routers import DefaultRouter
from .views import (
    TeamRequestViewSet,
    TeamViewSet,
    # EventViewSet,
    EventOrganizerViewSet,
    EventListView, 
    EventDetailView, 
    EventCreateView, 
    EventUpdateView, 
    EventDeleteView,
    UserProfileAPIView,
    TeamProfileAPIView
    )
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
    
)

router = DefaultRouter()
team_list = TeamViewSet.as_view({
    'post': 'custom_action'
})


router.register(r'team-requests',TeamRequestViewSet,basename='teamrequest')
router.register(r'teams',TeamViewSet,basename='teams')
# router.register(r'events',EventViewSet,basename='event')
router.register(r'event-organizer',EventOrganizerViewSet,basename='event_organizer')


urlpatterns = [
    path('',include(router.urls)),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('teams/create/<str:request_id>/',team_list,name='team-create-with-request-id'),
    path('events/', EventListView.as_view(), name='event-list'),
    path('events/<int:pk>/', EventDetailView.as_view(), name='event-detail'),
    path('events/create/', EventCreateView.as_view(), name='event-create'),
    path('events/<int:pk>/update/', EventUpdateView.as_view(), name='event-update'),
    path('events/<int:pk>/delete/', EventDeleteView.as_view(), name='event-delete'),
    path('profile/',UserProfileAPIView.as_view(),name='user-profile'),
    path('team/profile/',TeamProfileAPIView.as_view(),name='team-profile'),
]
