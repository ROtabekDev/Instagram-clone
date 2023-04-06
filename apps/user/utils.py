import requests
from os import getenv
from django.core.mail import send_mail
from django.conf import settings

phone_regex_pattern = r'^\+998\d{9}$'
email_regex_pattern = r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'


def send_sms_by_phone(data):
    # Define the URL endpoint to which the POST request will be sent
    url = "https://notify.eskiz.uz/api/message/sms/send"

    # Define the Bearer token to be included in the Authorization header
    token = getenv("SMS_TOKEN")

    # Define the headers to be included in the request
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Make the POST request with requests.post()
    response = requests.post(url, json=data, headers=headers)
    # Check if the request was successful
    if response.status_code == 200:
        return True
    return False



def send_sms_by_email(email, code):
    subject = f'SMS CODE'
    message = f'\n\nYour sms code : {code}\n\n'
    mail_sent = send_mail(subject, message, settings.EMAIL_HOST_USER, [email])
    print(mail_sent, 'send_sms_by_email')
    return mail_sent