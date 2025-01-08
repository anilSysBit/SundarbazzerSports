from django.shortcuts import render,get_object_or_404
from django.shortcuts import HttpResponse,render,redirect
from django.core.exceptions import ValidationError
from django.http import HttpResponseBadRequest,JsonResponse
from django.views.decorators.http import require_POST
from django.db import IntegrityError
from .models import Payment,Transaction,Event,EventTeam
from matchApp.models import Match
from django.contrib.auth.models import User
from django.views import View
import uuid
import hmac
import hashlib
import json
import base64
from django.conf import settings
from django.core.paginator import Paginator
from .forms import PlayerForm,EventForm,TeamForm,EventTeamForm,OTPRequestForm,OTPForm,PasswordResetForm
from matchApp.forms import MatchForm
from django.contrib import messages
from . import constants
from django.db.models import Count,Q
from .utils import send_otp_email

from .models import PointTable,TieSheet,RecentEvents,LatestNews,Team,TeamRequest,Coach,Player,OTP
import random
from django.contrib.auth import update_session_auth_hash


# auth


def login_view(request):
    return render(request,"./auth/login.html")


def send_otp_view(request):
    if request.method == 'POST':
        form = OTPRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)
            otp_code = random.randint(1000, 9999)
            OTP.objects.update_or_create(user=user, defaults={'otp': otp_code})
            
            request.session['email'] = email
            send_otp_email(email, otp_code)

            messages.success(request, "OTP sent to your email. Please check your inbox.")
            return redirect('verify_otp')
        else:
            # If form is not valid, the errors will automatically be attached to the form fields
            messages.error(request, "There was an error with your email. Please check and try again.")

    else:
        form = OTPRequestForm()

    return render(request, 'auth/send_otp.html', {'form': form})


def verify_otp(request):
    # Check if email exists in session
    email = request.session.get('email')

    if not email:
        messages.error(request, "Email session has expired or is missing. Please request an OTP again.")
        return redirect('send_otp')  # Redirect to OTP request page if email is not found in session

    if request.method == 'POST':
        form = OTPForm(request.POST)
        
        if form.is_valid():
            user_otp = form.cleaned_data.get('otp')

            print('user otp',user_otp)

            # Retrieve the user based on email from the session
            try:
                user = User.objects.get(email=email)
                otp_instance = OTP.objects.filter(user=user).first()

                if otp_instance and otp_instance.otp == user_otp and otp_instance.is_valid():
                    messages.success(request, "OTP verified successfully!")
                    request.session['otp'] = user_otp  # Save OTP to session for further use
                    return redirect('change_password')  # Redirect to change password page
                else:
                    messages.error(request, "Invalid or expired OTP.")
            except User.DoesNotExist:
                messages.error(request, "User not found.")
        else:
            messages.error(request, "Please enter a valid OTP.")
    else:
        form = OTPForm()

    return render(request, './auth/verify_otp.html', {'range':range(4),'form': form})

def change_password(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data.get('new_password')
            user = request.user
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)  # To keep the user logged in
            messages.success(request, "Password changed successfully!")
            return redirect('login')
    else:
        form = PasswordResetForm()

    return render(request, './auth/change_password.html', {'form': form})
"""
    Player  Views
"""


def player_data_api(request,player_id):
    player = get_object_or_404(Player,pk=player_id)

    playerData = {
        'id':player.id,
        'name':player.name,
        'designation':player.designation,
        'jersey_no':player.jersey_no,
        'team_name':player.team.name,
    }
    return JsonResponse(playerData)


def view_players(request,team_id):
    team = get_object_or_404(Team,id=team_id)
    players = Player.objects.filter(team=team)
    return render(request,'./teams/player_table.html',{'team':team,'players':players})


# creating player function
def create_player(request,team_id):
    team = get_object_or_404(Team,id=team_id)
    form = PlayerForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Player created successfully!")
            return redirect('team-players',team.id)
        else:
            return render(request,'./teams/create_player.html',{'team':team,'form':form},status=400)

            
    return render(request,'./teams/create_player.html',{'team':team,'form':form})


# updating player function
def update_player(request, player_id):
    player = get_object_or_404(Player, id=player_id)  # Fetch the player to update
    team = get_object_or_404(Team, id=player.team.id)
    form = PlayerForm(request.POST or None, request.FILES or None, instance=player)  # Pass the player instance to the form

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Player updated successfully!")
            return redirect('team-players', team.id)
        else:
            return render(request, './teams/create_player.html', {'team': team, 'form': form, 'player': player}, status=400)

    return render(request, './teams/create_player.html', {'team': team, 'form': form, 'player': player})


# function to delete the player
@require_POST
def delete_player(request,player_id):

    item = get_object_or_404(Player, pk=player_id)
    item.delete()
    messages.success(request,'Player Deleted Successfully')

    return JsonResponse({'message': 'Item deleted successfully', 'item_id': player_id}, status=200)
            


