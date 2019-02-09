from django.urls import path, include
from . import views

urlpatterns = [

    path('user/mail', views.send_user_email, name='user_email' ),
    #path('user/mail', views.send_user_email, name='user_email' ),
]