from django.urls import path, include
from . import views

urlpatterns = [

    path('user/mail', views.send_user_email, name='user_email' ),
    path('activity/click/<mail_id>', views.register_click_activity, name='user_click' ),
    path('unsubscribe/<mail_id>', views.register_unsubscribe_activity, name='user_unsubscribe' ),
    path('activity/open/<mail_id>', views.register_open_activity, name='user_open' ),
    path('customer/overview', views.customer_overview, name='user_overview' ),
    path('mail/action', views.customer_mail_action, name='user_action' ),
    path('mail/performance', views.mail_performance, name='user_performance' ),
]

