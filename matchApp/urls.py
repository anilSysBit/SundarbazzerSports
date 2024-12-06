from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('matches/',views.match_list_view,name='match'),

    path("<int:match_id>/",views.match_view,name='match-profile'),

    # game simulator

    path('add-goal/',views.add_goal_view,name='add-goal'),
    path('add-foul/',views.add_foul_view,name='add-foul'),
    path('game-simulation/<int:match_id>/',views.match_simulator_view,name='match-simulate'),
    path('match-data-api/<int:match_id>/',views.match_data_api,name='match_data_api'),


    # adding match time scheduling
    path('match-schedule/<int:pk>/',views.match_time_manager_view,name='match-schedule')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)