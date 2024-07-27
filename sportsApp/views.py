from django.shortcuts import render,get_object_or_404
from django.shortcuts import HttpResponse,render,redirect
from django.core.exceptions import ValidationError

from .models import PointTable,TieSheet,RecentEvents,LatestNews,Team,TeamRequest

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


def teams(request):
    verified_teams = Team.objects.filter(is_verified=True)
    return render(request,'./teams/teamPage.html',{'teams':verified_teams})



# view for requesting the team

def submit_team_request(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        total_players = request.POST.get('total_players')
        sports_genere = request.POST.get('sports_genere')
        email = request.POST.get('email')
        address = request.POST.get('address')

        # Perform validation
        errors = []
        if not name:
            errors.append("Name is required.")
        if not total_players or not total_players.isdigit() or int(total_players) < 1:
            errors.append("Total players must be a positive integer.")
        if sports_genere not in dict(TeamRequest.SPORT_TYPES).keys():
            errors.append("Invalid sports genre.")
        if email and TeamRequest.objects.filter(email=email).exists():
            errors.append("Email must be unique.")
        
        if errors:
            return render(request, './teams/teamRequestForm.html', {
                'errors': errors,
                'name': name,
                'total_players': total_players,
                'sports_genere': sports_genere,
                'email': email,
                'address': address
            })

        try:
            # Save the data
            team_request = TeamRequest(
                name=name,
                total_players=int(total_players),
                sports_genere=sports_genere,
                email=email,
                address=address
            )
            team_request.full_clean()  # Validates the model instance
            team_request.save()
            return redirect('success_state')  # Redirect to the success page

        except ValidationError as e:
            errors.extend(e.messages)  # Add model validation errors to the errors list
            return render(request, './teams/teamRequestForm.html', {
                'errors': errors,
                'name': name,
                'total_players': total_players,
                'sports_genere': sports_genere,
                'email': email,
                'address': address
            })

    
    return render(request, './teams/teamRequestForm.html')

def success_state(request):
    return render(request,"./teams/successRequest.html")