# EmailAnalysis

Install the packages from requirements.txt

pip install -r requirements.txt

Setup the MySql database. Change the db name and password in settings.py file in notification folder.

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mail',
        'USER': 'root',
        'PASSWORD': 'root',
    }
}


Setup a new email account and set up your deatils.

EMAIL_HOST_USER = 'bk78196@gmail.com'
EMAIL_HOST_PASSWORD = ''
