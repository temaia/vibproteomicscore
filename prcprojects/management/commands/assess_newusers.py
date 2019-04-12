import csv
import os
import json
from prcprojects.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings
#from django.conf.urls.static import static
#from django.contrib.staticfiles.templatetags.staticfiles import static
# coding=UTF-8

from youtrack.connection import Connection, httplib2
from xml.etree.ElementTree import fromstring
import random
import urllib
import csv
import re
import time
import datetime
#from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.template.loader import get_template
from django.templatetags.static import static
httplib2.debuglevel=4

# def username_present(username):
# 	if User.objects.filter(username=username).exists():
# 		return True

class Command(BaseCommand):
	help='Gets new users from YouTrack'

	#def add_arguments(self, parser):
	#	parser.add_argument('usersfile', type=str, help='Indicates the number os users to be created')
		#User.objects.create_user(email=usor[0], password = usor[1],Main_analysis_type  = usor[2])

	def handle(self, *args, **kwargs):
		#configfile = static("acessorio.json")
		configfile=os.path.join(settings.BASE_DIR, "static/acessorio.json")
		with open(configfile) as config_file:
			config = json.load(config_file)
		yt = Connection(url='https://youtrack.ugent.be', token=config['YTTOKR']) #@
		# get CMB issues
		PRCissues = yt.get_all_issues("PRC-",0,500)
		# open PRC issue IDs
		PRCissuesIDs = []
		Currentissuesindexes = list()
		counter=0
		for issue in PRCissues:
		    if datetime.datetime.now() - datetime.datetime.fromtimestamp(int(issue["created"])/1000)<datetime.timedelta(hours=40):
		        PRCissuesIDs.append(issue["id"])
		        Currentissuesindexes.append(counter)
		    counter = counter+1
		# update PRCissues (filter State Closed)
		PRCissues = [PRCissues[index] for index in Currentissuesindexes]
		filename=os.path.join(settings.BASE_DIR, "static/PRC_issues_creation_hourly.csv")   
		with open(filename, 'w') as csvfile:
		    #csvfile.write('Running start date\tLab PI\tType\tUser Name\tYouTrack\tProject Name (YouTrack)\t# samples\tMS_Injections_Per_Sample\trun length (hours)\ttotal running time (hours)\tMass_Spectrometer\tCreated_DateH\tArrival_DateH\tMS_RunStateH\tMS_RunStatesH\tMS_RunStatesnrH\tre-runs/problems\tMS_RunStartH\tMS_RunStartsH\tMS_RunStartsnrH\tresolvedH\tResolvedDateH\tCleatedDate\n')
		    #csvfile.write('YouTrack_id,Contact_Email,Analysis_Type\n')
		    i=0 
		    for issue in PRCissues:
		        # name of fields in issue
		        indices = list()
		        for attr_name, attr_type in issue._attribute_types.items():
		            indices.append(attr_name)
		        # YouTrack_id
		        issueid=issue['id']
		        # Project_name
		        issuecontactemail=issue['Contact_Email']
		        # No_Samples
		        if 'Analysis_Type' in indices:
		            issueAnalysisType=str(issue['Analysis_Type'])
		        else:
		            issueAnalysisType='None'      
		        row = issueid+',' + issuecontactemail + ',' + issueAnalysisType
		        row = row + '\n'
		        csvfile.write(row,)
		        i = i+1
