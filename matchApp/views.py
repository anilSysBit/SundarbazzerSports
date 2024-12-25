
from django.shortcuts import render,get_object_or_404
from django.shortcuts import render,redirect
from django.core.exceptions import ValidationError
from django.http import HttpResponseBadRequest,JsonResponse
from django.views.decorators.http import require_POST
from django.db import IntegrityError
from .models import Match,Goal,Player,MatchTimeManager,MatchPauseResume
from sportsApp.models import Event
from django.contrib.auth.models import User
from django.conf import settings
from django.core.paginator import Paginator
from .forms import GoalForm,FoulForm,MatchTimeManagerForm,SubstitutionForm,MatchPauseResumeForm
from django.contrib import messages
from sportsApp import constants
from django.db.models import Count,Q
from utils.time_formatter import format_duration
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.utils.timezone import now


def match_list_view(request):
    
    matches = Match.objects.all()

    print(Match.objects.count())
    return render(request,'matches/all_match.html',{'matches':matches})


# Create your views here.
def match_view(request,match_id):
    match = get_object_or_404(Match,pk=match_id)
    event = get_object_or_404(Event,pk=match.event.id)

    match_datetime = datetime.combine(match.match_date,match.match_time)

    # time_manager = get_object_or_404(MatchTimeManager,match=match)
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
        'actual_time':'',
    }

    time_manager, created = MatchTimeManager.objects.get_or_create(match=match)
    timeManagerForm = MatchTimeManagerForm()
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
       'match_pause_status':False,
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

        form_data = request.POST.copy()
        match = form_data['match']

        _mtm = get_object_or_404(MatchTimeManager,match=match)

        if _mtm.match_ended:
            return JsonResponse({
                'success': False,
                'message': 'Cannot Add goal After match is ended',
            }, status=400)
        

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
        form_data = request.POST.copy()
        match = form_data['match']
        _mtm = get_object_or_404(MatchTimeManager,match=match)

        if _mtm.match_ended:
            return JsonResponse({
                'success': False,
                'message':'Cannot add goal after match is ended',
                'errors': 'Cannot Add goal After match is ended',
            }, status=400)

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
            match = get_object_or_404(Match,pk=pk)
            match_time_manager = get_object_or_404(MatchTimeManager,match=match)
            form = MatchTimeManagerForm(request.POST, instance=match_time_manager)
            
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


def get_pause_or_resumed(request,match_id):
    match = get_object_or_404(Match,pk=match_id)
    match_pause_resume = MatchPauseResume.objects.filter(match=match)
    match_time_manager = get_object_or_404(MatchTimeManager,match=match)
    data = {
        'match':match.id,
        'time_manager_initiation':False,
        'pause_resume_initiation':False,
        'is_ongoing':False,
        'recent_status':'resumed',
    }
    message = ''

    
    match_status = constants.MatchStatus
    if match.status == match_status.ONGOING:
        data['is_ongoing']  = True
        if match_time_manager :
            data['time_manager_initiation'] = True

            if match_time_manager.first_half_start_time and match_time_manager.second_half_start_time:
                data['is_before_half'] = False
            else:
                data['is_before_half'] =True


        if match_pause_resume.count() > 0:
            latest_pause_resume = match_pause_resume.latest('paused_at')

            print('latest pause resume',latest_pause_resume)

            if latest_pause_resume.paused_at and not latest_pause_resume.resumed_at:
                data['recent_status'] = 'paused'
                data['recent_resume_id'] = latest_pause_resume.id
            else:
                data['recent_status'] = 'resumed'

            data['pause_resume_initiation'] = True
    else:
        message="Match should be ongoing to get the detail."

    

    return JsonResponse({
        'success':True,
        'message':message,
        'data':data
    })
    

@csrf_exempt
def pause_match(request):
    if request.method == 'POST':
        post_data = request.POST.copy()  # Make a mutable copy of POST data
        match_time_manager = get_object_or_404(MatchTimeManager,match=post_data['match'])
        if match_time_manager.match_ended :
            return JsonResponse({
                'success': False,
                'message': 'Match Already Over Cannot Make Changes'
            },status=400)
        
        if not post_data.get('paused_at'):  # If paused_at is not provided
            post_data['paused_at'] = now()  # Set paused_at to current time
        
    
        form = MatchPauseResumeForm(post_data)
        
        if form.errors:  
            return JsonResponse({
                'success': False,
                'errors': form.errors
            }, status=400)  # <-- Return status 400 if form has errors

        if form.is_valid():
            match_pause_resume = form.save()
            return JsonResponse({
                'success': True,
                'message': 'Match paused successfully.',
                'data': {
                    'id': match_pause_resume.id,
                    'match': match_pause_resume.match.id,
                    'paused_at': match_pause_resume.paused_at,
                    'is_before_half': match_pause_resume.is_before_half,
                }
            })

    return JsonResponse({
        'success': False,
        'message': 'Only POST requests are allowed.'
    }, status=405)  # <-- 405 Method Not Allowed