# changingthe player status
@require_POST
def change_player_status(request,player_id):
    item = get_object_or_404(Player, pk=player_id)
    item.is_active = not item.is_active  # Toggle the is_verified status
    messages.success(request,f"{'Activated' if item.is_active else 'Deactivated'} player {item.name}")
    item.save()  # Save the updated item


    return JsonResponse({'message': 'Team Verified Successfully', 'player_id': player_id}, status=200)


    
"""
        End of player views
"""









""" 
    Team Views
"""
def create_team_view(request):
    if request.method == 'POST':
        form = TeamForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Team created successfully.")
            return redirect('team')  # Adjust 'team_list' to the actual name of your redirect view
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = TeamForm()

    return render(request, 'teams/create_team.html', {'form': form})



def edit_team_view(request, team_id):
    team = get_object_or_404(Team, id=team_id)

    if request.method == 'POST':
        form = TeamForm(request.POST, request.FILES, instance=team)
        if form.is_valid():
            form.save()
            messages.success(request, "Team updated successfully.")
            return redirect('team')  # Adjust 'team_detail' to your team detail or list view name
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = TeamForm(instance=team)

    return render(request, 'teams/create_team.html', {'form': form, 'team': team})



def team_profile(request,team_id):
    
    team = get_object_or_404(Team,id=team_id)
    # coach = get_object_or_404(Coach,team_id=team_id)
    coach = None
      
    players = Player.objects.filter(team=team)
    return render(request,'./teams/teamProfile.html',{'team':team,'coach':coach,'basic_detail':True,})


class TeamView(View):
    def get(self, request, *args, **kwargs):
        teams_per_page = 5  # Define how many teams to display per page
        all_teams = Team.objects.all()  # Retrieve all teams

        # Set up paginator
        paginator = Paginator(all_teams, teams_per_page)
        page_number = request.GET.get('page', 1)  # Get the page number from the request, default to 1
        page_obj = paginator.get_page(page_number)  # Get the items for the current page

        # Calculate the starting index for the current page
        start_index = (page_obj.number - 1) * teams_per_page

        return render(request, './teams/teamPage.html', {
            'page_obj': page_obj,       # The page object with paginated items
            'start_index': start_index,  # Starting index for the current page
        })

    def post(self, request, *args,**kwargs):
        pk = kwargs.get('team_id')
        item = get_object_or_404(Team, pk=pk)
        item.delete()
        return JsonResponse({'message': 'Item deleted successfully', 'item_id': pk}, status=200)

@require_POST   
def changeTeamStatus(request, team_id):
    item = get_object_or_404(Team, pk=team_id)
    item.is_verified = not item.is_verified  # Toggle the is_verified status
    item.save()  # Save the updated item
    messages.success(request,f"{'Verified' if item.is_verified else 'Unverified'} team {item.name}")

    return JsonResponse({'message': 'Team Verified Successfully', 'item_id': team_id}, status=200)




"""

    End of Team View
"""





def esewa_payment(request):
    return render(request,'./payments/payment_summary.html')

from decimal import Decimal
def payment_request(request):
    if request.method == 'POST':
        # Example user ID and transaction type
        # Save payment information to the database
        payment_type = 'EVENT_REGISTRATION_PAYMENT'
        user_id = User.objects.get(pk=1)
        transaction_uuid = uuid.uuid4().hex


        amount = 100
        # amount = request.POST.get('total_amount')
        Payment.objects.create(
            transaction_type = payment_type,
            transaction_uuid = transaction_uuid,
            user = user_id,
            total_amount = amount,
        )
        
        # Extract total_amount from the POST request
        if amount is None:
            return HttpResponseBadRequest('Total amount not found in request.')

        # Print the total amount for debugging
        print('Total amount:', amount)


        tax_amount = 10
        total_amount = amount + tax_amount
        product_code = "EPAYTEST"
        success_url = "http://127.0.0.1:8000/payment/successfull"
        failure_url = "https://google.com"

        fields = {
            'amount': amount,
            'tax_amount': tax_amount,
            'total_amount': total_amount,
            'transaction_uuid': transaction_uuid,
            'product_code': product_code,
            'product_service_charge': 0,
            'product_delivery_charge': 0,
            'success_url': success_url,
            'failure_url': failure_url,
            'signed_field_names': 'total_amount,transaction_uuid,product_code',
        }

        secret_key = '8gBm/:&EnhH.1/q'
        signature = generate_signature(fields, secret_key)



        context = {
            'fields': fields,
            'signature': signature,
            'esewa_url': 'https://rc-epay.esewa.com.np/api/epay/main/v2/form'
        }

        return render(request, 'payments/esewa_payment.html', context)

    return HttpResponseBadRequest('Invalid request method.')



def generate_signature(fields, secret_key):
    signed_fields = fields['signed_field_names'].split(',')
    sorted_fields = {field: fields[field] for field in signed_fields}
    signature_data = ",".join(f"{k}={v}" for k, v in sorted_fields.items())
    signature = hmac.new(
        bytes(secret_key, 'utf-8'),
        bytes(signature_data, 'utf-8'),
        hashlib.sha256
    ).digest()
    return base64.b64encode(signature).decode()


def payment_success(request):
    pass


