#In order to access Django app DB with standalone python script this section must be included 
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Sight.settings")
django.setup()

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from Portfolios.models import PortfolioUser, StockPortfolio
from Dashboards.models import Notifications


alert_status = Notifications.objects.filter(status='On')

for user in alert_status:
    get_portfoliouser_id = PortfolioUser.objects.get(id=user.user_id)
    get_user_email = User.objects.get(id=get_portfoliouser_id.user_id)
    get_user_stocks = StockPortfolio.objects.filter(user=get_portfoliouser_id)
    for stocks in get_user_stocks:
        symbol = stocks.symbol
        price = stocks.price
        change = stocks.change
        signal = stocks.signal

    subject = "New notifications regarding your stocks."
    email_template_name = "alert_email.txt"
    c={
    "email":get_user_email,
    'symbol': symbol,
    'price': price,
    'change': change,
    'signal': signal,
    'site_name': 'Sight Stock App',
    }
    email = render_to_string(email_template_name, c)

    send_mail(subject, email, 'sightstockapp@outlook.com', [get_user_email], fail_silently=False)





