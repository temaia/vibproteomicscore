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
import re
import time
import pandas as pd
import httpx
from utils.utils import youtrack_get,youtrackurl_get,ytclient
#httplib2.debuglevel=4
#httplib.debuglevel=4
# connection

class Command(BaseCommand):
    help='YouTrack issues update from Created to Closed, all projects'

    #def add_arguments(self, parser):
    #   parser.add_argument('usersfile', type=str, help='Indicates the number os users to be created')
        #User.objects.create_user(email=usor[0], password = usor[1],Main_analysis_type  = usor[2])

    def handle(self, *args, **kwargs):
        configfile=os.path.join(settings.BASE_DIR, "static/acessorio.json")
        with open(configfile) as config_file:
            config = json.load(config_file)
        #client = httpx.Client(base_url="http://127.0.0.1:8112/api")#,
        #YTTOKR = youtrack_get()
        client = ytclient(youtrackurl_get())
        url = str(client.base_url)+"issues"
        headers = {'Authorization': 'Bearer {}'.format(config['YTTOKR'])}
        #params = {'fields':'id,idReadable,name,created,summary,customFields(id,value(id, localizedName,name),name)', 'query':'in:PRC'}
        #yt = Connection(url='https://youtrack.ugent.be', token=config['YTTOKR']) 
        # get CMB issues
