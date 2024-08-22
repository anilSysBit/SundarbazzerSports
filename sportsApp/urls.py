from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.index,name='home'),
    path('leaderboard/',views.leaderboard,name='leaderboard'),
    path("events/",views.events, name='events'),
    path("news/<int:news_id>/",views.latest_news_page,name='news_detail'),
    path("teams/",views.teams,name="team"),
    path("teams/<int:team_id>",views.team_profile,name="team_profile"),
    path("submit_team_request/",views.submit_team_request,name='submit_team_request'),
    path("success_state/",views.success_state,name="success_state"),
    path('create-team/<uuid:res_num>/', views.create_team, name='create-team'),
    path('payment/',views.esewa_payment,name='payment')
]