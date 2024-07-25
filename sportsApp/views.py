from django.shortcuts import render,get_object_or_404
from django.shortcuts import HttpResponse

from .models import PointTable,TieSheet,RecentEvents,LatestNews

# Create your views here.
def index(request):
    recent_events = RecentEvents.objects.all().order_by('-date')[:5]
    latest_news = LatestNews.objects.all()
    return render(request,'main.html',{'recent_events':recent_events,'latest_news':latest_news})


def leaderboard(request):
    point_table = PointTable.objects.all().order_by('-points')
    tie_sheet = TieSheet.objects.all().order_by('-match_date')
    return render(request,'./leaderboard/leaderboard.html',{'point_table':point_table,'tie_sheet':tie_sheet})


def events(request):
    recent_events = RecentEvents.objects.all().order_by('-date')
    return render(request,'./eventPage.html',{'recent_events':recent_events})


def latest_news_page(request, news_id):
    data = get_object_or_404(LatestNews, id=news_id)
    return render(request, './news/newsView.html', {'data': data})