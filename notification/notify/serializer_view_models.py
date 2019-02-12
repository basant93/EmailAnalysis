from rest_framework import serializers


class CustomerInfoSerializer(serializers.Serializer):
    mail_delivered = serializers.IntegerField()
    total_mail_sent = serializers.IntegerField()



class CustomerOverViewMainSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    error_code = serializers.IntegerField()
    status_code = serializers.CharField()
    data = CustomerInfoSerializer()
