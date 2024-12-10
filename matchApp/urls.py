from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
    
urlpatterns = [

    path('matches/',views.match_list_view,name='match'),

    path("<int:match_id>/",views.match_view,name='match-profile'),

    
    # game simulator
    path("substitution-players/<int:pid1>/<int:pid2>/",views.get_player_for_substitution,name='substitution-players'),
    path('add-goal/',views.add_goal_view,name='add-goal'),
    path('add-foul/',views.add_foul_view,name='add-foul'),
    path('add-substitution/',views.add_substitutiton_api,name='subsitution-api'),
    path('game-simulation/<int:match_id>/',views.match_simulator_view,name='match-simulate'),
    path('match-data-api/<int:match_id>/',views.match_data_api,name='match_data_api'),


    path('start-match/<int:match_id>/',views.actual_start_match_api,name='start-match-update-time'),


    # get match times api
    path('match-time-api/<int:match_id>/',views.get_match_time_api,name='match-time-api'),
    # adding match time scheduling
    path('match-schedule/<int:pk>/',views.match_time_manager_view,name='match-schedule')
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)