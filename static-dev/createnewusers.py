import csv
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.template.loader import get_template
User = get_user_model()

with open("static-dev/newusers.csv", "r") as csvfile:
    userreader = csv.reader(csvfile, delimiter=',')
    for usor in userreader:
        User.objects.create_user(email=usor[0], password = usor[1])
    for usor in userreader:
        user = User.objects.filter(email=usor[0]).get()
        user.profile.Email= user.email
        user.profile.Project_ID = usor[3]
        user.profile.Main_Analysis_Type  = usor[2]
        user.save()

user = User.objects.filter(email='teresa.maia@vib-ugent.be').get()
template1 = get_template('InvitationForRegistrationEmail.txt')
template2 = get_template('InvitationForRegistrationEmail.html')
subject = '[VIB Proteomics Core, New Project] '+user.profile.Project_ID
message = render_to_string(template1, {'user': user})
html_message = render_to_string(template2, {'user': user})
from_email=settings.EMAIL_HOST_USER
to_list = [user.email]
send_mail(subject, message, from_email, to_list, html_message=html_message, fail_silently=False)

template2 = '/home/pportal/dev2Sep18/myenv3/pportal3/templates/InvitationForRegistrationEmail.html'
>>> template1 = '/home/pportal/dev2Sep18/myenv3/pportal3/templates/InvitationForRegistrationEmail.txt'
>>> message = render_to_string(template1, {'user': user})
>>> html_message = render_to_string(template2, {'user': user})
>>> from_email=settings.EMAIL_HOST_USER
>>> to_list = [user.email]
>>> send_mail(subject, message, from_email, to_list, html_message=html_message, fail_silently=False)
1
>>> user.email
'teresa.maia@vib-ugent.be'
>>> send_mail(subject, message, from_email, to_list, html_message=html_message, fail_silently=False)
1
>>> template1 = '/home/pportal/dev2Sep18/myenv3/pportal3/templates/InvitationForRegistrationEmail.txt'
>>> template2 = '/home/pportal/dev2Sep18/myenv3/pportal3/templates/InvitationForRegistrationEmail.html'
>>> send_mail(subject, message, from_email, to_list, html_message=html_message, fail_silently=False)


