from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework import status

from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from notify.utils import validate_user_email
from notify.helpers import send_mail
from rest_framework.response import Response
from notify.models import CustomerView, EmailActivity, EmailsInfo, EmailsUnsubscribed

from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse

@api_view(['POST'])
def send_user_email(request):
    """
    Send mail to users with their content. Also mark if the mail was delivered. 
    general_template.html has links to register click, unsubscribe event. 
    It also has api for registering open event.
    """

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
    count = 0
    for user_mail in user_email_content:

        email_info = EmailsInfo(subject = subject, user_mail_id = user_mail['email_id'], user_name = user_mail['username'] )
        email_info.save()

        email_activity = EmailActivity()
        email_activity.save()

        customer_view = CustomerView(customer_email = email_info, customer_activity = email_activity)
        customer_view.save()
        camp_id = customer_view.campaign_id

        click_link = 'http://127.0.0.1:8000/notify/activity/click/'+ str(customer_view.campaign_id) + '/' + str(user_mail['email_id'])
        unsubscribe_link = 'http://127.0.0.1:8000/notify/unsubscribe/'+ str(customer_view.campaign_id) + '/' + str(user_mail['email_id'])
        open_link = 'http://127.0.0.1:8000/notify/activity/open/'+ str(customer_view.campaign_id) + '/' + str(user_mail['email_id'])

        parameter_dict = {
            'html_template_content_path' : html_template_content_path,
            'sender_mail' : sender_mail, 'subject' : subject,
            'mail_id' : [user_mail['email_id']], 'content' : user_mail['content'],
            'click_link' : click_link, 'open_link' : open_link, 'unsubscribe_link' : unsubscribe_link
        }

        val = send_mail(parameter_dict)
        count += val
        email_activity_obj = CustomerView.objects.get(campaign_id=camp_id).customer_activity
        email_activity_obj.email_delivered = val
        email_activity_obj.save()
    
    main_response = Response(data= "Count :- " + str(count) + " mails have been send successfully.", status=status.HTTP_200_OK)

    return main_response


@api_view(['GET'])
def register_click_activity(request, camp_id, mail_id):

    customer_activity_obj = CustomerView.objects.get(campaign_id = camp_id).customer_activity
    customer_activity_obj.email_clicked = True
    customer_activity_obj.save()

    html_send_mail_template_path = 'notify/click_mail_template.html'
    html_template_context = get_template(html_send_mail_template_path)
    html_template = html_template_context.render({})

    return HttpResponse(html_template)


@api_view(['GET'])
def register_open_activity(request, camp_id, mail_id):

    customer_activity_obj = CustomerView.objects.get(campaign_id = camp_id).customer_activity
    customer_activity_obj.email_opened = True
    customer_activity_obj.save()

    html_send_mail_template_path = 'notify/open_mail_template.html'
    html_template_context = get_template(html_send_mail_template_path)
    html_template = html_template_context.render({})

    return HttpResponse(html_template)

@api_view(['GET'])
def register_unsubscribe_activity(request, camp_id, mail_id):

    customer_activity_obj = CustomerView.objects.get(campaign_id = camp_id).customer_activity
    customer_activity_obj.email_unsubscribed = True
    customer_activity_obj.save()

    html_send_mail_template_path = 'notify/unsubscribe_mail_template.html'
    html_template_context = get_template(html_send_mail_template_path)
    html_template = html_template_context.render({})

    return HttpResponse(html_template)


@api_view(['GET'])
def customer_overview(request):

    customer_activity_obj = CustomerView.objects.all()
    
    customer_activity_obj.email_unsubscribed = True
    customer_activity_obj.save()

    email_unsubscribed = EmailsUnsubscribed.objects.get(mail=mail_id)
    email_unsubscribed.unsubscribed = True
    email_unsubscribed.save()

    main_response = Response(data="suceess register_unsubscribe_activity", status=status.HTTP_200_OK)

    return main_response