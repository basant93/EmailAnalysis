from django.template.loader import get_template
from django.template import Context
from django.core.mail import EmailMultiAlternatives



def send_mail(mail_parameter):

    html_template_context = get_template(mail_parameter['html_template_content_path'])
    #context = Context({'context' : mail_parameter})
    context = {'context' : mail_parameter}

    html_template = html_template_context.render(context)
    text_content = "This is deafult message. Email html content was not rendered."
    

    mail = EmailMultiAlternatives(mail_parameter['subject'], text_content, mail_parameter['sender_mail'],
            mail_parameter['mail_id'] )

    mail.attach_alternative(html_template, 'text/html')
    print(mail)
    print(mail.send())
    #mail.send()