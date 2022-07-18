import httpx
import json

def ytclient(baseurl):
    #client = httpx.Client(base_url="https://youtrack.cmb.ugent.be/api")#,
    client = httpx.Client(base_url=baseurl)#,
    
    return(client)

def prepareProjectIssuesDict(jsonObj):
    '''
    # get dictionary with fields&values
    '''
    print(jsonObj.keys())
    cfs = jsonObj['customFields']
    cfsdict = dict()
    cfsdict['id'] = jsonObj['id']
    cfsdict['idReadable'] = jsonObj['idReadable']
    cfsdict['summary'] = jsonObj['summary']
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
##    if cfsdict['State'] in ['Arrived', 'Sample_Prep',"MS_Run","Data_Analysis"]:
##        issuesdict[cfsdict['idReadable']] = cfsdict
    return(cfsdict)

def getissue(client,issueid,base_url,accesstok) :
    url = base_url+"issues/"+issueid
    headers = {'Authorization': 'Bearer {}'.format(accesstok),
           'content-type': 'application/json;charset=utf-8',
           'Accept': 'application/json;charset=utf-8'}
    params = {'fields':'id,idReadable,name,summary,description,customFields(id,name,value(fullName,id,isResolved,localizedName,name))'}
    PRCissuefields = client.get(url, params = params, headers = headers)
    PRCissuefieldsjson = PRCissuefields.json()
    currentissue= prepareProjectIssuesDict(PRCissuefieldsjson)
    return(currentissue)

def updateissuemainSG(client,issueid,base_url,accesstok,description,analysis) :
    url = base_url+"issues/"+issueid
    headers = {'Authorization': 'Bearer {}'.format(accesstok),
           'content-type': 'application/json;charset=utf-8',
           'Accept': 'application/json;charset=utf-8'}
    params = {'fields':'id,summary,description,customFields(id,name,value(fullName,id,isResolved,localizedName,name))'}    
    Contact_Person = analysis[0]['Name']
    GroupLeader = str(analysis[0]['Group_leader'])
    if analysis[0]['Affiliation'] == 'Industry':
        Study_Type ="Non-Academic" #+ str(analysis[0]['Affiliation_Type']) )
    elif analysis[0]['Affiliation'].find('VIB') != -1:
        Study_Type = "VIB" #+ str(analysis[0]['Affiliation_Type']) )
    else:
        Study_Type ="Academic" #+ str(analysis[0]['Affiliation_Type']) )
    ### to be commented #######################
##    yt.update_issue(Project_ID, summary = "ContactPerson-GroupLeader-analysistype-keyword1",
##            description=description)
    No_Samples = int(str(analysis[3]['Nb_samples']))
    Project_Title = analysis[1]['Project_title']
    data={'description': description,
     'customFields':[{'name':'GroupLeader','$type':'SimpleIssueCustomField','value': GroupLeader},
                     {'name':'Contact_Person','$type':'SimpleIssueCustomField','value': Contact_Person},
                     {'name':'Study_Type','$type':'SingleEnumIssueCustomField','value':{'name': Study_Type}},
                     {'name':'No_Samples','$type':'SimpleIssueCustomField','value': No_Samples},
                     {'name':'Project_Title','$type':'SimpleIssueCustomField','value': Project_Title}]}
    # data={'description': description,
    #       'customFields':[{'name':'GroupLeader','$type':'SimpleIssueCustomField','value':'133'},
    #                       {'name':'Contact_Person','$type':'SimpleIssueCustomField','value':'george'},
    #                       {'name':'Study_Type','$type':'SingleEnumIssueCustomField','value':{'name':'VIB'}},
    #                       {'name':'No_Samples','$type':'SimpleIssueCustomField','value':10},
    #                       {'name':'Project_Title','$type':'SimpleIssueCustomField','value':'sdada QHO'}]}

    responsemain = client.post(url, data= json.dumps(data), params = params,
                        headers = headers)
    return(responsemain)

def updateissuemainPMD(client,issueid,base_url,accesstok,description,analysis) :
    url = base_url+"issues/"+issueid
    headers = {'Authorization': 'Bearer {}'.format(accesstok),
           'content-type': 'application/json;charset=utf-8',
           'Accept': 'application/json;charset=utf-8'}
    params = {'fields':'id,summary,description,customFields(id,name,value(fullName,id,isResolved,localizedName,name))'}    
    Contact_Person = analysis[0]['Name']
    GroupLeader = str(analysis[0]['Group_leader'])
    if analysis[0]['Affiliation'] == 'Industry':
        Study_Type ="Non-Academic" #+ str(analysis[0]['Affiliation_Type']) )
    elif analysis[0]['Affiliation'].find('VIB') != -1:
        Study_Type = "VIB" #+ str(analysis[0]['Affiliation_Type']) )
    else:
        Study_Type ="Academic" #+ str(analysis[0]['Affiliation_Type']) )
    ### to be commented #######################
