from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from sportsApp.view2 import EventView

urlpatterns = [
    path('',EventView.index , name='home'),
    path('leaderboard/',views.leaderboard,name='leaderboard'),
    path("events/",views.events, name='events'),
    path("news/<int:news_id>/",views.latest_news_page,name='news_detail'),


    # Team url admin panel
    path('create-team/', views.create_team, name='create-team'),
    path("teams/",views.TeamView.as_view(),name="team"),
    path("teams/<int:team_id>/",views.team_profile,name="team-profile"),
    path("teams/<int:team_id>/players/",views.view_players,name="team-players"),
    path("teams/<int:team_id>/create-player/",views.create_player,name="create-player"),
    path("team-delete/<int:team_id>/",views.TeamView.as_view(),name="delete_team"),
    path('change-team-status/<int:team_id>/',views.changeTeamStatus,name='change-team-status'),

    # player
    path("change-player-status/<int:player_id>/",views.change_player_status,name="change-player-status"),
    path("delete-player/<int:player_id>/",views.delete_player,name="delete-player"),
    path("update-player/<int:player_id>/",views.update_player,name='update-player'),



    # matches

    path('matches/',views.match_view,name='match'),
    path('create-match/',views.create_match_view,name='create-match'),
    # path("create-team/",views.submit_team_request,name='submit_team_request'),
    path("success_state/",views.success_state,name="success_state"),
    path('payment/',views.esewa_payment,name='payment'),
    path('payment/request/',views.payment_request,name='payment_request'),
    path('esewa/response/',views.esewa_response,name='esewa_response'),
    path("payment/successfull",views.esewa_response,name='payment_successfull'),
    path("join",views.join_now,name='join_now'),
    # for event
    # path("organizer/",EventView.index , name='organizer')

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)