#params={'fields':'id,isReadable,summary,customFields(id,projectCustomField(field(name,value)))',
                                          # 'query':'in:PRC'}
        params = {'fields':'id,idReadable,name,summary,customFields(id,value(id, localizedName,name),name)', 'query':'in:PRC'}
        PRCissuefields = client.get(url, params = params, headers = headers)
        params = {'fields':'id,idReadable,name,summary,customFields(id,value(id, localizedName,name),name)', 'query':'in:PSB'}
        PSBissuefields = client.get(url, params = params, headers = headers)
        params = {'fields':'id,idReadable,name,summary,customFields(id,value(id, localizedName,name),name)', 'query':'in:CMB'}
        CMBissuefields = client.get(url, params = params, headers = headers)
        params = {'fields':'id,idReadable,name,summary,customFields(id,value(id, localizedName,name),name)', 'query':'in:MSStatus'}
        MSSissuefields = client.get(url, params = params, headers = headers)

        PRCissuefieldsjson = PRCissuefields.json()
        PSBissuefieldsjson = PSBissuefields.json()
        CMBissuefieldsjson = CMBissuefields.json()
        MSSissuefieldsjson = MSSissuefields.json()
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
                # unresolved issues fiter-in
                if cfsdict['State'] in ['Arrived', 'Sample_Prep',"MS_Run","Data_Analysis"]:
                    issuesdict[cfsdict['idReadable']] = cfsdict
            return(issuesdict)

        def prepareProjectIssuesDictMSS(jsonObj):
            issuesdict = dict()
            for issue in jsonObj:  
                cfs = issue['customFields']
                cfsdict = dict()
                cfsdict['idReadable'] = issue['idReadable']
                cfsdict['summary'] = issue['summary']
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
                issuesdict[cfsdict['idReadable']] = cfsdict
            return(issuesdict)

        PRCIssuesDict= prepareProjectIssuesDict(PRCissuefieldsjson)
        PSBIssuesDict= prepareProjectIssuesDict(PSBissuefieldsjson)
        CMBIssuesDict= prepareProjectIssuesDict(CMBissuefieldsjson)
        MSSIssuesDict= prepareProjectIssuesDictMSS(MSSissuefieldsjson)
                
        #filename =os.path.join(settings.BASE_DIR, "static/PRCCMBPSB_issues_dailyreport.csv")
        def writeIssuesDictToFile(ProjectIssuesFullDict_list,filename):
            '''
            # write to csv file with issues custom fields
            '''
            with open(filename, 'w', encoding='utf-8') as csvfile:
                #csvfile.write('Running start date\tLab PI\tType\tUser Name\tYouTrack\tProject Name (YouTrack)\t# samples\tMS_Injections_Per_Sample\trun length (hours)\ttotal running time (hours)\tMass_Spectrometer\tCreated_DateH\tArrival_DateH\tMS_RunStateH\tMS_RunStatesH\tMS_RunStatesnrH\tre-runs/problems\tMS_RunStartH\tMS_RunStartsH\tMS_RunStartsnrH\tresolvedH\tResolvedDateH\tCleatedDate\n')
                csvfile.write('YouTrack_id,No_Samples,total_running_time,Mass_Spectrometer,State,Scheduling_State,Project_Name\n')
                i=0
                for IssuesDict in ProjectIssuesFullDict_list:
                    for issuekey in IssuesDict:
                        # name of fields in issue
                        issue = IssuesDict[issuekey]
                        indices = list(issue.keys())
                        #for attr_name, attr_type in issue._attribute_types.items():
                         #   indices.append(attr_name)
                        # YouTrack_id
                        issueid=issue['idReadable']
                        # Project_name
                        issuesummary=issue['summary']
                        # No_Samples
                        if 'No_Samples' in indices:
                            issueNoSamples=str(issue['No_Samples'])
                        else:
                            issueNoSamples='None'
                        # total running time (hours)
                        if 'MS_Total_Time_h' in indices:
                            issueMS_Total_Time_h=str(issue['MS_Total_Time_h'])
                        else:
                            issueMS_Total_Time_h='None'
                        # Mass_Spectrometer
                        if 'Mass_Spectrometer' in indices:
                            issueMassSpectrometer=issue['Mass_Spectrometer']
                        else:
                            issueMassSpectrometer='None'
                        # State
                        if 'State' in indices:
                            issueState=issue['State']
                        else:
                            issueState='None'
                        # Scheduling_State
                        if 'Scheduling_State' in indices:
                            issueSchedulingState=issue['Scheduling_State']
                        else:
                            issueSchedulingState='None'        
                        row = issueid+','  + issueNoSamples+ ',' + issueMS_Total_Time_h + ',' + issueMassSpectrometer + "," + issueState + "," + issueSchedulingState + ',' + issuesummary
                        row = row + '\n'
                        csvfile.write(row,)
                        i = i+1
                csvfile.close()

        #filename = os.path.join("/home/pportal/Downloads", "PRCCMBPSB_issues_dailyreport.csv")
        filename =os.path.join(settings.BASE_DIR, "static/PRCCMBPSB_issues_dailyreport.csv")
        writeIssuesDictToFile([PRCIssuesDict,CMBIssuesDict,PSBIssuesDict], filename)

        filename =os.path.join(settings.BASE_DIR, "static/MSSissues_issues_dailyreport.csv")
        #filename = os.path.join("/home/pportal/Downloads", "MSSissues_issues_dailyreport.csv")
        #filename =os.path.join(settings.BASE_DIR, "static/MSSissues_issues_dailyreport.csv")
        with open(filename, 'w', encoding='utf-8') as csvfile:
            csvfile.write('Mass_Spectrometer,Status,Status_description\n')
            i=0
            MSindexed_lst = ['Orbitrap Fusion Lumos','Q-Exactive HF','Q-Exactive HF Biopharma', 'Q-Exactive','LTQ Orbitrap Elite']
            rowlist=[None]*5
            for issuekey in MSSIssuesDict:
                # name of fields in issue
                issue = MSSIssuesDict[issuekey]
                indices = list(issue.keys())
                #indices = list()
                #MSindexed_lst = ['Orbitrap Fusion Lumos','Q-Exactive HF','Q-Exactive HF Biopharma', 'Q-Exactive','LTQ Orbitrap Elite']
                #for i in range(5):
                # Mass Spectrometer
                #issue = MSSIssuesDict[indices[i]]
                #indices = list()
                #for attr_name, attr_type in issue._attribute_types.items():
                #    indices.append(attr_name)
                issueMS=issue['Mass_Spectrometer']
                # MassSpec status
                issueStatus=issue['Status']
                # Status description
                if 'Status_description' in indices:
                    issueStatusdescription=str(issue['Status_description']).lower()
                elif issueStatus == "On":
                    issueStatusdescription='running'
                else:
                    issueStatusdescription='under maintenance'
                row = issueMS + ',' + issueStatus + "," + issueStatusdescription
                row = row + '\n'
                rowlist[MSindexed_lst.index(issueMS)]=row
                i = i+1
            for i in range(5):
                csvfile.write(rowlist[i])
            csvfile.close()



        # CMBissues = yt.get_all_issues("CMB",0,1500)
        # PSBissues = yt.get_all_issues("PSB",0,1500)
        # MSSissues = yt.get_all_issues("MSStatus-",0,100)

        # issue IDs per project

        # open PRC issue IDs
        # PRCissuesIDs = []
        # PRCCurrentissuesindexes = list()
        # counter=0
        # for issue in PRCissues:
        #     if issue["State"]=='Created' or issue["State"]=='Arrived' or issue["State"]=='Sample_Prep' or issue["State"]=="MS_Run" or issue["State"]=="Data_Analysis" or issue["State"]=="Closed":
        #         PRCissuesIDs.append(issue["id"])
        #         PRCCurrentissuesindexes.append(counter)
        #     counter = counter+1
        # # update PRCissues (filter State Closed)
        # PRCissues = [PRCissues[index] for index in PRCCurrentissuesindexes]

        # CMBissuesIDs = []
        # CMBCurrentissuesindexes = list()
        # counter=0
        # for issue in CMBissues:
        #     if issue["State"]=='Arrived' or issue["State"]=='Sample_Prep' or issue["State"]=="MS_Run" or issue["State"]=="Data_Analysis":
        #         CMBissuesIDs.append(issue["id"])
        #         CMBCurrentissuesindexes.append(counter)
        #     counter = counter+1
        # # update PRCissues (filter State Closed)
        # CMBissues = [CMBissues[index] for index in CMBCurrentissuesindexes]

        # PSBissuesIDs = []
        # PSBCurrentissuesindexes = list()
        # counter=0
        # for issue in PSBissues:
        #     if issue["State"]=='Arrived' or issue["State"]=='Sample_Prep' or issue["State"]=="MS_Run" or issue["State"]=="Data_Analysis":
        #         PSBissuesIDs.append(issue["id"])
        #         PSBCurrentissuesindexes.append(counter)
        #     counter = counter+1
        # # update PRCissues (filter State Closed)
        # PSBissues = [PSBissues[index] for index in PSBCurrentissuesindexes]
           
        # # function to handle inhesistent attributes    
        # def find_attribute_in_list(element, list_element):
        #     try:
        #         index_element = list_element.index(element)
        #         return index_element
        #     except ValueError:
        #         return 'None'
        # #filename ="/home/pportal/dev2Sep18/prcsite/vibproteomicscore/static/PRCCMBPSB_issues_dailyreport.csv"
        # filename =os.path.join(settings.BASE_DIR, "static/PRCCMBPSB_issues_dailyreport.csv")
        # with open(filename, 'w', encoding='utf-8') as csvfile:
        #     #csvfile.write('Running start date\tLab PI\tType\tUser Name\tYouTrack\tProject Name (YouTrack)\t# samples\tMS_Injections_Per_Sample\trun length (hours)\ttotal running time (hours)\tMass_Spectrometer\tCreated_DateH\tArrival_DateH\tMS_RunStateH\tMS_RunStatesH\tMS_RunStatesnrH\tre-runs/problems\tMS_RunStartH\tMS_RunStartsH\tMS_RunStartsnrH\tresolvedH\tResolvedDateH\tCleatedDate\n')
        #     csvfile.write('YouTrack_id,No_Samples,total_running_time,Mass_Spectrometer,State,Scheduling_State,Project_Name\n')
        #     i=0 
        #     for issue in PRCissues:
        #         # name of fields in issue
        #         indices = list()
        #         for attr_name, attr_type in issue._attribute_types.items():
        #             indices.append(attr_name)
        #         # YouTrack_id
        #         issueid=issue['id']
        #         # Project_name
        #         issuesummary=issue['summary']
        #         # No_Samples
        #         if 'No_Samples' in indices:
        #             issueNoSamples=str(issue['No_Samples'])
        #         else:
        #             issueNoSamples='None'
        #         # total running time (hours)
        #         if 'MS_Total_Time_h' in indices:
        #             issueMS_Total_Time_h=issue['MS_Total_Time_h']
        #         else:
        #             issueMS_Total_Time_h='None'
        #         # Mass_Spectrometer
        #         if 'Mass_Spectrometer' in indices:
        #             issueMassSpectrometer=issue['Mass_Spectrometer']
        #         else:
        #             issueMassSpectrometer='None'
        #         # State
        #         if 'State' in indices:
        #             issueState=issue['State']
        #         else:
        #             issueState='None'
        #         # Scheduling_State
        #         if 'Scheduling_State' in indices:
        #             issueSchedulingState=issue['Scheduling_State']
        #         else:
        #             issueSchedulingState='None'        
        #         row = issueid+','  + issueNoSamples+ ',' + issueMS_Total_Time_h + ',' + issueMassSpectrometer + "," + issueState + "," + issueSchedulingState + ',' + issuesummary
        #         row = row + '\n'
        #         csvfile.write(row,)
        #         i = i+1
        #     for issue in CMBissues:
        #         # name of fields in issue
        #         indices = list()
        #         for attr_name, attr_type in issue._attribute_types.items():
        #             indices.append(attr_name)
        #         # YouTrack_id
        #         issueid=issue['id']
        #         # Project_name
        #         issuesummary=issue['summary']
        #         # No_Samples
        #         if 'No_Samples' in indices:
        #             issueNoSamples=str(issue['No_Samples'])
        #         else:
        #             issueNoSamples='None'
        #         # total running time (hours)
        #         if 'MS_Total_Time_h' in indices:
        #             issueMS_Total_Time_h=issue['MS_Total_Time_h']
        #         else:
        #             issueMS_Total_Time_h='None'
        #         # Mass_Spectrometer
        #         if 'Mass_Spectrometer' in indices:
        #             issueMassSpectrometer=issue['Mass_Spectrometer']
        #         else:
        #             issueMassSpectrometer='None'
        #         # State
        #         if 'State' in indices:
        #             issueState=issue['State']
        #         else:
        #             issueState='None'
        #         # Scheduling_State
        #         if 'Scheduling_State' in indices:
        #             issueSchedulingState=issue['Scheduling_State']
        #         else:
        #             issueSchedulingState='None'        
        #         row = issueid + ',' + issueNoSamples+ ',' + issueMS_Total_Time_h + ',' + issueMassSpectrometer + "," + issueState + "," + issueSchedulingState+',' + issuesummary
        #         row = row + '\n'
        #         csvfile.write(row,)
        #         i = i+1
        #     for issue in PSBissues:
        #         # name of fields in issue
        #         indices = list()
        #         for attr_name, attr_type in issue._attribute_types.items():
        #             indices.append(attr_name)
        #         # YouTrack_id
        #         issueid=issue['id']
        #         # Project_name
        #         issuesummary=issue['summary']
        #         # No_Samples
        #         if 'No_Samples' in indices:
        #             issueNoSamples=str(issue['No_Samples'])
        #         else:
        #             issueNoSamples='None'
        #         # total running time (hours)
        #         if 'MS_Total_Time_h' in indices:
        #             issueMS_Total_Time_h=issue['MS_Total_Time_h']
        #         else:
        #             issueMS_Total_Time_h='None'
        #         # Mass_Spectrometer
        #         if 'Mass_Spectrometer' in indices:
        #             issueMassSpectrometer=issue['Mass_Spectrometer']
        #         else:
        #             issueMassSpectrometer='None'
        #         # State
        #         if 'State' in indices:
        #             issueState=issue['State']
        #         else:
        #             issueState='None'
        #         # Scheduling_State
        #         if 'Scheduling_State' in indices:
        #             issueSchedulingState=issue['Scheduling_State']
        #         else:
        #             issueSchedulingState='None'        
        #         row = issueid + ',' + issueNoSamples+ ',' + issueMS_Total_Time_h + ',' + issueMassSpectrometer + "," + issueState + "," + issueSchedulingState+',' + issuesummary
        #         row = row + '\n'
        #         csvfile.write(row,)
        #         i = i+1
        #     csvfile.close()

             
        # filename =os.path.join(settings.BASE_DIR, "static/MSSissues_issues_dailyreport.csv")
        # with open(filename, 'w', encoding='utf-8') as csvfile:
        #     #csvfile.write('Running start date\tLab PI\tType\tUser Name\tYouTrack\tProject Name (YouTrack)\t# samples\tMS_Injections_Per_Sample\trun length (hours)\ttotal running time (hours)\tMass_Spectrometer\tCreated_DateH\tArrival_DateH\tMS_RunStateH\tMS_RunStatesH\tMS_RunStatesnrH\tre-runs/problems\tMS_RunStartH\tMS_RunStartsH\tMS_RunStartsnrH\tresolvedH\tResolvedDateH\tCleatedDate\n')
        #     csvfile.write('Mass_Spectrometer,Status,Status_description\n')
        #         # name of fields in issue
        #     indices = list()
        #     rowlist=[None]*5
        #     MSindexed_lst = ['Orbitrap Fusion Lumos','Q-Exactive HF','Q-Exactive HF Biopharma', 'Q-Exactive','LTQ Orbitrap Elite']
        #     for attr_name, attr_type in issue._attribute_types.items():
        #         indices.append(attr_name)
        #     for i in range(5):
        #         # Mass Spectrometer
        #         issue = MSSissues[i]
        #         indices = list()
        #         for attr_name, attr_type in issue._attribute_types.items():
        #             indices.append(attr_name)
        #         issueMS=issue['Mass_Spectrometer']
        #         # MassSpec status
        #         issueStatus=issue['Status']
        #         # Status description
        #         if 'Status_description' in indices:
        #             issueStatusdescription=str(issue['Status_description']).lower()
        #         elif issueStatus == "On":
        #             issueStatusdescription='running'
        #         else:
        #             issueStatusdescription='under maintenance'
        #         row = issueMS + ',' + issueStatus + "," + issueStatusdescription
        #         row = row + '\n'
        #         rowlist[MSindexed_lst.index(issueMS)]=row
        #         #i = i+1
        #     for i in range(5):
        #         csvfile.write(rowlist[i])
        #     csvfile.close()