##    yt.update_issue(Project_ID, summary = "ContactPerson-GroupLeader-analysistype-keyword1",
##            description=description)
    No_Samples = int(str(analysis[2]['Nb_samples']))
    Project_Title = analysis[1]['Project_title']
    MS = 'LTQ Orbitrap XL'
    data={'description': description,
     'customFields':[{'name':'GroupLeader','$type':'SimpleIssueCustomField','value': GroupLeader},
                     {'name':'Contact_Person','$type':'SimpleIssueCustomField','value': Contact_Person},
                     {'name':'Study_Type','$type':'SingleEnumIssueCustomField','value':{'name': Study_Type}},
                     {'name':'No_Samples','$type':'SimpleIssueCustomField','value': No_Samples},
                     {'name':'Project_Title','$type':'SimpleIssueCustomField','value': Project_Title},
                     {'name':'SamplePrep_Responsible','$type':'SingleEnumIssueCustomField','value': {'name':'Hans'}},
                     {'name':'DataAnalysis_Responsible','$type':'SingleEnumIssueCustomField','value': {'name':'Hans'}},
                     {'name':'Mass_Spectrometer','$type':'SingleEnumIssueCustomField','value':{'name': MS}},
                     {'name':'Run_Length_h','$type':'SingleEnumIssueCustomField','value':{'name':'15_min'}}]}
    # data={'description': description,
    #       'customFields':[{'name':'GroupLeader','$type':'SimpleIssueCustomField','value':'133'},
    #                       {'name':'Contact_Person','$type':'SimpleIssueCustomField','value':'george'},
    #                       {'name':'Study_Type','$type':'SingleEnumIssueCustomField','value':{'name':'VIB'}},
    #                       {'name':'No_Samples','$type':'SimpleIssueCustomField','value':10},
    #                       {'name':'Project_Title','$type':'SimpleIssueCustomField','value':'sdada QHO'}]}

    responsemain = client.post(url, data= json.dumps(data), params = params,
                        headers = headers)
    return(responsemain)
            # yt.execute_command(Project_ID, "SamplePrep_Responsible Hans")
            # yt.execute_command(Project_ID, "DataAnalysis_Responsible Hans")
            # yt.execute_command(Project_ID, "Mass_Spectrometer LTQ Orbitrap XL")
            # yt.execute_command(Project_ID, "Run_Length_h 15_min")

def updateissuetagsSG(client,issueid,base_url,accesstok,analysis) :
    url = base_url+"commands"
    params = {'fields':'tags(id,name)'}
    headers = {'Authorization': 'Bearer {}'.format(accesstok),
           'content-type': 'application/json;charset=utf-8',
           'Accept': 'application/json;charset=utf-8'}
    params = {'fields':'tags(id,name)'}
    if analysis[1]['Sample_preparation']:
        #print("sp")
        data = {
        'query':'tag nSP', 
        'issues':[{'idReadable':issueid}]
        }
        responseSP = client.post(url, data= json.dumps(data), params = params,
                        headers = headers)
         #yt.execute_command(Project_ID, "tag nSP")
    if analysis[1]['Data_analysis']:
        #print("da")
        data = {
        'query':'tag nDA', 
        'issues':[{'idReadable':issueid}]
        }
        responseDA = client.post(url, data= json.dumps(data), params = params,
                        headers = headers)
    #print(issueid)
    try:
        if analysis[3]['Isotopic_labeling_details'] is not None:
            Isotopic_labeling_details = analysis[3]['Isotopic_labeling_details']
            if 'tmt' in Isotopic_labeling_details.lower():
                #print("tmt")
                tagTMT=True
                data = {
                    'query':'tag TMT',
                    'issues':[{'idReadable':issueid}]
                    }
                responseTMT = client.post(url, data= json.dumps(data), params = params,
                            headers = headers)
    except KeyError:
        Other_information = analysis[3]['Other_information']
        data = {
            'query':'tag TMT',
            'issues':[{'idReadable':issueid}]
            }
        if 'tmt' in Other_information.lower():
            responseTMT = client.post(url, data= json.dumps(data), params = params,
                            headers = headers)

    if 'PTM' in analysis[2].keys():
        print('PTM')
        data = {
        'query':'tag PTM',
        'issues':[{'idReadable':issueid}]
        }
        responsePTM = client.post(url, data= json.dumps(data), params = params,
                headers = headers)
    #return(responseDA)

def updateissueattachmentsSG(client,issueid,base_url,accesstok, analysis, sdbf,sdbfg) :
    url = base_url+"issues/"+issueid +"/attachments" 
    headers = {'Authorization': 'Bearer {}'.format(accesstok),
           'vary': 'Accept-Encoding, User-Agent'}
    params = {'fields':'id,name,author(id,name),mymeType', 'muteUpdateNotification':True}
    EDfile = [('upload-file',analysis[4]['EDfile'],)]
    #EDfile = [('upload-file',open('/home/pportal/Downloads/Experimental_design.xlsx','rb'),)]
    EDissuerequest = client.post(url, params = params, headers = headers, files=EDfile)
    if sdbf:
        try:
            DBfile = [('upload-file',analysis[2]['Sequence_database_file'],)]
            DBissuerequest = client.post(url, params = params, headers = headers, files=DBfile)
        except KeyError:
            DBfile = [('upload-file',analysis[2]['Bait_sequence_file'],)]
            #DBfile = [('upload-file',analysis[2]['Sequence_database_file'],)]
            #DBfile = [('upload-file',open('/home/pportal/Downloads/Sequence_database_file.fasta','r'),)]
            DBissuerequest = client.post(url, params = params, headers = headers, files=DBfile)
    if sdbfg:
        Gelfile = [('upload-file',analysis[2]['Gel_file'],)]
        #DBfile = [('upload-file',open('/home/pportal/Downloads/Sequence_database_file.fasta','r'),)]
        Gelissuerequest = client.post(url, params = params, headers = headers, files=Gelfile)       
    return(EDissuerequest)
        #yt.create_attachment(Project_ID,name=Sequence_database_file,content=analysis[2]['Sequence_database_file'],author_login ="root", group="PRC-team") 
    #yt.create_attachment(Project_ID,name=str(analysis[4]['EDfile']),content=analysis[4]['EDfile'],author_login ="root", group="PRC-team" ) 

    #return(currentissue)