def esewa_response(request):
    if request.method == 'GET':
        # Extract the encoded response directly from the query string
        encoded_response = request.GET.get('data')

        if not encoded_response:
            return HttpResponseBadRequest('No response data found.')

        try:
            # Decode the base64-encoded string
            decoded_response = base64.b64decode(encoded_response).decode('utf-8')

            # Parse the JSON string to a Python dictionary
            response_data = json.loads(decoded_response)

            # Extract data
            transaction_code = response_data.get('transaction_code')
            status = response_data.get('status')
            total_amount = response_data.get('total_amount')
            transaction_uuid = response_data.get('transaction_uuid')
            product_code = response_data.get('product_code')
            signature = response_data.get('signature')

            # Find or create the payment instance
            try:
                payment = Payment.objects.get(transaction_uuid=transaction_uuid)
            except Payment.DoesNotExist:
                # Handle the case where the payment does not exist
                return HttpResponseBadRequest('Payment not found.')

            try:
                # Attempt to create a new transaction
                Transaction.objects.create(
                    status=status,
                    total_amount=total_amount,
                    transaction_uuid=transaction_uuid,
                    product_code=product_code,
                    ref_id=transaction_code,
                    payment=payment,
                    description=f"Transaction for {product_code}",
                )
            except IntegrityError:
                # If an IntegrityError occurs, redirect to the home page
                return redirect('home')  # Replace 'home' with your actual home page route name

            # Redirect to the /payment page
            return render(request, './payments/payment_successfull.html')

        except (base64.binascii.Error, json.JSONDecodeError) as e:
            return HttpResponseBadRequest(f'Invalid response data: {str(e)}')

    return HttpResponseBadRequest('Invalid request method.')



def join_now(request):
    return render(request, './auth/auth_options.html')






"""
    Match Views 
"""

def event_match_view(request,event_id):
    event = get_object_or_404(Event,pk=event_id)
    matches = Match.objects.filter(event = event)

    print(Match.objects.count())
    return render(request,'matches/event_match.html',{'event':event,'matches':matches})





def create_match_view(request,event_id):
    event = get_object_or_404(Event,pk=event_id)
    form = MatchForm(request.POST or None,event=event)

    print("Just going to the function")
    
    if request.method == 'POST':
        if form.is_valid():
            print('going validation')
            form.save()
            messages.success(request, "New Match created successfully!")
            return redirect('match')
        else:
            print('going on the error')
            return render(request,'matches/create_match.html',{'event':event,'form':form},status=400)
    return render(request,'matches/create_match.html',{'event':event,'form':form})

def edit_match_view(request, match_id):
    match = get_object_or_404(Match, pk=match_id)
    event = get_object_or_404(Event, pk=match.event.id)
    form = MatchForm(request.POST or None, instance=match, event=event)

    print("Just going to the edit function")
    
    if request.method == 'POST':
        if form.is_valid():
            print('going to validation')
            form.save()
            messages.success(request, "Match updated successfully!")
            return redirect('match')  # Adjust 'match' to your actual match list view or redirect destination
        else:
            print('error in form submission')
            return render(request, 'matches/create_match.html', {'event': event, 'form': form,'update':True}, status=400)

    return render(request, 'matches/create_match.html', {'event': event, 'form': form,'update':True,})



def delete_match_view(request,match_id):
    item = get_object_or_404(Match, pk=match_id)
    item.delete()
    messages.success(request,"Successfully Deleted the match")
    return JsonResponse({'message': 'Match deleted successfully', 'item_id': match_id}, status=200)

"""
    End of Match viewsets
"""



"""
Event Views


"""

def event_list_view(request):
    events = Event.objects.all()
    return render(request,"event/event_list.html",{'events':events})


def event_profile_view(request,event_id):
    event = get_object_or_404(Event,pk=event_id)
    event_teams = EventTeam.objects.filter(event=event)
    return render(request,"event/event_profile.html",{'event':event,'event_teams':event_teams,'show_description':True})



def create_event_view(request):
    
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('event')  # or any other page after saving
    else:
        form = EventForm()
    
    return render(request, 'event/create_event.html', {'form': form})


def edit_event_view(request, event_id):
    # Fetch the existing event or return 404 if not found
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()  # Save the updated event
            messages.success(request,"Event Updated successfully")
            return redirect('event')  # Redirect to the event list or any other page after saving
        else:
            messages.error(request,'Event Not Updated updated')
    else:
        form = EventForm(instance=event)  # Prepopulate form with the existing event data

    return render(request, 'event/create_event.html', {'form': form,'update':True})


"""
    End of Event View
"""




"""
    Team Event Registration

    
"""

def create_event_team(request,event_id):
    event = get_object_or_404(Event,pk=event_id)

    if request.method == 'POST':
        form = EventTeamForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request,f'Successfully Registered team to the {event.title}')
            return redirect('event-profile',event_id)
        else:
            messages.error(request,"Please Corrent the Error Below")
    else:
        form = EventTeamForm(event=event)
    return render(request,'event/create_event_registration.html',{'event':event,'form':form})


""" 
    End of Event Team
    
"""


