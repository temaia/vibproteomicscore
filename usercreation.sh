#!/bin/bash

/home/pportal/dev2Sep18/myenv3/bin/python /home/pportal/dev2Sep18/myenv3/pportal3/manage.py shell

import csv
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.mail import send_email
User = get_user_model()

user = User.objects.filter(email='teresa.maia#vib-ugent.be').get()

subject = '[VIB Proteomics Core, New Project] '+user.profile.Project_ID
message = render_to_string('requests/templates/InvitationForRegistrationEmail.txt', {'user': user})
html_message = render_to_string('requests/templates/InvitationForRegistrationEmail.html', {'user': user})
from_email=settings.EMAIL_HOST_USER
to_list = [user.email]