    
from django.core.mail import send_mail
from django.conf import settings





from django.template.loader import render_to_string
from django.core.mail import EmailMessage

# def send_registration_mail(team_name,email,registration_number):
#         subject = 'Your Account Details'
#         message = f"""
#         Hello Team {team_name},

#         You have been apporved to be a team on our site

#         Please Click the link below to create a team
#         then you will get your login credentials to personalize your team members
#         and will receive a portal to manage your team

#         link: http://127.0.0.1:8000/create-team/{registration_number}/'

#         Please keep these details safe.

#         Regards,
#         Your Team
#         """
#         send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)
    

def send_otp_email(user_email, otp):
    subject = "Your OTP for Verification"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user_email]

    # Render the HTML template with context
    context = {"otp": otp}
    email_body = render_to_string("./emails/otp_email.html", context)

    # Send the email
    email = EmailMessage(subject, email_body, from_email, recipient_list)
    email.content_subtype = "html"  # Specify HTML content
    email.send()


def send_registration_email(user_email,name,username,password):
    subject = "Your Login Credentials  GPN Sports"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user_email]

    context = {'email':user_email,name:"name","username":username,"password":password}
    email_body = render_to_string("./emails/team_reg_email.html", context)

    email = EmailMessage(subject, email_body, from_email, recipient_list)
    email.content_subtype = "html"  # Specify HTML content
    email.send()


def send_registration_mail(team_name,email,registration_number):
        subject = "Registration Mail from GPN Sport"
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]

        context = {'before_registration':True,'email':email,'rno':registration_number,'team_name':team_name}
        email_body = render_to_string("./emails/team_reg_email.html", context)

        email = EmailMessage(subject, email_body, from_email, recipient_list)
        email.content_subtype = "html"  # Specify HTML content
        email.send()



def is_staff(user):
     return user.is_staff

def is_team(user):
    if not user.is_staff and user.groups.filter(name='TeamGroup').exists():
         return True
    return False
     