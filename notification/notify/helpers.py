from django.template.loader import get_template
from django.template import Context
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from notify.utils import validate_user_email


def send_mail(mail_parameter):

    html_template_context = get_template(mail_parameter['html_template_content_path'])
    #context = Context({'context' : mail_parameter})
    context = {'context' : mail_parameter}

    html_template = html_template_context.render(context)
    text_content = "This is default message. Email html content was not been rendered."
    

    mail = EmailMultiAlternatives(mail_parameter['subject'], text_content, settings.EMAIL_HOST_USER,
            mail_parameter['to_mail_id'] )

    mail.attach_alternative(html_template, 'text/html')
#     print(mail)
#     print(mail.send())
    return mail.send()


def valid_email_response(user_mails):
    user_email_content = []
    check_dup_mails = []

    for user_mail in user_mails:
        mail = user_mail['email_id']

        if(validate_user_email(mail)  and mail not in check_dup_mails):
            user_email_content.append(user_mail)
            check_dup_mails.append(mail)
    
    return user_email_content
