from django.shortcuts import render,redirect,get_object_or_404
from sportsApp.forms import TeamForm
from sportsApp.models import TeamRequest
from django.http import HttpResponseNotFound
from django.contrib import messages
from sportsApp.utils import send_registration_email
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User,Group
from .models import Team,Player
from sportsApp.models import Event
from sportsApp.constants import EventStatus
from django.db.models import Q
# Create your views here.


def register_team(request,res_id):
    if not res_id:
        # Return a 404 response if no `res_id` is provided
        return HttpResponseNotFound("Registration ID not found.")
    
    team_request = get_object_or_404(TeamRequest,registration_number=res_id)

    if request.method == 'POST':
        if not team_request:
            return HttpResponseNotFound("This Page Doesn't Exist")

        form = TeamForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data['email']
            random_password = get_random_string(length=8)  # You can adjust the length as needed
            # email_prefix = email.split('@')[0].replace('.', '')

            # new_username = email_prefix
            # counter = 1

            # print('new username',email_prefix)

            # while User.objects.filter(username=new_username).exists():
            #     new_username = f"{email_prefix}{counter}"
            #     counter += 1

            new_user = User.objects.create_user(
                username=email,
                email=email,
                password=random_password
            )
            team_group, created = Group.objects.get_or_create(name="TeamGroup")
            new_user.groups.add(team_group)

            team = form.save(commit=False)
            team.user = new_user
            team.save()
            team_request.delete()

            send_registration_email(email,team.name,email,random_password)
            messages.success(request, "Team created successfully.")
            return redirect('team_registration_success')  # Adjust 'team_list' to the actual name of your redirect view
        else:
            messages.error(request, "Please correct the errors below.")

    team_request = get_object_or_404(TeamRequest,registration_number=res_id)
    default_values = {
        'name':team_request.name,
        'phone':team_request.phone,
        'email':team_request.email,
        'short_name':team_request.short_name,
        'address':team_request.address,
    }
    if team_request:
        form = TeamForm(initial = default_values)
        return render(request, './temp_team/team_registration.html', {'form': form})

def team_success_view(request):
    message = "A mail is sent to your gmail including with login credentials. You can login to our site with that credentials.\nThank your for regestering"
    return render(request,'./temp_team/success.html',{'header':"Successfully Registered Your Team",'message':message})



def edit_team_profile(request):
    user = request.user
    
    team = get_object_or_404(Team, user=user)

    if request.method == 'POST':
        form = TeamForm(request.POST, request.FILES, instance=team)
        if form.is_valid():
            form.save()
            messages.success(request, "Team updated successfully.")
            return redirect('team_profile')  # Adjust 'team_detail' to your team detail or list view name
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = TeamForm(instance=team)

    return render(request, 't_profile/profile.html', {'form': form, 'team': team})



def team_dashboard(request):
    user = request.user
    team = get_object_or_404(Team,user=user)
    # coach = get_object_or_404(Coach,team_id=team_id)
    coach = None
      
    # players = Player.objects.filter(team=team)
    return render(request,'./teams/teamProfile.html',{'team':team,'coach':coach,'basic_detail':True,})


def team_players(request):
    user = request.user
    team = get_object_or_404(Team,user=user)
    players = Player.objects.filter(team=team)
    return render(request,'./players/team_player_list.html',{'team':team,'players':players})


def team_ongoing_events_view(request):
    events = Event.objects.filter(Q(status=EventStatus.INITIATED ) | Q(status=EventStatus.REGISTRATION))

    return render(request,"event/event_list.html",{'events':events})

def team_jersey_view(request):
    user = request.user
    team = get_object_or_404(Team,user = user)

    return render(request,'jersey/team_jersey_page.html',{'team':team})