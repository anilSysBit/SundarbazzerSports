
from django.shortcuts import render,get_object_or_404
from django.shortcuts import HttpResponse,render,redirect
from django.core.exceptions import ValidationError
from django.http import HttpResponseBadRequest,JsonResponse
from django.views.decorators.http import require_POST
from django.db import IntegrityError
from .models import Match,Goal,Player
from sportsApp.models import Event
from django.contrib.auth.models import User
from django.conf import settings
from django.core.paginator import Paginator
from .forms import GoalForm,FoulForm
from django.contrib import messages
from sportsApp import constants
from django.db.models import Count,Q



def match_list_view(request):
    
    matches = Match.objects.all()

    print(Match.objects.count())
    return render(request,'matches/all_match.html',{'matches':matches})

# Create your views here.
def match_view(request,match_id):
    match = get_object_or_404(Match,pk=match_id)
    event = get_object_or_404(Event,pk=match.event.id)
    players1 = Player.objects.filter(team=match.team1.team).order_by('-is_active')
    players2 = Player.objects.filter(team=match.team2.team).order_by('-is_active')

    details = {}
    if match.status == 'Running':
        details['match_status'] = 'Match is Running'
    elif match.status == 'Initiated':
        details['match_status'] = 'Match Has Not Started'
    
    return render(request,'matches/match_view.html',{'event':event,'match':match,'player1':players1,'player2':players2})


# Match Simulator

"""Running the match Page"""

def match_simulator_view(request,match_id):
    match = get_object_or_404(Match,pk=match_id)
    event = get_object_or_404(Event,pk=match.event.id)


    players1 = Player.objects.filter(team=match.team1.team, is_active=True).annotate(
            goal_count=Count('goals', filter=Q(goals__match=match)),
            foul_count=Count('fouls', filter=Q(fouls__match=match))
        )
    players2 = Player.objects.filter(team=match.team2.team, is_active=True).annotate(
        goal_count=Count('goals', filter=Q(goals__match=match)),
        foul_count=Count('fouls', filter=Q(fouls__match=match))
    )
    # Extra players for team 1 and 2
    extra_players1 = Player.objects.filter(team=match.team1.team, is_active=False).annotate(
        goal_count=Count('goals', filter=Q(goals__match=match)),
        foul_count=Count('fouls', filter=Q(fouls__match=match))
    )
    extra_players2 = Player.objects.filter(team=match.team2.team, is_active=False).annotate(
        goal_count=Count('goals', filter=Q(goals__match=match)),
        foul_count=Count('fouls', filter=Q(fouls__match=match))
    )

    # Counts
    players1_count = players1.count()
    players2_count = players2.count()
    extra_players1_count = extra_players1.count()
    extra_players2_count = extra_players2.count()



        # Total goals for team 1 and team 2
    team1_total_goals = Goal.objects.filter(player__team=match.team1.team, match=match).count()
    team2_total_goals = Goal.objects.filter(player__team=match.team2.team, match=match).count()


    # Total players for each team
    total_players_team1 = Player.objects.filter(team=match.team1.team).count()
    total_players_team2 = Player.objects.filter(team=match.team2.team).count()

    count = {
        'team1':{
            'total':total_players_team1,
            'active':players1_count,
            'extra':extra_players1_count,
            'total_goals': team1_total_goals,
        },
            'team2':{
            'total':total_players_team2,
            'active':players2_count,
            'extra':extra_players2_count,
            'total_goals': team2_total_goals,
        }
    }


    context = {
       'match':match,
       'event':event,
       'count':count,
       'foul':FoulForm(instance=match),
       'alerts':game_stimulation_alerts(),
       'goal_type_choices':constants.GOAL_TYPE.choices,
       'player1':{'active_players':players1,'extra_players':extra_players1},
       'player2':{'active_players':players2,'extra_players':extra_players2},

    }

    return render(request,'game/match_simulator.html',context=context)


def match_data_api(request, match_id):
    match = get_object_or_404(Match, pk=match_id)
    
    # Fetching only goal count and foul count for active players for both teams
    team1_active_players = Player.objects.filter(team=match.team1.team, is_active=True).annotate(
        goal_count=Count('goals', filter=Q(goals__match=match)),
        foul_count=Count('fouls', filter=Q(fouls__match=match))
    )
    
    team2_active_players = Player.objects.filter(team=match.team2.team, is_active=True).annotate(
        goal_count=Count('goals', filter=Q(goals__match=match)),
        foul_count=Count('fouls', filter=Q(fouls__match=match))
    )

    # Summing up total goals for each team (you can update this data if needed)
    team1_total_goals = sum(player.goal_count for player in team1_active_players)
    team2_total_goals = sum(player.goal_count for player in team2_active_players)

    # Prepare data to be sent in the response
    data = {
        'team1': {
            'total_goals': team1_total_goals,
            'active_players': list(team1_active_players.values(
                'id', 'goal_count', 'foul_count'
            )),
        },
        'team2': {
            'total_goals': team2_total_goals,
            'active_players': list(team2_active_players.values(
                'id', 'goal_count', 'foul_count'
            )),
        },
    }
    
    return JsonResponse(data)

    

def add_goal_view(request):
    if request.method == 'POST':
        form = GoalForm(request.POST)


        if form.is_valid():
            player = form.cleaned_data['player']
            if not player.is_active:
                return JsonResponse({
                    'success': False,
                    'message': f'Error: {player.name} is not active. Cannot add goal of extra players',
                }, status=400)
                
            goal = form.save()
            # messages.success(request,f'Added goal of {goal.player.name}')
            return JsonResponse({
                'success': True,
                'message': f'Added goal of {goal.player.name}',
                
            }, status=201)
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors,
            }, status=400)
    else:
        return JsonResponse({
            'success': False,
            'message': 'Invalid request method. Use POST.',
        }, status=405)
    
def add_foul_view(request):
    if request.method == 'POST':
        form = FoulForm(request.POST)


        if form.is_valid():
            player = form.cleaned_data['player']
            if not player.is_active:
                return JsonResponse({
                    'success': False,
                    'message': f'Error: {player.name} is not active. Cannot add Foul of extra players',
                }, status=400)
                
            goal = form.save()
            # messages.success(request,f'Added goal of {goal.player.name}')
            return JsonResponse({
                'success': True,
                'message': f'Added foul of {goal.player.name}',
                
            }, status=201)
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors,
            }, status=400)
    else:
        return JsonResponse({
            'success': False,
            'message': 'Invalid request method. Use POST.',
        }, status=405)
    


def game_stimulation_alerts():
     alerts = [
        {"title": "Permission 1", "message": "Allow access to camera?", "button_text": "Allow", "handle_action": "handleCameraPermission()"},
        {"title": "Permission 2", "message": "Enable notifications?", "button_text": "Enable", "handle_action": "handleNotificationPermission()"},
        # Add more alerts as needed
    ]
     
     return alerts