@csrf_exempt
def resume_match(request, resume_id):
    if request.method == 'POST':
        match_pause_resume = get_object_or_404(MatchPauseResume, pk=resume_id)
        _mtm = get_object_or_404(MatchTimeManager,match=match_pause_resume.match)
        if _mtm.match_ended:
            return JsonResponse({
                'success': False,
                'message': 'Match Already Over Cannot Make Changes'
            },status=400)
        form = MatchPauseResumeForm(request.POST, instance=match_pause_resume)
        if match_pause_resume:
            match_pause_resume.resumed_at = now()
            match_pause_resume.save()

            return JsonResponse({
                'success':True,
                'message':'Successfully Resumed the match',
            },status=200)
        else:
            return JsonResponse({
                'success': False,
                'message':'Cannot Resume ! No Data Found for when it was paused'
            },status=400)
    return JsonResponse({
        'success': False,
        'message': 'Only POST requests are allowed.'
    },status=405)


def get_leaked_duration(match,match_time_manager,is_before_half=True):
    
    leaked_time = 0
    pause_running_time = False
    match_pause_resume = MatchPauseResume.objects.filter(match=match,is_before_half=is_before_half)
    resumed_data = match_pause_resume.exclude(resumed_at__isnull=True)
    if match_pause_resume.count() > 0:
        if resumed_data.count() > 0:
            for data in resumed_data:
                leaked_duration = data.resumed_at - data.paused_at
                
                leaked_time += leaked_duration.seconds

        latest_pivot = match_pause_resume.latest('created_at')
        print('latest pivot',latest_pivot)
        if latest_pivot.paused_at and latest_pivot.resumed_at is None:
            pause_running_time = True
        else:
            pause_running_time = False



    return {'leaked_time':leaked_time,'pause_running_time':pause_running_time}

@csrf_exempt
def get_match_time_api(request,match_id):
    
    if request.method == 'GET':

        match = get_object_or_404(Match,pk=match_id)
        match_time_manager = get_object_or_404(MatchTimeManager,match=match)
        event = get_object_or_404(Event,id=match.event.id)

        match_duration = event.match_duration
        half_time_duration = match_duration / 2


        if not match_time_manager.first_half_start_time:
                return JsonResponse({
                    'success':False,
                    'message':'Start First half to Calulate the time',
                    'start_status':'not_started',
                },status=400)
        first_half_start_time = match_time_manager.first_half_start_time.time().strftime('%H:%M %p')
        
             
        


        running_time = datetime.now() - match_time_manager.first_half_start_time

        if match_time_manager.is_half_time_over and match_time_manager.second_half_start_time:
            running_time = datetime.now() - match_time_manager.second_half_start_time

        pause_resume_overview = get_leaked_duration(match,match_time_manager,is_before_half= not match_time_manager.is_half_time_over)

        print('time',pause_resume_overview)
        leckage_time = pause_resume_overview['leaked_time']
        pause_running_time = pause_resume_overview['pause_running_time']
        
        # return
        data_running_time = running_time.seconds - leckage_time


        data_remaning_time = half_time_duration - running_time

        if data_running_time > (event.match_duration/2).seconds:

            data_running_time = (event.match_duration/2).seconds
            pause_running_time = True
        
        if match_time_manager.is_half_time_over and match_time_manager.second_half_start_time is None:
            pause_running_time = True
        




        if match_time_manager.match_ended:
            data_running_time = (match_time_manager.match_end_date_time - match_time_manager.second_half_start_time).seconds
            # print('data running time ',data_running_time.seconds)
            data = {
                'match':match.id,
                'time_manager':match_time_manager.id,
                'start_time':match_time_manager.start_time,
                'game_duration':format_duration(event.match_duration),
                'half_time_duration': format_duration(half_time_duration),
                'first_half_start_time':first_half_start_time,
                'second_half_start_time':match_time_manager.second_half_start_time,
                'running_time':data_running_time,
                'remaning_time':0,
                'leakage_time':0 if (not match_time_manager.second_half_start_time and match_time_manager.is_half_time_over) else leckage_time,
                'pause_running_time':True,
                'is_half_time_over':match_time_manager.is_half_time_over,
                'is_match_ended':match_time_manager.match_ended
            }
        else:
                    data = {
            'match':match.id,
            'time_manager':match_time_manager.id,
            'start_time':match_time_manager.start_time,
            'game_duration':format_duration(event.match_duration),
            'half_time_duration': format_duration(half_time_duration),
            'first_half_start_time':first_half_start_time,
            'second_half_start_time':match_time_manager.second_half_start_time,
            'running_time':data_running_time,
            'remaning_time':0 if match_time_manager.match_ended else format_duration(data_remaning_time),
            'leakage_time':0 if (not match_time_manager.second_half_start_time and match_time_manager.is_half_time_over) else leckage_time,
            'pause_running_time':pause_running_time,
            'is_half_time_over':match_time_manager.is_half_time_over,
            'is_match_ended':match_time_manager.match_ended
        }

        return JsonResponse({
            'success':True,
            'data':data,
            "message":"Successfully get the Data",
        })

        

    return JsonResponse({
        'success':False,
        # 'data':data,
        "message":"Invalid GET request",
    },status=405)


