
from django.shortcuts import render,get_object_or_404
from django.shortcuts import render,redirect
from django.core.exceptions import ValidationError
from django.http import HttpResponseBadRequest,JsonResponse
from django.views.decorators.http import require_POST
from django.db import IntegrityError
from .models import Match,Goal,Player,MatchTimeManager
from sportsApp.models import Event
from django.contrib.auth.models import User
from django.conf import settings
from django.core.paginator import Paginator
from .forms import GoalForm,FoulForm,MatchTimeManagerForm,SubstitutionForm
from django.contrib import messages
from sportsApp import constants
from django.db.models import Count,Q
from utils.time_formatter import format_duration
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime


def match_list_view(request):
    
    matches = Match.objects.all()

    print(Match.objects.count())
    return render(request,'matches/all_match.html',{'matches':matches})


# Create your views here.
def match_view(request,match_id):
    match = get_object_or_404(Match,pk=match_id)
    event = get_object_or_404(Event,pk=match.event.id)

    match_datetime = datetime.combine(match.match_date,match.match_time)

    time_manager = get_object_or_404(MatchTimeManager,match=match)
    match_status = constants.MatchStatus

    if match.status == match_status.EXPIRED:
        is_match_open = False
    
    elif datetime.now() > match_datetime and match.status != match_status.EXPIRED:
        match.status = constants.MatchStatus.ONGOING
        match.save()
        is_match_open = False
    else:
        is_match_open = True

    is_match_open = True
    match_duration = format_duration(event.match_duration)
    half_time = event.match_duration / 2
    match_time = {
        'duration':match_duration,
        'half_time':format_duration(half_time),
        'is_match_open':is_match_open,
        'actual_time':datetime.combine(match.match_date,time_manager.start_time or match.match_time)
    }

    time_manager, created = MatchTimeManager.objects.get_or_create(match=match)
    timeManagerForm = MatchTimeManagerForm(instance=time_manager)
    players1 = Player.objects.filter(team=match.team1.team).order_by('-is_active')
    players2 = Player.objects.filter(team=match.team2.team).order_by('-is_active')

    details = {}
    if match.status == 'Running':
        details['match_status'] = 'Match is Running'
    elif match.status == 'Initiated':
        details['match_status'] = 'Match Has Not Started'
    
    return render(request,'matches/match_view.html',{'event':event,'match':match,'match_time':match_time,'time_form':timeManagerForm,'player1':players1,'player2':players2})


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



def get_match_time_data_api(request,match_id):
    match = get_object_or_404(Match,pk=match_id)
    event = get_object_or_404(Event,pk=match.event)

    data = {
        'match_date':match.match_date,
        'prev_match_time':match.match_time,
        'match_day':match.match_day,
        'match_duration':format_duration(event.match_duration),
        'match_start_time':match.time_manager.start_time
    }

    return JsonResponse({
        'success':True,
        'data':data,
        'message':"Data fetched Successfully",
        'status':200
    })


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


@csrf_exempt
def match_time_manager_view(request, pk=None):
    if request.method == 'POST':
        if pk:
            instance = get_object_or_404(MatchTimeManager, pk=pk)
            form = MatchTimeManagerForm(request.POST, instance=instance)
        else:
            form = MatchTimeManagerForm(request.POST)
        
        if form.is_valid():
            match_time_manager = form.save()
            new_time = form.cleaned_data['start_time']

            

            return JsonResponse({
                'success': True,
                'message': f'Match time manager updated successfully. New Time is {new_time}',
                'data': {
                }
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Invalid form data',
                'errors': form.errors
            }, status=400)
    
    return JsonResponse({'success': False, 'message': 'Invalid HTTP method'}, status=405)


def get_player_data(player):
    playerData = {
        'id':player.id,
        'name':player.name,
        'designation':player.designation,
        'jersey_no':player.jersey_no,
        'team_name':player.team.name,
    }

    return playerData

def get_player_for_substitution(request, pid1, pid2):
    player1 = get_object_or_404(Player, pk=pid1)
    player2 = get_object_or_404(Player, pk=pid2)

    if player1.team != player2.team:
        return JsonResponse({'error': 'Both Players should be of same teams.'}, status=400)

    if player1.is_active and player2.is_active:
        return JsonResponse({'error': 'Cannot SubstituteBoth players are currently playing.'}, status=400)

    if player1.is_active and not player2.is_active:
        player1_data = get_player_data(player1)
        player2_data = get_player_data(player2)
        return JsonResponse({'player1': player1_data, 'player2': player2_data}, status=200)

    return JsonResponse({'error': 'Player 1 is not playing.'}, status=400)



def format_iso_duration(iso_duration):
    formatted_duration = int(iso_duration.total_seconds())
    return format_duration

@csrf_exempt
def get_match_time_api(request,match_id):
    
    if request.method == 'GET':

        match = get_object_or_404(Match,pk=match_id)
        match_time_manager = get_object_or_404(MatchTimeManager,match=match)
        event = get_object_or_404(Event,id=match.event.id)

        match_duration = event.match_duration
        half_time_duration = match_duration / 2

        first_half_start_time = match_time_manager.first_half_start_time.time().strftime("%H:%M %p")

        # print('time',first_half_start_time)

        running_time = datetime.now() - match_time_manager.first_half_start_time

        

        data = {
            'start_time':match_time_manager.start_time,
            'game_duration':format_duration(event.match_duration),
            'half_time_duration': format_duration(half_time_duration),
            'first_half_start_time':first_half_start_time,
            'second_half_start_time':match_time_manager.second_half_start_time,
            'running_time':running_time.seconds,
        }
    return JsonResponse({
        'success':False,
        'data':data,
        "message":"Invalid GET request",
        'status':400
    })

@csrf_exempt
def actual_start_match_api(request,match_id):

    if request.method == "POST":

        match_time_manager = get_object_or_404(MatchTimeManager,match=match_id)

        current_time = datetime.now()
        match_time_manager.first_half_start_time = current_time

        match_time_manager.save()

        # print('check date time',datetime.now().time())

        return JsonResponse({
            'success':True,
            'message':f"Successfully started the match on ({current_time.strftime('%H:%M %p')}). This time will calcuate all the durations.",
            'status':200,
        })

    return JsonResponse({
        'success':False,
        "message":"Invalid POST request",
        'status':400
    })




# substitution form

def add_substitutiton_api(request):

    if request.method == 'POST':
        form = SubstitutionForm(request.POST)


        if form.is_valid():
            player_out = form.cleaned_data['player_out']
            player_in = form.cleaned_data['player_in']

            goal = form.save()
            # messages.success(request,f'Added goal of {goal.player.name}')
            return JsonResponse({
                'success': True,
                'message': f'Substituted player , {player_out.name}({player_out.jersey_no}) OUT {player_in.name} ({player_in.jersey_no})IN',
                
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






