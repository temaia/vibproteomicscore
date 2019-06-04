# coding=UTF-8

#from youtrack.connection import Connection, httplib2
from youtrack.connection import Connection, httplib2
#from connection import Connection, httplib2
from xml.etree.ElementTree import fromstring
import random
import urllib
#import httplib
#import urllib2

#import socks
import csv
import re
import time
import datetime

httplib2.debuglevel=4
#httplib.debuglevel=4
# connection
yt = Connection('https://youtrack.ugent.be', 'root', 'PRCyt,17*')#, proxy_info = httplib2.ProxyInfo(socks.PROXY_TYPE_HTTP, 'youtrack.ugent.be', 8080))
 
print('connected')

# get CMB issues
PRCissues = yt.get_all_issues("PRC-",0,500)
#datetime.datetime.now()-datetime.datetime.fromtimestamp(int(issue['created'])<datetime.timedelta(minutes=40)
#datetime.datetime.fromtimestamp(int(PRCissues[0]['created'])/1000).strftime('%Y-%m-%d %H:%M:%S.%f')
# issue IDs per project

# open PRC issue IDs
PRCissuesIDs = []
Currentissuesindexes = list()
counter=0
for issue in PRCissues:
    if datetime.datetime.now() - datetime.datetime.fromtimestamp(int(issue["created"])/1000)<datetime.timedelta(hours=4):
        PRCissuesIDs.append(issue["id"])
        Currentissuesindexes.append(counter)
    counter = counter+1
# update PRCissues (filter State Closed)
PRCissues = [PRCissues[index] for index in Currentissuesindexes]
##    
##
##    
### function to handle inhesistent attributes    
##def find_attribute_in_list(element, list_element):
##    try:
##        index_element = list_element.index(element)
##        return index_element
##    except ValueError:
##        return 'None'
#filename ="/home/pportal/dev2Sep18/prcsite/PRC_issues_creation_hourly.csv"
filename ="/usr/local/www/apache24/data/PRCsite/vibproteomicscore/static/PRC_issues_creation_hourly.csv"      
with open(filename, 'w', encoding='utf-8') as csvfile:
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
    #csvfile.close()            
        
