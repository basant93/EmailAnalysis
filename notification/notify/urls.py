from django.urls import path, include
from . import views

urlpatterns = [

    path('user/mail', views.send_user_email, name='user_email' ),
    path('activity/click/<camp_id>/<mail_id>', views.register_click_activity, name='user_click' ),
    path('unsubscribe/<camp_id>/<mail_id>', views.register_unsubscribe_activity, name='user_unsubscribe' ),
    path('activity/open/<camp_id>/<mail_id>', views.register_open_activity, name='user_open' ),
    path('customer/overview', views.register_open_activity, name='user_open' ),
]