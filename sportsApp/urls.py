from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.index,name='home'),
    path('leaderboard/',views.leaderboard,name='leaderboard'),
    path("events/",views.events, name='events'),
    path("news/<int:news_id>/",views.latest_news_page,name='news_detail')
]