from django.shortcuts import render,get_object_or_404
from django.shortcuts import HttpResponse,render,redirect
from django.core.exceptions import ValidationError
from django.http import HttpResponseBadRequest
from django.db import IntegrityError
from .models import Payment,Transaction
from django.contrib.auth.models import User
import uuid
import hmac
import hashlib
import json
import base64
from django.conf import settings



from .models import PointTable,TieSheet,RecentEvents,LatestNews,Team,TeamRequest,Coach

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


def team_profile(request,team_id):
    
    team = get_object_or_404(Team,id=team_id)
    coach = get_object_or_404(Coach,team_id=team_id)
    players = [
        {'name': 'Player 1', 'position': 'goalkeeper', 'image': 'https://via.placeholder.com/100'},
        {'name': 'Player 2', 'position': 'right-back', 'image': 'https://via.placeholder.com/100'},
        {'name': 'Player 3', 'position': 'center-back-1', 'image': 'https://via.placeholder.com/100'},
        {'name': 'Player 4', 'position': 'center-back-2', 'image': 'https://via.placeholder.com/100'},
        {'name': 'Player 5', 'position': 'left-back', 'image': 'https://via.placeholder.com/100'},
        # {'name': 'Player 6', 'position': 'defensive-midfielder', 'image': 'https://via.placeholder.com/100'},
        {'name': 'Player 7', 'position': 'right-midfielder', 'image': 'https://via.placeholder.com/100'},
        {'name': 'Player 8', 'position': 'central-midfielder', 'image': 'https://via.placeholder.com/100'},
        {'name': 'Player 9', 'position': 'left-midfielder', 'image': 'https://via.placeholder.com/100'},
        {'name': 'Player 10', 'position': 'right-winger', 'image': 'https://via.placeholder.com/100'},
        {'name': 'Player 11', 'position': 'left-winger', 'image': 'https://via.placeholder.com/100'},
        {'name': 'Player 12', 'position': 'forward', 'image': 'https://via.placeholder.com/100'}
    ]
    return render(request,'./teams/teamProfile.html',{'team':team,'coach':coach,'players':players})


def create_team(request, res_num):
    if request.method == 'GET':
        try:
            team_request = get_object_or_404(TeamRequest, registration_number=res_num)
            return render(request, 'teams/create_team.html', {'res_data': team_request,'res_num':res_num})
        except ValidationError:
            return redirect("")
        
    if request.method == 'POST':
        name = request.POST.get("name")
        short_name = request.POST.get("short_name")
        total_players = request.POST.get('total_players')
        sports_genere = request.POST.get("sports_genere")
        email = request.POST.get("email")
        address = request.POST.get('address')
        logo = request.FILES.get('logo')
        banner = request.FILES.get('banner')
        gender = request.POST.get('gender')
        # registration_number = request.POST.get('res_num')


        print('email',email)
        errors = []
        try:
            # Save the data
            team_request = Team(
                name=name,
                total_players=int(total_players),
                sports_genere=sports_genere,
                email=email,
                address=address,
                short_name=short_name,
                logo=logo,
                banner = banner,
                gender = gender
            )
            team_request.full_clean()  # Validates the model instance
            team_request.save()

            # After creating the team, delete the team request
            team_request = get_object_or_404(TeamRequest, registration_number=res_num)
            team_request.delete()


            return redirect('success_state')  # Redirect to the success page

        except ValidationError as e:
            errors.extend(e.messages)  # Add model validation errors to the errors list
            return render(request, './teams/create_team.html', {'res_data':{
                'errors': errors,
                'name': name,
                'total_players': total_players,
                'sports_genere': sports_genere,
                'short_name':short_name,
                'email': email,
                'address': address,
                'banner':banner,
                'logo':logo,
                'registration_num':res_num,
                'gender':gender
            }})

    
    return render(request, './teams/create_team.html')




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