def updateissuetagsPMD(client,issueid,base_url,accesstok,analysis) :
    url = base_url+"commands"
    params = {'fields':'tags(id,name)'}
    headers = {'Authorization': 'Bearer {}'.format(accesstok),
           'content-type': 'application/json;charset=utf-8',
           'Accept': 'application/json;charset=utf-8'}
    params = {'fields':'tags(id,name)'}
    if analysis[1]['Sample_preparation']:
        #print("sp")
        data = {
        'query':'tag nSP', 
        'issues':[{'idReadable':issueid}]
        }
        responseSP = client.post(url, data= json.dumps(data), params = params,
                        headers = headers)
         #yt.execute_command(Project_ID, "tag nSP")
    if analysis[1]['Data_analysis']:
        #print("da")
        data = {
        'query':'tag nDA', 
        'issues':[{'idReadable':issueid}]
        }
        responseDA = client.post(url, data= json.dumps(data), params = params,
                        headers = headers)
    #print(issueid)
    # try:
    #     if analysis[3]['Isotopic_labeling_details'] is not None:
    #         Isotopic_labeling_details = analysis[3]['Isotopic_labeling_details']
    #         if 'tmt' in Isotopic_labeling_details.lower():
    #             #print("tmt")
    #             tagTMT=True
    #             data = {
    #                 'query':'tag TMT',
    #                 'issues':[{'idReadable':issueid}]
    #                 }
    #             responseTMT = client.post(url, data= json.dumps(data), params = params,
    #                         headers = headers)
    # except KeyError:
    #     Other_information = analysis[2]['Other_information']
    #     data = {
    #         'query':'tag TMT',
    #         'issues':[{'idReadable':issueid}]
    #         }
    #     if 'tmt' in Other_information.lower():
    #         responseTMT = client.post(url, data= json.dumps(data), params = params,
    #                         headers = headers)

    if 'PTM' in analysis[2].keys():
        print('PTM')
        data = {
        'query':'tag PTM',
        'issues':[{'idReadable':issueid}]
        }
        responsePTM = client.post(url, data= json.dumps(data), params = params,
                headers = headers)
    #return(responseDA)

def updateissueattachmentsPMD(client,issueid,base_url,accesstok, analysis, sdbf,sdbfg) :
    url = base_url+"issues/"+issueid +"/attachments" 
    headers = {'Authorization': 'Bearer {}'.format(accesstok),
           'vary': 'Accept-Encoding, User-Agent'}
    params = {'fields':'id,name,author(id,name),mymeType', 'muteUpdateNotification':True}
    EDfile = [('upload-file',analysis[3]['EDfile'],)]
    #EDfile = [('upload-file',open('/home/pportal/Downloads/Experimental_design.xlsx','rb'),)]
    EDissuerequest = client.post(url, params = params, headers = headers, files=EDfile)
    # if sdbf:
    #     try:
    #         DBfile = [('upload-file',analysis[2]['Sequence_database_file'],)]
    #         DBissuerequest = client.post(url, params = params, headers = headers, files=DBfile)
    #     except KeyError:
    #         DBfile = [('upload-file',analysis[2]['Bait_sequence_file'],)]
    #         #DBfile = [('upload-file',analysis[2]['Sequence_database_file'],)]
    #         #DBfile = [('upload-file',open('/home/pportal/Downloads/Sequence_database_file.fasta','r'),)]
    #         DBissuerequest = client.post(url, params = params, headers = headers, files=DBfile)
    # if sdbfg:
    #     Gelfile = [('upload-file',analysis[2]['Gel_file'],)]
    #     #DBfile = [('upload-file',open('/home/pportal/Downloads/Sequence_database_file.fasta','r'),)]
    #     Gelissuerequest = client.post(url, params = params, headers = headers, files=Gelfile)       
    return(EDissuerequest)
        #yt.create_attachment(Project_ID,name=Sequence_database_file,content=analysis[2]['Sequence_database_file'],author_login ="root", group="PRC-team") 
    #yt.create_attachment(Project_ID,name=str(analysis[4]['EDfile']),content=analysis[4]['EDfile'],author_login ="root", group="PRC-team" ) 

    #return(currentissue)