@csrf_exempt
def actual_start_match_api(request,match_id):

    type = int(request.GET.get('type'))

    print(type)

    if request.method == "POST":
        match = get_object_or_404(Match,pk=match_id)
        _mtm = get_object_or_404(MatchTimeManager,match=match) #match time manager


        if not _mtm.match_ended:
            if type == 0:
                if now() <= _mtm.start_time:
                    return JsonResponse({
                        'success':False,
                        'message':f"Cannot Start the Match Before the Start time ({_mtm.start_time}).Update start time to start match now."
                    },status=400)
                
                _mtm.first_half_start_time = now()
                _mtm.save()
                return JsonResponse({
                    'success':True,
                    "message":"Match First Half Started Successfully",
                })
            elif type == 2:
                if(_mtm.start_time and _mtm.first_half_start_time and _mtm.is_half_time_over):
                    _mtm.second_half_start_time = now()
                    _mtm.save()

                    return JsonResponse({
                        'success':True,
                        "message":"Match Second Half started Successfully",
                    })
                return JsonResponse({
                    'success':False,
                    'message':'Match doesn\'t have first half detail to start second half. Is half time over should be true.',
                },status=400)

            elif type == 1:
                if _mtm.first_half_start_time and not _mtm.is_half_time_over:
                    _mtm.is_half_time_over = True
                    _mtm.save()

                    return JsonResponse({
                        'success':True,
                        "message":"Match First Half Over Successfully",
                        })
                return JsonResponse({
                    'success':False,
                    'message':'Match already half time over. Reinitialize To change.',
                },status=400)

            elif type == 3:
                if (_mtm.is_half_time_over and not _mtm.match_ended and _mtm.first_half_start_time and _mtm.second_half_start_time):
                    match.status = constants.MatchStatus.COMPLETED
                    _mtm.match_end_date_time = datetime.now()
                    _mtm.match_ended = True
                    _mtm.save()
                    match.save()

                    return JsonResponse({
                        'success':True,
                        "message":"Match Ended Successfully",
                    })
                return JsonResponse({
                    'success':False,
                    'message':'Data is not correct on match to finish the match.',
                },status=400)
            
            else:
                return JsonResponse({
                    'success':False,
                    "message":"Invalid Query request",
                    'status':400
                },status=400)
        else:
            return JsonResponse({
                'success':False,
                'message':"This match already Ended. Cannot make changes further"
            },status=400)
        

    return JsonResponse({
        'success':False,
        "message":"Invalid POST request",
        'status':400
    })






# substitution form
def check_match_ended(match_id):
    _mtm = get_object_or_404(MatchTimeManager,match=match_id)
    print('going here',_mtm)
    if _mtm.match_ended:
        return True
    return False

def add_substitutiton_api(request):

    if request.method == 'POST':
        form = SubstitutionForm(request.POST)
        form_data = request.POST.copy()
        print(form_data)
        match_id = form_data['match']
        if check_match_ended(match_id):
            return JsonResponse({
                'success': False,
                'message':'Cannot Make Change after Game is Over',
            }, status=400)

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


    



