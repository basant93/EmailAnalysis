
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

#Validate the mail id. Returns True if mail is valid else False
def validate_user_email(email):

    try:
        validate_email(email)
        return True
    except ValidationError:
        return False