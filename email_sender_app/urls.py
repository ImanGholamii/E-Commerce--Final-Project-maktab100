from django.urls import path
from email_sender_app.views import send_email_view

app_name = 'email_sender'
urlpatterns = [
    path('send/', send_email_view, name='send-email'),
]