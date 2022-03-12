from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib import messages
from django.contrib.auth.models import User
from Portfolios.models import PortfolioUser




def homeView(request):

    return render(request, 'landing.html')   


def loginView(request):
  '''Form support for Login'''
  if request.method == "POST":
    email = request.POST.get('email', '')
    password = request.POST.get('password', '')

    authenticated = authenticate(username=email, password=password)

    # Valid username and password
    if authenticated is not None and authenticated.is_active:
      login(request, authenticated)
      return render(request, 'landing.html')
    # Incorrect username or password
    else:
      return render(request, 'registration/login.html', {'errors': ['Invalid Username and/or Password']})

  else:
    # Displacy Login Form
    return render(request, 'registration/login.html')






def logout_user(request):
  '''Logouts the currently signed in user and redirects to home page'''
  logout(request)
  return render(request, 'landing.html')

def signupView(request):
  '''Form support for User Registration Process'''
  if request.method == "POST":
    # Get POST params from request
    f_name = request.POST.get('first_name', '')
    l_name = request.POST.get('last_name', '')
    email = request.POST.get('email', '')
    password = request.POST.get('password', '')
    confirm_password = request.POST.get('password_confirmation', '')

    errors = []
    # Check if the user already exists
    try:
      User.objects.get(username=email)
      errors.append('A user by that username already exists')
    except User.DoesNotExist:
      pass

    # Input Field checks
    if len(password) < 3:
      errors.append('Enter a valid password that is more than 3 characters')
    if password != confirm_password:
      errors.append('Password and Confirm Password don\'t match')
    if len(errors) > 0:
      return render(request, 'registration/signup.html', {'errors' : errors})

    # Create a User and redirect to login
    user = User.objects.create_user(first_name=f_name, last_name=l_name, username=email, password=password)
    PortfolioUser.objects.create(user=user, first_name=f_name, last_name=l_name)
    return render(request, 'registration/login.html')
  else:
    # Display registration form
    return render(request, 'registration/signup.html')

def password_reset_request(request):
  if request.method == "POST":
    email_password_reset = request.POST.get('email_password_reset', '')
    associated_users = User.objects.filter(Q(email=email_password_reset))
    if associated_users.exists():
      for user in associated_users:
        subject = "Password Reset Requested"
        email_template_name = "password/password_reset_email.txt"
        c = {
        "email":user.email,
        'domain':'127.0.0.1:8000',
        'site_name': 'Sight',
        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
        "user": user,
        'token': default_token_generator.make_token(user),
        'protocol': 'http',
        }
        email = render_to_string(email_template_name, c)
        try:
          send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
        except BadHeaderError:
          return HttpResponse('Invalid header found.')
        messages.success(request, 'A message with reset password instructions has been sent to your inbox.')
        return redirect ("../login")
 
  return render(request=request, template_name='password/password_reset.html')


