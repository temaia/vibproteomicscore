# coding=UTF-8

import csv
import os
import json
from prcprojects.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings
#from youtrack.connection import Connection, httplib2
from xml.etree.ElementTree import fromstring
import random
import urllib
import csv
import re
import time
import datetime
import httpx
import pandas as pd
#from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.template.loader import get_template
from django.templatetags.static import static
from utils.utils import youtrack_get,youtrackurl_get,ytclient
#httplib2.debuglevel=4
#httplib.debuglevel=4


class Command(BaseCommand):
    help='Gets new users from YouTrack'

    #def add_arguments(self, parser):
    #    parser.add_argument('usersfile', type=str, help='Indicates the number os users to be created')
        #User.objects.create_user(email=usor[0], password = usor[1],Main_analysis_type  = usor[2])

    def handle(self, *args, **kwargs):
        #configfile = static("acessorio.json")
        configfile=os.path.join(settings.BASE_DIR, "static/acessorio.json")
        with open(configfile) as config_file:
            config = json.load(config_file)
        #client = httpx.Client(base_url="http://127.0.0.1:8112/api")#,
        #YTTOKR = youtrack_get()
        client = ytclient(youtrackurl_get())
        url = str(client.base_url)+"issues"
        headers = {'Authorization': 'Bearer {}'.format(config['YTTOKR'])}
        params = {'fields':'id,idReadable,name,created,summary,customFields(id,value(id, localizedName,name),name)', 'query':'in:PRC'}
        #yt = Connection(url='https://youtrack.ugent.be', token=config['YTTOKR']) 
        # get CMB issues
        PRCissues = client.get(url, params = params, headers = headers)
        PRCissuefieldsjson = PRCissues.json()

        def prepareProjectIssuesDict(jsonObj):
            '''
            # get dictionary with fields&values
            '''
            issuesdict = dict()
            for issue in jsonObj:  
                cfs = issue['customFields']
                cfsdict = dict()
                cfsdict['idReadable'] = issue['idReadable']
                cfsdict['summary'] = issue['summary']
                cfsdict['created'] = issue['created']
                for cf in cfs:
                    cfname = cf['name']
                    cfvalue = cf['value']
                    if isinstance(cfvalue, dict):
                        if 'name' in cfvalue.keys():
                            cfvalue = cfvalue['name']
                        else:
                            cfvalue = ''
                    elif isinstance(cfvalue,list):
                        for el in cfvalue:
                            if 'name' in el.keys():
                                 cfvalue = el['name']
                            else:cfvalue = ''
                                    
                    cfsdict[cfname]=cfvalue
                # new issues (created less than 40h ago) fiter-in
                if datetime.datetime.now() - datetime.datetime.fromtimestamp(int(cfsdict["created"])/1000)<datetime.timedelta(hours=40):
                    issuesdict[cfsdict['idReadable']] = cfsdict
            return(issuesdict)

        # open PRC issue IDs   
        #print(PRCissuefieldsjson)     
        PRCIssuesDict= prepareProjectIssuesDict(PRCissuefieldsjson)
        #filename = os.path.join("/home/pportal/Downloads", "PRC_issues_creation_hourly.csv")  
        filename=os.path.join(settings.BASE_DIR, "static/PRC_issues_creation_hourly.csv")
        with open(filename, 'w', encoding='utf-8') as csvfile:
            #csvfile.write('Running start date\tLab PI\tType\tUser Name\tYouTrack\tProject Name (YouTrack)\t# samples\tMS_Injections_Per_Sample\trun length (hours)\ttotal running time (hours)\tMass_Spectrometer\tCreated_DateH\tArrival_DateH\tMS_RunStateH\tMS_RunStatesH\tMS_RunStatesnrH\tre-runs/problems\tMS_RunStartH\tMS_RunStartsH\tMS_RunStartsnrH\tresolvedH\tResolvedDateH\tCleatedDate\n')
            #csvfile.write('YouTrack_id,Contact_Email,Analysis_Type\n')
            i=0
            for issuekey in PRCIssuesDict:
                # issue
                issue = PRCIssuesDict[issuekey]
                # name of fields in issue
                indices = list(issue.keys())
                # YouTrack_id
                issueid=issue['idReadable']
                # Project_name
                issuecontactemail=issue['Contact_Email']
                # sendRegistrationEmail
                if 'sendRegistrationEmail' in indices:
                    issuesendregistrationemail=issue['sendRegistrationEmail']
                else:
                    issuesendregistrationemail='Yes'
                # No_Samples
                if 'Analysis_Type' in indices:
                    issueAnalysisType=str(issue['Analysis_Type'])
                else:
                    issueAnalysisType='None'      
                row = issueid+',' + issuecontactemail + ',' + issueAnalysisType + ',' + issuesendregistrationemail     
                row = row + '\n'
                csvfile.write(row,)
                i = i+1

        # PRCissuesIDs = []
        # Currentissuesindexes = list()
        # counter=0
        # for issue in PRCissues:
        #     #print(issue['id'])
        #     if datetime.datetime.now() - datetime.datetime.fromtimestamp(int(issue["created"])/1000)<datetime.timedelta(hours=40):
        #     #timesincecreation = datetime.datetime.now() - datetime.datetime.fromtimestamp(int(issue["created"])/1000)
        #     #if timesincecreation < datetime.timedelta(hours=60) and timesincecreation > datetime.timedelta(hours=1):
        #         PRCissuesIDs.append(issue["id"])
        #         Currentissuesindexes.append(counter)
        #     counter = counter+1
        # # update PRCissues (filter State Closed)
        # print(PRCissuesIDs)
        # PRCissues = [PRCissues[index] for index in Currentissuesindexes]
        # filename=os.path.join(settings.BASE_DIR, "static/PRC_issues_creation_hourly.csv")   
        # with open(filename, 'w', encoding='utf-8') as csvfile:
        #     #csvfile.write('Running start date\tLab PI\tType\tUser Name\tYouTrack\tProject Name (YouTrack)\t# samples\tMS_Injections_Per_Sample\trun length (hours)\ttotal running time (hours)\tMass_Spectrometer\tCreated_DateH\tArrival_DateH\tMS_RunStateH\tMS_RunStatesH\tMS_RunStatesnrH\tre-runs/problems\tMS_RunStartH\tMS_RunStartsH\tMS_RunStartsnrH\tresolvedH\tResolvedDateH\tCleatedDate\n')
        #     #csvfile.write('YouTrack_id,Contact_Email,Analysis_Type\n')
        #     i=0
        #     for issue in PRCissues:
        #         # name of fields in issue
        #         indices = list()
        #         for attr_name, attr_type in issue._attribute_types.items():
        #             indices.append(attr_name)
        #             # YouTrack_id
        #         issueid=issue['id']
        #         # Project_name
        #         issuecontactemail=issue['Contact_Email']
        #         # sendRegistrationEmail
        #         if 'sendRegistrationEmail' in indices:
        #             issuesendregistrationemail=issue['sendRegistrationEmail']
        #         else:
        #             issuesendregistrationemail='Yes'
        #         # No_Samples
        #         if 'Analysis_Type' in indices:
        #             issueAnalysisType=str(issue['Analysis_Type'])
        #         else:
        #             issueAnalysisType='None'      
        #         row = issueid+',' + issuecontactemail + ',' + issueAnalysisType + ',' + issuesendregistrationemail     
        #         row = row + '\n'
        #         csvfile.write(row,)
        #         i = i+1
