#In order to access Django app DB with standalone python script this section must be included 
import sys, os, django
#sys.path.append("/Users/17874/Projects\Capstone_Sight") #here store is root folder(means parent)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Sight.settings")
django.setup()

from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User
from Portfolios.models import PortfolioUser, StockPortfolio
from Dashboards.models import Notifications




alert_status = Notifications.objects.filter(status='On')
for user in alert_status:
    get_portfoliouser_id = PortfolioUser.objects.get(id=user.user_id)
    get_user_email = User.objects.get(id=get_portfoliouser_id.user_id)


subject = "Your stocks have changed."
email_template_name = "alert_email.txt"
c={
"email":get_user_email.username,
'domain':'sightstockapp.azurewebsites.net',
'site_name': 'Sight Stock App',
'protocol': 'https',
}
email = render_to_string(email_template_name, c)

send_mail(subject, email, 'sightstockapp@outlook.com', [get_user_email.username], fail_silently=False)



# def send_alert():

#     alert_status = Notifications.objects.filter(status='On')
#     get_portfoliouser_id = PortfolioUser.objects.get(id=alert_status.user)
#     get_user_email = User.objects.get(id=get_portfoliouser_id.user)
#     user_email = get_user_email.username
#     get_alerts = StockPortfolio.objects.filter(user=get_portfoliouser_id.user)

#     subject = "Your notifications for today"
#     email_template_name = "alert_email.txt"
#     c={
#     'symbol':get_alerts.symbol,
#     'change':get_alerts.change,
#     'price':get_alerts.price,
#     'signal':get_alerts.signal,
#     }
#     email = render_to_string(email_template_name, c)
#     try:
#         send_mail(subject, email, 'sightstockapp@outlook.com', [user_email], fail_silently=False)
#     except BadHeaderError:

#         return HttpResponse('Invalid header found.')



