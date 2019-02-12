

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