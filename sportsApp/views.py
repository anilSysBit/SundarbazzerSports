from django.shortcuts import render
from django.shortcuts import HttpResponse

# Create your views here.
def index(request):
    return render(request,'main.html')


def leaderboard(request):
    return render(request,'./leaderboard/leaderboard.html')