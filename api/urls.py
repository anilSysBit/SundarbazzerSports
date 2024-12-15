
from django.urls import path,include
from django.conf import settings
from rest_framework.routers import DefaultRouter
from .views import (
    TeamRequestViewSet,
    TeamViewSet,
    UserProfileAPIView,
    TeamProfileAPIView,
    EventProfileApiView,
    EventUserViewSet,
    OrganizerEventViewSet,
    )

from .serializers import match_serializers

from .serializers import team_serializers

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
# router.register(r'teams',TeamViewSet,basename='teams')
# router.register(r'events',EventViewSet,basename='event')


urlpatterns = [
    path('',include(router.urls)),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('teams/create/<str:request_id>/',team_list,name='team-create-with-request-id'),

    path('profile/',UserProfileAPIView.as_view(),name='user-profile'),

    path('events/',EventUserViewSet.as_view(),name='events'),

    path('team/profile/',TeamProfileAPIView.as_view(),name='team-profile'),

    path('organizer/profile/',EventProfileApiView.as_view(),name='organizer-profile'),

    path('organizer/create/',EventProfileApiView.as_view(),name='create-organizer'),

    path('organizer/events/',OrganizerEventViewSet.as_view(),name='organizer-events'),
    
    path('matches/',match_serializers.UserListMatchViewSet.as_view(),name='matches'),

    path(
        'match/create/<int:event_id>/',
        match_serializers.MatchViewSet.as_view(),
        name='create-match'
        ),

    # get players of the team

    path('players/<int:team_id>/',team_serializers.TeamPlayerViewSet.as_view(),name='get-team-players'),


    # teams
    path('teams/',team_serializers.TeamListViewSet.as_view(),name='team-list'),
]
