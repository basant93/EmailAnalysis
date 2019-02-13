from rest_framework import serializers


class CustomerInfoSerializer(serializers.Serializer):
    mail_delivered = serializers.IntegerField()
    total_mail_sent = serializers.IntegerField()


class CustomerOverViewMainSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    error_code = serializers.IntegerField()
    status_code = serializers.CharField()
    data = CustomerInfoSerializer()


class MailPerformaceDetailsSerializer(serializers.Serializer):
    user_email = serializers.EmailField()
    username = serializers.CharField()
    last_mail_sent_datetime = serializers.CharField()
    mail_sent_count = serializers.IntegerField()
    click_mail_count = serializers.IntegerField()
    email_delivered_count = serializers.IntegerField()


class MailPerformaceInfoSerializer(serializers.Serializer):
    customer_view = MailPerformaceDetailsSerializer(many=True)


class CustomerMailPerformaceMainSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    error_code = serializers.IntegerField()
    status_code = serializers.CharField()
    data = MailPerformaceInfoSerializer()


class CustomerMailDetailsSerializer(serializers.Serializer):
    mail_id = serializers.EmailField()
    email_clicked = serializers.IntegerField()
    email_opened = serializers.IntegerField()
    email_delivered = serializers.IntegerField()
    email_unsubscribed = serializers.IntegerField()



class CustomerMailDetailsMainSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    error_code = serializers.IntegerField()
    status_code = serializers.CharField()
    data = CustomerMailDetailsSerializer()