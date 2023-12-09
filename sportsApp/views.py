from django.shortcuts import render
from django.shortcuts import HttpResponse
from .models import PointTable,TieSheet,RecentEvents

# Create your views here.
def index(request):
    recent_events = RecentEvents.objects.all().order_by('-date')
    return render(request,'main.html',{'recent_events':recent_events})


def leaderboard(request):
    point_table = PointTable.objects.all().order_by('-points')
    tie_sheet = TieSheet.objects.all().order_by('-match_date')
    return render(request,'./leaderboard/leaderboard.html',{'point_table':point_table,'tie_sheet':tie_sheet})
