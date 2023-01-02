from django.core.mail import EmailMessage
from django.conf import settings
import json

def send_mail_to_user(email_to,subject,message):
    try:
        email_from = settings.EMAIL_HOST_USER
        email = EmailMessage(subject,message,email_from,[email_to])

        attach_files = ['info.json','starred.json','top10_contributors.json']
        
        for file in attach_files:    
            f = open(file,'r')
            data = json.dumps(json.load(f)).encode('utf-8')
            email.attach(file,data,'file/json')
        
        if email.send():
            return True
        return False

    except Exception as e:
        print(e)