

class CustomerOverview(object):
    success = None
    error = None
    data = None
    status = None


class CustomerOverviewResponse(object):
    mail_delivered = None
    total_mail_sent = None

    def __init__(self, count, total_mails):
        self.mail_delivered = count
        self.total_mail_sent = total_mails

class AllCustomerMails(object):
    user_email = None
    username = None
    last_mail_sent_datetime = None
    mail_sent_count = None
    click_mail_count = None
    email_delivered_count = None


class MailPerformanceResponse(object):
    customer_view = None


    def __init__(self, customer_mail_performance):
        self.customer_view = MailPerformanceResponse.process_mail_performance(customer_mail_performance)
    
    @staticmethod
    def process_mail_performance(mails_performace):
        ret_val = []

        for mail_response in mails_performace:
            print('-----------------')
            print(mail_response)
            print("######################")
            mail_result = AllCustomerMails()
            mail_result.user_email = mail_response['user_email']
            mail_result.username = mail_response['username']
            mail_result.last_mail_sent_datetime = mail_response['last_mail_sent_datetime']
            mail_result.mail_sent_count = mail_response['mail_sent_count']
            mail_result.click_mail_count = mail_response['click_mail_count']
            mail_result.email_delivered_count = mail_response['email_delivered_count']

            ret_val.append(mail_result)
        
        return ret_val


class CustomerMailDetails(object):

    mail_id = None
    email_clicked = None
    email_opened = None
    email_delivered = None
    email_unsubscribed = None

    def __init__(self, customer_mail_details):
        self.mail_id = customer_mail_details['mail_id']
        self.email_clicked = customer_mail_details['email_clicked']
        self.email_opened = customer_mail_details['email_opened']
        self.email_delivered = customer_mail_details['email_delivered']
        self.email_unsubscribed = customer_mail_details['email_unsubscribed']