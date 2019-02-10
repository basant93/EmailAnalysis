from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework import status

from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from notify.utils import validate_user_email
from notify.helpers import send_mail
from rest_framework.response import Response
from notify.models import CustomerView, EmailActivity, EmailsInfo

@api_view(['POST'])
def send_user_email(request):

    data = JSONParser().parse(request)
    sender_mail = data['sender_mail']
    subject = data['subject'],


    html_template_content_path = 'notify/general_template.html'

    user_email_content = []

    for user_mail in data['user_emails']:
        mail = user_mail['email_id']

        if(validate_user_email(mail) ):
            user_email_content.append(user_mail)
    
    print(user_email_content)

    for user_mail in user_email_content:

        email_activity = EmailActivity()
        email_activity.save()

        email_info = EmailsInfo(subject = subject, user_mail_id = user_mail['email_id'], user_name = user_mail['username'] )
        email_info.save()

        customer_view = CustomerView(customer_email = email_info, customer_activity = email_activity)
        customer_view.save()


        click_link = 'http://127.0.0.1:8000/notify/activity/click/'+ str(customer_view.campaign_id) + '/' + str(user_mail['email_id'])
        unsubscribe_link = 'http://127.0.0.1:8000/notify/unsubscribe/'+ str(customer_view.campaign_id) + '/' + str(user_mail['email_id'])
        open_link = 'http://127.0.0.1:8000/notify/activity/open/'+ str(customer_view.campaign_id) + '/' + str(user_mail['email_id'])
        parameter_dict = {
            'html_template_content_path' : html_template_content_path,
            'sender_mail' : sender_mail, 'subject' : subject,
            'mail_id' : [user_mail['email_id']], 'content' : user_mail['content'],
            'click_link' : click_link, 'open_link' : open_link, 'unsubscribe_link' : unsubscribe_link
        }

        send_mail(parameter_dict)

    main_response = Response(data="suceess", status=status.HTTP_200_OK)

    return main_response








