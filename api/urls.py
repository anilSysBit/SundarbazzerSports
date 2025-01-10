
from django.urls import path,include
from django.conf import settings
from rest_framework.routers import DefaultRouter
from .views import (
    TeamRequestViewSet,
    TeamViewSet,
    UserProfileAPIView,
    TeamProfileAPIView,
    EventUserViewSet,
    )

from ._serializers import match_serializers

from ._serializers import team_serializers

from ._serializers import event_serializers

from ._serializers import user_serializers

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
    
)

router = DefaultRouter()
team_list = TeamViewSet.as_view({
    'post': 'custom_action'
})


# router.register(r'teams',TeamViewSet,basename='teams')
# router.register(r'events',EventViewSet,basename='event')


urlpatterns = [
    path('',include(router.urls)),

    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    path('team-requests/',TeamRequestViewSet.as_view(),name='team-requests'),

    path('verify-login/', user_serializers.VerifyLoginView.as_view(), name='api_verify_login'),
    # otp url validation
    path('send-otp/', user_serializers.SendOTPView.as_view(), name='api_send_otp'),
    path('verify-otp/', user_serializers.VerifyOTPView.as_view(), name='api_verify_otp'),
    path('change-password/', user_serializers.ChangePasswordView.as_view(), name='api_change_password'),

    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('teams/create/<str:request_id>/',team_list,name='team-create-with-request-id'),

    path('profile/',UserProfileAPIView.as_view(),name='user-profile'),

    path('events/',EventUserViewSet.as_view(),name='events'),

    path('event/<int:pk>/',event_serializers.EventDetailView.as_view(),name='user-event-view'),

    # path('team/profile/',TeamProfileAPIView.as_view(),name='team-profile'),

    path('matches/',match_serializers.UserListMatchViewSet.as_view(),name='matches'),

    path('match/<int:pk>/',match_serializers.MatchSingleViewSet.as_view(),name='match-view'),
    path('match/<int:match_id>/players/<int:team_id>/', match_serializers.MatchTeamPlayersView.as_view(), name='match-team-players'),
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
