from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from sportsApp.view2 import EventView

urlpatterns = [
    path('',EventView.index , name='home'),
    path('leaderboard/',views.leaderboard,name='leaderboard'),
    # path("events/",views.events, name='events'),
    path("news/<int:news_id>/",views.latest_news_page,name='news_detail'),


    # Team url admin panel
path('create-team/', views.create_team_view, name='create-team'),
    path("teams/",views.TeamView.as_view(),name="team"),
    path("teams/<int:team_id>/",views.team_profile,name="team-profile"),
    path("teams/<int:team_id>/players/",views.view_players,name="team-players"),
    path("teams/<int:team_id>/create-player/",views.create_player,name="create-player"),
    path("team-delete/<int:team_id>/",views.TeamView.as_view(),name="delete_team"),
    path('change-team-status/<int:team_id>/',views.changeTeamStatus,name='change-team-status'),
    path('edit-team/<int:team_id>/',views.edit_team_view,name='edit-team'),

    # player
    path("change-player-status/<int:player_id>/",views.change_player_status,name="change-player-status"),
    path("delete-player/<int:player_id>/",views.delete_player,name="delete-player"),
    path("update-player/<int:player_id>/",views.update_player,name='update-player'),



    # matches

    path('matches/',views.match_list_view,name='match'),
    path('delete-match/<int:match_id>/',views.delete_match_view,name='delete-match'),

    # events

    path('events/',views.event_list_view,name='event'),
    path('event/<int:event_id>/',views.event_profile_view,name='event-profile'),
    path('event/<int:event_id>/matches/',views.match_view,name='event-matches'),
    path('edit-match/<int:match_id>/',views.edit_match_view,name='edit-match-admin'),
    path('event/<int:event_id>/create-match/',views.create_match_view,name='create-match-admin'),
    path('create-event/',views.create_event_view,name='create-event'),
    path('edit-event/<int:event_id>/',views.edit_event_view,name='edit-event'),
    path('register-team-event/<int:event_id>/',views.create_event_team,name='register-team-event'),
    
    # Matches

    path("match/<int:match_id>/",views.match_view,name='match-profile'),
    # path("create-team/",views.submit_team_request,name='submit_team_request'),
    path("success_state/",views.success_state,name="success_state"),
    path('payment/',views.esewa_payment,name='payment'),
    path('payment/request/',views.payment_request,name='payment_request'),
    path('esewa/response/',views.esewa_response,name='esewa_response'),
    path("payment/successfull",views.esewa_response,name='payment_successfull'),
    path("join",views.join_now,name='join_now'),
    # for event
    # path("organizer/",EventView.index , name='organizer')


    # game simulator

    path('game-simulation/<int:match_id>/',views.match_simulator_view,name='match-simulate'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)