from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework import status

from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from notify.helpers import send_mail, valid_email_response
from rest_framework.response import Response

from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse

from notify.models import CustomerView, EmailActivity, EmailsInfo, EmailsUnsubscribed, Category
from notify.view_models import CustomerOverview, CustomerOverviewResponse, MailPerformanceResponse
from notify.serializer_view_models import CustomerOverViewMainSerializer, CustomerMailPerformaceMainSerializer
from django.db.models import Q


@api_view(['POST'])
def send_user_email(request):
    """
    Send mail to users with their content. Also mark if the mail was delivered. 
    general_template.html has links to register click, unsubscribe event. 
    It also has api for registering open event.
    """

    data = JSONParser().parse(request)
    campaign_subject = data['campaign_subject']
    campaign_description = data['campaign_description']
    campaign_category_obj = Category.objects.get(category = data['category'])
    customer_view = CustomerView(campaign_subject = campaign_subject, campaign_description = campaign_description, \
    campaign_category = campaign_category_obj)
    customer_view.save()

    camp_id = customer_view.campaign_id

    html_template_content_path = 'notify/general_template.html'
    user_email_content = valid_email_response(data['user_emails'])
    print(user_email_content)
    count = 0
    total_mails = 0

    for user_mail in user_email_content:

        email_activity_obj = EmailActivity()
        email_activity_obj.save()

        email_info = EmailsInfo(subject = user_mail['subject'], user_mail_id = user_mail['email_id'], user_name = user_mail['username'], \
            customer = customer_view, email_activity = email_activity_obj )
        email_info.save()

        click_link = 'http://127.0.0.1:8000/notify/activity/click/'+ str(email_info.id)
        unsubscribe_link = 'http://127.0.0.1:8000/notify/unsubscribe/'+ str(camp_id) + "/" + str(email_info.id)
        open_link = 'http://127.0.0.1:8000/notify/activity/open/'+ str(email_info.id)

        mail_parameter_dict = {
            'html_template_content_path' : html_template_content_path,
             'subject' : user_mail['subject'],
            'to_mail_id' : [user_mail['email_id']], 'content' : user_mail['content'],
            'click_link' : click_link, 'open_link' : open_link, 'unsubscribe_link' : unsubscribe_link
        }

        val = send_mail(mail_parameter_dict)
        count += val
        total_mails += 1

        email_info_obj = EmailsInfo.objects.get(id=email_info.id).email_activity
        email_info_obj.email_delivered = val
        email_info_obj.save()

    main_response = CustomerOverview()
    main_response.success = True
    main_response.error_code = 0
    main_response.status_code = status.HTTP_200_OK
    main_response.data = CustomerOverviewResponse(count, total_mails)
    serializer = CustomerOverViewMainSerializer(main_response)

    return Response(serializer.data)



@api_view(['GET'])
def register_click_activity(request, mail_id):

    email_info_obj = EmailsInfo.objects.get(id=mail_id).email_activity
    email_info_obj.email_clicked = True
    email_info_obj.save()

    html_send_mail_template_path = 'notify/click_mail_template.html'
    html_template_context = get_template(html_send_mail_template_path)
    html_template = html_template_context.render({})

    return HttpResponse(html_template)


@api_view(['GET'])
def register_open_activity(request, mail_id):

    email_info_obj = EmailsInfo.objects.get(id=mail_id).email_activity
    email_info_obj.email_opened = True
    email_info_obj.save()

    html_send_mail_template_path = 'notify/open_mail_template.html'
    html_template_context = get_template(html_send_mail_template_path)
    html_template = html_template_context.render({})

    return HttpResponse(html_template)

@api_view(['GET'])
def register_unsubscribe_activity(request, camp_id, mail_id):
    """
    Unsubscribe the email. It register campaign id of the mail unsubscribed. So admin can fetch 
    the category of mail user do not wish to receive.
    """
    email_info_obj = EmailsInfo.objects.get(id=mail_id)
    customer_view_obj = CustomerView.objects.get(campaign_id = camp_id)
    EmailsUnsubscribed.objects.get_or_create(mail = email_info_obj.user_mail_id, unsubscribed = True,\
         customer = customer_view_obj)

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


@api_view(['GET'])
def customer_mail_action(request, mail_id):

    email_info_obj = EmailsInfo.objects.get(id=mail_id).email_activity
    email_info_obj.email_unsubscribed = True
    email_info_obj.save()
    
    html_send_mail_template_path = 'notify/unsubscribe_mail_template.html'
    html_template_context = get_template(html_send_mail_template_path)
    html_template = html_template_context.render({})

    return HttpResponse(html_template)



@api_view(['GET'])
def mail_performance(request):

    unique_emails = list(EmailsInfo.objects.values('user_mail_id').distinct())
    print(unique_emails)
    customer_mail_performance = []
    for email in unique_emails:
        customer_performance = {}
   
        user_email = email['user_mail_id']
        username = EmailsInfo.objects.filter(user_mail_id = email['user_mail_id']).first().user_name
        last_mail_sent_datetime = EmailsInfo.objects.filter(user_mail_id = email['user_mail_id']).order_by('-sent_datetime').first().sent_datetime.strftime('%d/%m/%Y - %H:%M:%S')
        mail_sent_count =  EmailsInfo.objects.filter(user_mail_id = email['user_mail_id']).count()
        click_mail_count = EmailsInfo.objects.filter( Q(email_activity__email_clicked = 1) , Q(user_mail_id = email['user_mail_id'])).count()
        email_delivered_count = EmailsInfo.objects.filter( Q(email_activity__email_delivered = 1) , Q(user_mail_id = email['user_mail_id'])).count()

        customer_performance['user_email'] = user_email
        customer_performance['username'] = username
        customer_performance['last_mail_sent_datetime'] = last_mail_sent_datetime
        customer_performance['mail_sent_count'] = mail_sent_count
        customer_performance['click_mail_count'] = click_mail_count
        customer_performance['email_delivered_count'] = email_delivered_count

        customer_mail_performance.append(customer_performance)

    print(customer_mail_performance)
    main_response = CustomerOverview()
    main_response.success = True
    main_response.error_code = 0
    main_response.status_code = status.HTTP_200_OK
    main_response.data = MailPerformanceResponse(customer_mail_performance)
    serializer = CustomerMailPerformaceMainSerializer(main_response)

    return Response(serializer.data)
    # email_info_obj = EmailsInfo.objects.values('user_mail_id').annonate()
    # email_info_obj.email_unsubscribed = True
    # email_info_obj.save()
    


    # html_send_mail_template_path = 'notify/unsubscribe_mail_template.html'
    # html_template_context = get_template(html_send_mail_template_path)
    # html_template = html_template_context.render({})

    # return HttpResponse(html_template)