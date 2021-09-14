import csv
import os

from prcprojects.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.templatetags.staticfiles import static
#from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.template.loader import get_template

def username_present(username):
	if User.objects.filter(username=username).exists():
		return True

class Command(BaseCommand):
	help='Creates new user from PRC_issue_creation.csv'

	#def add_arguments(self, parser):
	#	parser.add_argument('usersfile', type=str, help='Indicates the number os users to be created')
		#User.objects.create_user(email=usor[0], password = usor[1],Main_analysis_type  = usor[2])

	def handle(self, *args, **kwargs):
		#usersfile = kwargs['usersfile']
		usersfile=os.path.join(settings.BASE_DIR, "static/PRC_issue_creation.csv")
		with open(usersfile, "r", encoding='utf-8') as csvfile:
			userreader = csv.reader(csvfile, delimiter=',')
			for usor in userreader:
				if not username_present(usor[0]):
					print(usor[0])
					password = User.objects.make_random_password(length=5, allowed_chars="ABCDEFGHIJKLMNOPQRSTUVWXZ0123456789")
					User.objects.create_user(username=usor[0],email=usor[1], password = password, Main_analysis_type  = usor[2])
					#User.objects.create_user(username=usor[0],email=usor[1], password = password, Main_analysis_type  = usor[2])
					user = User.objects.filter(username=usor[0]).get()
					#user = User.objects.filter(email=usor[1]).get()
					#template1 = os.path.join(settings.BASE_DIR , 'templates/InvitationForRegistrationEmail2.txt')
					template2 = os.path.join(settings.BASE_DIR, 'templates/InvitationForRegistrationEmail2.html')
					subject = "VIB Proteomics Core New Project"
					#message = render_to_string(template1, {'user': user})
					html_message = render_to_string(template2, {'user': user,'pw': password})
					from_email=settings.EMAIL_HOST_USER
					to_list = [user.email]
					bcc = [settings.ADMINS[0][1],settings.ADMINS[1][1]]
					msg=EmailMessage(subject, html_message, from_email, to_list, bcc)
					msg.content_subtype = "html"
					msg.send()
				#User.objects.create_user(username="PRC-21", password=password, email="mariana@gmail.com", Main_analysis_type = "PRM")
			
		# self.stdout.write("User %s created" % usor[0])
        #User.objects.create_user(username="PRC-21", password=password, email="mariana@gmail.com", Main_analysis_type = "PRM")
        #from requests.models import User
        #password = User.objects.make_random_password(length=5, allowed_chars="ABCDEFGHIJKLMNOPQRSTUVWXZ0123456789")
