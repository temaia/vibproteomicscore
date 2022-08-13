#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8

#####from django.core.urlresolvers import reverse
import json
from django.urls import reverse
from django.conf import settings
from utils.utils import prepareProjectIssuesDict,getissue,updateissuemainSG,updateissuetagsSG,updateissueattachmentsSG,updateissuemainPMD,updateissuetagsPMD,updateissueattachmentsPMD
from utils.utils import youtrack_get,youtrackurl_get,ytclient
import httpx
import urllib
import json
import pandas as pd
import os
#from youtrack.connection import Connection
from .acessorio import *

from django.contrib.auth import get_user
from django.contrib.auth.views import PasswordContextMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.http import is_safe_url
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, FormView, ListView,RedirectView
from django.views.generic.detail import SingleObjectMixin 
from django.views.generic.base import TemplateResponseMixin
from django.contrib.auth import authenticate, login, logout
#from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import User,Profile, Analysis
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm,
)
from django.forms.models import construct_instance 

from .forms import AnalysisForm,LoginForm, CustomerForm#,PasswordResetForm
from .forms import Specimen_APMSForm, Specimen_SGForm,Specimen_PTMForm,EDPMDForm, Specimen_GBForm, ExperimentForm,ExperimentPMDForm,ExperimentPTMForm,ExperimentAPMSForm,ExperimentGBForm, EDForm,TOUForm
from formtools.wizard.views import SessionWizardView
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from .excel_utils import WriteToExcel
from .excel_utilsapms import WriteToExcel2
from .excel_utilsgb import WriteToExcel3
from .excel_utilspmd import WriteToExcel4
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.mail import EmailMessage
#import logging
#logr=logging.getlogger(__name__)
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.tokens import default_token_generator
import os
import sys
#sys.path.insert(0, '/home/pportal/dev2/src/lib/python2.7/site-packages/youtrack/')
# authenticating
import http.client, urllib.request, urllib.error

#from youtrack import connection
import csv
#import logging
##logr=logging.getlogger(__name__)

from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings

class LoginView(FormView):
    form_class=LoginForm
    success_url = '/'
    template_name = 'login.html'
	# def login_page(request):
	# 	if request.method =='POST':
	# 		email=form.cleaned_data.get('email')
	# 		password=form.cleaned_data.get('password')
	# 		user = authenticate(username=email,password=password)
 #    		if user is not None:
 #    			login(request, user)
 #    			return HttpResponse('Signed in')
 #    		else:
 #    			return HttpResponse('Not signed in')
 #    	else:
 #    		return super(LoginView, self).form_invalid(form)
    def form_valid(self,form):
        request=self.request
        next_=request.GET.get('next')
        print(next_)
        next_post=request.POST.get('next')
        print(next_post)
        redirect_path = next_ or next_post or None
        username=form.cleaned_data.get('username')
        password=form.cleaned_data.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request, user)
            try:
                del request.session['guest_email_id']
            except:
                pass
            #return redirect(redirect_path)
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect("/")
        else:
            # return 'invalid login' 
            print ("Error") 
            return super(LoginView, self).form_invalid(form) 
        return render(request, "login") 
	# def form_valid(self,form):
	# 	request=self.request
	# 	next_=request.GET.get('/login')
	# 	next_post=request.POST.get('/profile')
	# 	redirect_path = next_ or next_post or None
	# 	email=form.cleaned_data.get('email')
	# 	password=form.cleaned_data.get('password')
	# 	user = authenticate(request,username=email,password=password)
	# 	if user.profile.Main_Analysis_Type is not None:
	# 		login(request, user)
	# 		return redirect('/profile')
	# 	else:
	# 		if is_safe_url(redirect_path, request.get_host()):
	# 			return redirect('/home')
	# 		else:
	# 			return redirect("/login")
	# 	return super(LoginView, self).form_invalid(form)  


class LogoutView(TemplateView):
    """
    A view that logout user and redirect to homepage.
    """
    permanent = False
    query_string = True
    pattern_name = 'home'

    def get_redirect_url(self, *args, **kwargs):
        """
        Logout user and redirect to target url.
        """
        if self.request.user.is_authenticated:
            print("logged in")
            logout(self.request)
        #else:
        return super(LogoutView, self).get_redirect_url(*args, **kwargs)
# def login_page(request):
# 	if user is not None:
# 		login(request,user)
# 		try:
# 			del request.session

#@login_required
#@transaction.atomic


# class PasswordResetView(PasswordContextMixin, FormView):
#     email_template_name = 'registration/password_reset_email.html'
#     extra_email_context = None
#     form_class = PasswordResetForm
#     from_email = None
#     html_email_template_name = None
#     subject_template_name = 'registration/password_reset_subject.txt'
#     success_url = reverse_lazy('password_reset_done')
#     template_name = 'registration/password_reset_form.html'
#     title = ('Password reset')
#     token_generator = default_token_generator

#     @method_decorator(csrf_protect)
#     def dispatch(self, *args, **kwargs):
#         return super().dispatch(*args, **kwargs)

#     def form_valid(self, form):
#         opts = {
#             'use_https': self.request.is_secure(),
#             'token_generator': self.token_generator,
#             'from_email': self.from_email,
#             'email_template_name': self.email_template_name,
#             'subject_template_name': self.subject_template_name,
#             'request': self.request,
#             'html_email_template_name': self.html_email_template_name,
#             'extra_email_context': self.extra_email_context,
#         }
#         form.save(**opts)
#         return super().form_valid(form)


# INTERNAL_RESET_URL_TOKEN = 'set-password'
# INTERNAL_RESET_SESSION_TOKEN = '_password_reset_token'


def index(request):
    return HttpResponse('Index page')


def maintenance(request):
    return render(request, 'maintenance.html')


#cleaned_data = wizard.get_cleaned_data_for_step('paytype') or {'method': 'none'}


FORMS = [("0", CustomerForm),
            ("1", CustomerForm),
         ("2", CustomerForm),
         ("3",CustomerForm),#,
          ("4",CustomerForm),#,
         ("5", TOUForm)]

TEMPLATES = {"0": "project-regis0.html",
             "1": "project-regis0.html",
             "2": "project-regis0.html",
             "3": "project-regis0.html",
             "4": "project-regis0.html",
             "5": "project-regis0.html"}#,
             #"4": "project-regis0.html"}

FORMSSG= [("0", CustomerForm),
            ("1", AnalysisForm),
         ("2", Specimen_SGForm),
         ("3",ExperimentForm),
         ("4", EDForm),
         ("5", TOUForm)]

TEMPLATESSG = {"0": "project-regis111.html",
             "1": "project-regis222.html",
             "2": "project-regis333.html",
             "3": "project-regis444.html",
             "4": "project-regis555.html",
             "5": "project-regis666.html"}

FORMSPMD= [("0", CustomerForm),
            ("1", AnalysisForm),
         #("2", Specimen_PMDForm),
         ("2",ExperimentPMDForm),
         ("3", EDPMDForm),
         ("4", TOUForm)]

TEMPLATESPMD = {"0": "project-regis111.html",
             "1": "project-regis222.html",
            # "2": "project-regis333PMD.html",
             "2": "project-regis444PMD.html",
             "3": "project-regis555PMD.html",
             "4": "project-regis666.html"}

# TEMPLATESSG = {"0": "project-regis111.html",
#              "1": "project-regis222.html",
#              "2": "project-regis333.html",
#              "3": "project-regis444.html",
#              "4": "project-regis555.html",
#              "5": "project-regis666.html"}

# TEMPLATESSG = {"0": "project-regis11.html",
#               "1": "project-regis22.html",
#               "2": "project-regis33.html",
#               "3": "project-regis44.html",
#               "4": "project-regis55.html"}

FORMSPTM = [("0", CustomerForm),
            ("1", AnalysisForm),
         ("2", Specimen_PTMForm),
         ("3",ExperimentPTMForm),
         ("4", EDForm),
          ("5", TOUForm)]

TEMPLATESPTM = {"0": "project-regis111.html",
             "1": "project-regis222.html",
             "2": "project-regis333PTM.html",
             "3": "project-regis44PTM.html",
             "4": "project-regis555.html",
             "5": "project-regis666.html"}

FORMSAPMS = [("0", CustomerForm),
            ("1", AnalysisForm),
         ("2", Specimen_APMSForm),
         ("3",ExperimentAPMSForm),
         ("4", EDForm),
          ("5", TOUForm)]

TEMPLATESAPMS = {"0": "project-regis111.html",
             "1": "project-regis222.html",
             "2": "project-regis333APMS.html",
             "3": "project-regis44APMS.html",
             "4": "project-regis555.html",
             "5": "project-regis666.html"}

FORMSGB= [("0", CustomerForm),
            ("1", AnalysisForm),
         ("2", Specimen_GBForm),
         ("3",ExperimentGBForm),
         ("4", EDForm),
          ("5", TOUForm)]

TEMPLATESGB = {"0": "project-regis111.html",
             "1": "project-regis222.html",
             "2": "project-regis3333GB.html",
             "3": "project-regis444.html",
             "4": "project-regis555.html",
             "5": "project-regis666.html"}

          

class ContactWizard(SessionWizardView):

    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT,'dbs'))
    #form_list = 
    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]
    # def done(self, form_list,form_dict, **kwargs):
    #     analysis = [form.cleaned_data for form in form_list]
    #     # file field
    #     print(type(form_list))
    #     upload_file = form_list[2].cleaned_data['Nb_samples']
    #     yt = Connection(url=youtrackurl_get(), token=youtrack_get()) #@
    #     #yt = connection.Connection(url='https://youtrack.ugent.be', api_key='perm:cHJjc2l0ZQ==.cHJjc2l0ZS10b2s=.XCNRP5yqauYkjFiFzj2VGYybpS3DJy')
    #     yt.execute_command("PRC-321", "No_Samples 19", group="PRC-website")
    #     return render(self.request,'done.html',{
    #         'form_data': analysis[0],
    #         'analysisd':form_dict,
    #         'upload_file' : upload_file,
    #         })
    def get_form_initial(self, step):
        """
        Set projet id and email for step1
        Set extra parameter for step2, which is from clean data of step1.
        """
        initial = self.initial_dict.get(step, {})
        #if step == '3':
         #   form_class = self.form_list[step]
            #initial.update({'Sample_Name':Analysis_Type})
          #  return initial
        if step == '4':
            form_class = self.form_list[step]
            prev_data = self.storage.get_step_data('1')
            samplename = prev_data.get('Project_ID','')
            #return samplename
            return self.initial_dict.get(step, {samplename:'samplename'})
     

class ContactWizardSG(SessionWizardView):
    instance=None
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT,'seqdbs'))
    def get_template_names(self):
        return [TEMPLATESSG[self.steps.current]]

    def done(self, form_list,form_dict, **kwargs):
        analysis = [form.cleaned_data for form in form_list]
        userid = get_user(self.request)
        customer,created = Profile.objects.update_or_create(user_id=self.request.user, defaults=analysis[0])
        analise,created = Analysis.objects.update_or_create(user_id=userid.id, defaults=analysis[1])
        # file field
        formtitles = ["User details", "Analysis overview", "Sample information", "Experimental Design information",
        "Experimental Design and Sample details", "Terms of Use"]
        formdict=dict()
        for i in range(len(formtitles)):
            formdict[formtitles[i]]=analysis[i]
        print('formdict' + str(formdict))
        Project_ID = analysis[0]['Project_ID']
        Contact_Person = analysis[0]['Name'].split(',')[0]
        # #### BLOCKSG1 ##### to be commented
        # yt = Connection(url=youtrackurl_get(), token=youtrack_get()) #@
        # # check whether to go ahead or to return a page saying the project has already been registered
        # currentissue = yt.get_issue(Project_ID)
        ##### BLOCKSG1 ######
        # NEW BLOCK 1

        YTTOKR = youtrack_get()
        client = ytclient(youtrackurl_get())
        currentissue = getissue(client,Project_ID,str(client.base_url),YTTOKR)
        print(currentissue.keys())
        ProjectTitle = currentissue['Project_Title']
        if ProjectTitle is None:
            ProjectTitle = 'noprojecttitle'
        # try:
        #     ProjectTitle = currentissue['Project_Title']
        # except KeyError:
            # ProjectTitle = 'noprojecttitle'
        if ProjectTitle == 'noprojecttitle' or currentissue['OverwriteRegistration'] == 'Yes': 
            summary = analysis[0]['Project_ID']# + "-" +  + "-" + Analysis_Type + "-" + keywords[0]
            if analysis[0]['VIBAffiliation'] is not None:
              VIBAffiliation = analysis[0]['VIBAffiliation']
            else:
              VIBAffiliation = ''
            if analysis[0]['Other_institution'] is not None:
              Other_institution = analysis[0]['Other_institution']
            else:
              Other_institution = ''
            sdbfg = False
            if analysis[2]['Sequence_database_name'] is not None:
              Sequence_database_name = analysis[2]['Sequence_database_name']
            else:
              Sequence_database_name = ''
            sdbf = False
            if analysis[2]['Sequence_database_file'] is not None:
              sdbf = True
              Sequence_database_file= analysis[2]['Sequence_database_file']
            else:
              Sequence_database_file = ''
            if analysis[2]['Buffer_composition'] is not None:
              Buffer_composition= analysis[2]['Buffer_composition']
            else:
              Buffer_composition = ''
            if analysis[3]['Isotopic_labeling_details'] is not None:
              Isotopic_labeling_details = analysis[3]['Isotopic_labeling_details']
            else:
              Isotopic_labeling_details = ''
            if analysis[3]['Other_information'] is not None:
              Other_information = analysis[3]['Other_information']
            else:
              Other_information = ''
            description = "# Sample Preparation notes\nProtocol: \nOther notes:\n"\
 + "\n# User Details\nInstitute/Organization: " + str(analysis[0]['Affiliation']) + "\nVIB Affiliation: " +VIBAffiliation + "\nOther institution" +Other_institution + "\nAddress: " + analysis[0]['Address']+ "\nPhone nr: " + analysis[0]['Phone'] + "\n\n# Analysis overview\nExperiment Summary: " + analysis[1]['Project_summary']+"\nProject_title: " + analysis[1]['Project_title'] + "\nData_Analysis: "+ str(analysis[1]['Data_analysis']) + "\n\n# Sample information" \
                  + "\nSample_Species: "+ analysis[2]['Species'] + '\nSequence_Database_Public_Availability: ' + str(analysis[2]['Sequence_Database_Public_Availability']) \
                  + "\nSequence_Database_Name: " + Sequence_database_name+"\nSequence_database_file: " + str(Sequence_database_file) + "\nSample_Type:" + analysis[2]['Sample_Type']  + "\nBuffer_composition:" + Buffer_composition + "\n\n# Experimental Design information\nConditions_to_compare: " + analysis[3]['Conditions_to_compare'] +"\nIsotopic labeling: " + str(analysis[3]['Isotopic_labeling'])+ "\nIsotopic labeling details: " + Isotopic_labeling_details + "\nOther information: " \
                  + Other_information
            ### BLOCKSG2 to be commented #######################
            # yt.update_issue(Project_ID, summary = "ContactPerson-GroupLeader-analysistype-keyword1",
            #         description=description)
            # yt.execute_command(Project_ID, "Contact_Person " + analysis[0]['Name'])
            # yt.execute_command(Project_ID, "GroupLeader "+ str(analysis[0]['Group_leader']  ))
            # if analysis[0]['Affiliation'] == 'Industry':
            #     yt.execute_command(Project_ID, "Study_Type Non-Academic") #+ str(analysis[0]['Affiliation_Type']) )
            # elif analysis[0]['Affiliation'].find("VIB") != -1:
            #     yt.execute_command(Project_ID, "Study_Type VIB") #+ str(analysis[0]['Affiliation_Type']) )
            # else:
            #     yt.execute_command(Project_ID, "Study_Type Academic") #+ str(analysis[0]['Affiliation_Type']) )
            # yt.execute_command(Project_ID, "No_Samples "+ str(analysis[3]['Nb_samples']))
            # yt.execute_command(Project_ID, "Project_Title "+ analysis[1]['Project_title'])
            # NEW BLOCK2
            # set main fields
            responsemain = updateissuemainSG(client,Project_ID,str(client.base_url),YTTOKR,description,analysis)
            print(responsemain.status_code)
            # NEW BLOCK3
            # if analysis[1]['Sample_preparation']:
            #      yt.execute_command(Project_ID, "tag nSP")
            # if analysis[1]['Data_analysis']:
            #      yt.execute_command(Project_ID, "tag nDA")
            # if 'tmt' in Isotopic_labeling_details.lower():
            #     yt.execute_command(Project_ID, "tag TMT")
            #base_url=str(client.base_url)
            #url = base_url+"commands"
            #accesstok=YTTOKR
            # print(url)
            # params = {'fields':'tags(id,name)'}
            # headers = {'Authorization': 'Bearer {}'.format(accesstok),
            #        'content-type': 'application/json;charset=utf-8',
            #        'Accept': 'application/json;charset=utf-8'}
            # issueid = Project_ID
            # if analysis[1]['Sample_preparation']:
            #     print("sp")
            #     data = {
            #     'query':'tag nSP', 
            #     'issues':[{'idReadable': Project_ID}]
            #     }
            #     responseSP = client.post(url, data= json.dumps(data), params = params,
            #                     headers = headers)
            #      #yt.execute_command(Project_ID, "tag nSP")
            # if analysis[1]['Data_analysis']:
            #     print("da")
            #     data = {
            #     'query':'tag nDA', 
            #     'issues':[{'idReadable': Project_ID}]
            #     }
            #     responseDA = client.post(url, data= json.dumps(data), params = params,
            #                     headers = headers)
            # if analysis[3]['Isotopic_labeling_details'] is not None:
            #     Isotopic_labeling_details = analysis[3]['Isotopic_labeling_details']
            #     if 'tmt' in Isotopic_labeling_details.lower():
            #         print("tmt")
            #         tagTMT=True
            #     data = {
            #     'query':'tag tmt', 
            #     'issues':[{'idReadable': Project_ID}]
            #     }
            responsetags = updateissuetagsSG(client,Project_ID,str(client.base_url),YTTOKR,analysis)
            #print(responsetags.status_code)
            # NEW BLOCK4
            # if sdbf:
            #     yt.create_attachment(Project_ID,name=Sequence_database_file,content=analysis[2]['Sequence_database_file'],author_login ="root", group="PRC-team") 
            # yt.create_attachment(Project_ID,name=str(analysis[4]['EDfile']),content=analysis[4]['EDfile'],author_login ="root", group="PRC-team" ) 
            attachmentsrequest = updateissueattachmentsSG(client,Project_ID,str(client.base_url),YTTOKR, analysis, sdbf, sdbfg)
            print(attachmentsrequest.status_code)
            ### BLOCKSG2 ######################################
            # send project registration confirmation email
            subject = 'VIB Proteomics Core, Project registration confirmation - Read carefully'
            html_message = render_to_string('confirmation_email.html', {'formdict': formdict,'Project_ID': Project_ID,'Contact_Person': Contact_Person})
            from_email=settings.EMAIL_HOST_USER
            to_list = [self.request.user.email]
            bcc = [settings.ADMINS[0][1],settings.ADMINS[1][1]]
            msg=EmailMessage(subject, html_message, from_email, to_list, bcc)
            msg.content_subtype = "html"
            msg.attach_file(os.path.join(settings.BASE_DIR,'static/TermsofUse_VIBProteomicsCore.pdf'))
            msg.attach_file(os.path.join(settings.BASE_DIR,'static/documents/Sender_Receiver_information.docx'))
            msg.send()
            return render(self.request,'done.html',{
                'formdict': formdict,

                })
        else:
            return render(self.request,'done4ar.html',{
                'formdict': formdict,

                })

    def get_form_initial(self, step):
        """
        Set projet id and email for step1
        Set extra parameter for step2, which is from clean data of step1.
        """
        initial = self.initial_dict.get(step, {})
        if step=='0':
            form_class=self.form_list[step]
            Project_ID = self.request.user.username
            Email = self.request.user.email
            initial.update({'Project_ID':Project_ID, 'Email':Email})
            return initial
        if step=='1':
            form_class=self.form_list[step]
            Main_analysis_type = self.request.user.Main_analysis_type
            #Analysis_Type = self.request.user.profile.Main_Analysis_Type
            initial.update({'Main_analysis_type':Main_analysis_type})
            return initial
        if step == '4':
            form_class = self.form_list[step]
            prev_data2 = self.storage.get_step_data('2')
            prev_data3 = self.storage.get_step_data('3')
            prev_data = {**prev_data2, **prev_data3}
            prev_data["PID"] = str(self.request.user.username)
            xlsx_data = WriteToExcel(prev_data)
            return self.initial_dict.get(step, prev_data)

class ContactWizardPMD(SessionWizardView):
    instance=None
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT,'seqdbs'))
    def get_template_names(self):
        #return [TEMPLATESSG[self.steps.current]]
        return [TEMPLATESPMD[self.steps.current]]

    def done(self, form_list,form_dict, **kwargs):
        analysis = [form.cleaned_data for form in form_list]
        userid = get_user(self.request)
        customer,created = Profile.objects.update_or_create(user_id=self.request.user, defaults=analysis[0])
        analise,created = Analysis.objects.update_or_create(user_id=userid.id, defaults=analysis[1])
        # file field
        formtitles = ["User details", "Analysis overview", "Experiment information", 
        "Sample details", "Terms of Use"]
        formdict=dict()
        for i in range(len(formtitles)):
            formdict[formtitles[i]]=analysis[i]
        print('formdict' + str(formdict))
        Project_ID = analysis[0]['Project_ID']
        Contact_Person = analysis[0]['Name'].split(',')[0]
        # yt = Connection(url=youtrackurl_get(), token=youtrack_get()) #@
        # # check whether to go ahead or to return a page saying the project has already been registered
        # currentissue = yt.get_issue(Project_ID)
        # try:
        #     ProjectTitle = currentissue['Project_Title']
        # except KeyError:
        #     ProjectTitle = 'noprojecttitle'
        # if ProjectTitle == 'noprojecttitle' or currentissue['OverwriteRegistration'] == 'Yes': 
        #     summary = analysis[0]['Project_ID']# + "-" +  + "-" + Analysis_Type + "-" + keywords[0]
        #     if analysis[0]['VIBAffiliation'] is not None:
        #       VIBAffiliation = analysis[0]['VIBAffiliation']
        #     else:
        #       VIBAffiliation = ''
        #     #try:
        #     if analysis[0]['Other_institution'] is not None:
        #       Other_institution = analysis[0]['Other_institution']
        #     else:
        #       Other_institution = ''
        # NEW BLOCK 1
        YTTOKR = youtrack_get()
        client = ytclient(youtrackurl_get())
        currentissue = getissue(client,Project_ID,str(client.base_url),YTTOKR)
        print(currentissue.keys())
        ProjectTitle = currentissue['Project_Title']
        if ProjectTitle is None:
            ProjectTitle = 'noprojecttitle'
        if ProjectTitle == 'noprojecttitle' or currentissue['OverwriteRegistration'] == 'Yes': 
            summary = analysis[0]['Project_ID']# + "-" +  + "-" + Analysis_Type + "-" + keywords[0]
            if analysis[0]['VIBAffiliation'] is not None:
              VIBAffiliation = analysis[0]['VIBAffiliation']
            else:
              VIBAffiliation = ''
            #try:
            if analysis[0]['Other_institution'] is not None:
              Other_institution = analysis[0]['Other_institution']
            else:
              Other_institution = ''
            sdbf=False
            sdbfg=False
            description = "# Sample Preparation notes\nProtocol: \nOther notes:\n"\
            "\n# User Details\nInstitute/Organization: " + str(analysis[0]['Affiliation']) + "\nVIB Affiliation: " +VIBAffiliation + "\nOther institution" +Other_institution + "\nAddress: " + analysis[0]['Address']+ "\nPhone nr: " + analysis[0]['Phone'] + "\n\n# Analysis overview\nExperiment Summary: " + analysis[1]['Project_summary']+"\nProject_title: " + analysis[1]['Project_title'] + "\nData_Analysis: "+ str(analysis[1]['Data_analysis']) 
            # yt.update_issue(Project_ID, summary = "ContactPerson-GroupLeader-analysistype-keyword1",
            #         description=description)

            # yt.execute_command(Project_ID, "Contact_Person " + analysis[0]['Name'])
            # yt.execute_command(Project_ID, "GroupLeader "+ str(analysis[0]['Group_leader']  ))
            # yt.execute_command(Project_ID, "SamplePrep_Responsible Hans")
            # yt.execute_command(Project_ID, "DataAnalysis_Responsible Hans")
            # yt.execute_command(Project_ID, "Mass_Spectrometer LTQ Orbitrap XL")
            # yt.execute_command(Project_ID, "Run_Length_h 15_min")
            # # #yt.execute_command(Project_ID, "Analysis_Type " +  analysis[1]['Analysis_type'])
            # if analysis[0]['Affiliation'] == 'Industry':
            #     yt.execute_command(Project_ID, "Study_Type Non-Academic") #+ str(analysis[0]['Affiliation_Type']) )
            # elif analysis[0]['Affiliation'].find("VIB") != -1:
            #     yt.execute_command(Project_ID, "Study_Type VIB") #+ str(analysis[0]['Affiliation_Type']) )
            # else:
            #     yt.execute_command(Project_ID, "Study_Type Academic") #+ str(analysis[0]['Affiliation_Type']) )
            # yt.execute_command(Project_ID, "No_Samples "+ str(analysis[2]['Nb_samples']))
            # yt.execute_command(Project_ID, "Project_Title "+ analysis[1]['Project_title'])
            # NEW BLOCK2
            # set main fields
            responsemain = updateissuemainPMD(client,Project_ID,str(client.base_url),YTTOKR,description,analysis)
            print(responsemain.status_code)
            # if analysis[1]['Sample_preparation']:
            #      yt.execute_command(Project_ID, "tag nSP")
            # if analysis[1]['Data_analysis']:
            #       yt.execute_command(Project_ID, "tag nDA")
            responsetags = updateissuetagsPMD(client,Project_ID,str(client.base_url),YTTOKR,analysis)
            #yt.create_attachment(Project_ID,name=str(analysis[3]['EDfile']),content=analysis[3]['EDfile'],author_login ="root", group="PRC-team" ) 
            attachmentsrequest = updateissueattachmentsPMD(client,Project_ID,str(client.base_url),YTTOKR, analysis, sdbf,sdbfg)
            print(attachmentsrequest.status_code)
            # send project registration confirmation email
            subject = 'VIB Proteomics Core, Project registration confirmation - Read carefully'
            #message = render_to_string('confirmation_email.txt', {'formdict': formdict,'Project_ID': Project_ID,'Contact_Person': Contact_Person})
            html_message = render_to_string('confirmation_email.html', {'formdict': formdict,'Project_ID': Project_ID,'Contact_Person': Contact_Person})
            from_email=settings.EMAIL_HOST_USER
            to_list = [self.request.user.email]
            #template2 = os.path.join(settings.BASE_DIR, 'templates/confirmation_email.html')
            #message = render_to_string(template1, {'user': user})
            bcc = [settings.ADMINS[0][1],settings.ADMINS[1][1]]
            msg=EmailMessage(subject, html_message, from_email, to_list, bcc)
            msg.content_subtype = "html"
            msg.attach_file(os.path.join(settings.BASE_DIR,'static/TermsofUse_VIBProteomicsCore.pdf'))
            msg.attach_file(os.path.join(settings.BASE_DIR,'static/documents/Sender_Receiver_information.docx'))
            msg.send()
            return render(self.request,'done.html',{
                'formdict': formdict,

                })
        else:
            return render(self.request,'done4ar.html',{
                'formdict': formdict,

                })

    def get_form_initial(self, step):
        """
        Set projet id and email for step1
        Set extra parameter for step2, which is from clean data of step1.
        """
        initial = self.initial_dict.get(step, {})
        if step=='0':
            form_class=self.form_list[step]
            Project_ID = self.request.user.username
            Email = self.request.user.email
            #Analysis_Type = self.request.user.profile.Main_Analysis_Type
            initial.update({'Project_ID':Project_ID, 'Email':Email})
            return initial
        if step=='1':
            form_class=self.form_list[step]
            Main_analysis_type = self.request.user.Main_analysis_type
            #Analysis_Type = self.request.user.profile.Main_Analysis_Type
            initial.update({'Main_analysis_type':Main_analysis_type})
            return initial
        if step == '3':
            form_class = self.form_list[step]
            prev_data2 = self.storage.get_step_data('2')
            #prev_data3 = self.storage.get_step_data('3')
            prev_data = {**prev_data2}
            prev_data["PID"] = str(self.request.user.username)
            xlsx_data = WriteToExcel4(prev_data)
            return self.initial_dict.get(step, prev_data)

class ContactWizardPTM(SessionWizardView):
    instance=None
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT,'seqdbs'))
    def get_template_names(self):
        return [TEMPLATESPTM[self.steps.current]]
    #def process_form_data(form_list):
     #   form_data = [form.get_cleaned_data for form in form_list] 
      #  return form_data
        #logr.debug(form_data[0])['subject']
        #logr.debug(form_data[1])['sender']
        #logr.debug(form_data[2])['message']
    def done(self, form_list,form_dict, **kwargs):
        #############################    
       # list of dictionaries of results
        analysis = [form.cleaned_data for form in form_list]
        userid = get_user(self.request)
        customer,created = Profile.objects.update_or_create(user_id=self.request.user, defaults=analysis[0])
        analise,created = Analysis.objects.update_or_create(user_id=userid.id, defaults=analysis[1])
        # file field
        formtitles = ["User details", "Analysis overview", "Sample information", "Experimental Design information",
        "Experimental Design and Sample details", "Terms of Use"]
        formdict=dict()
        for i in range(len(formtitles)):
            formdict[formtitles[i]]=analysis[i]
        print('formdict' + str(formdict))
        Project_ID = analysis[0]['Project_ID']
        Contact_Person = analysis[0]['Name'].split(',')[0]
        # new block1
        YTTOKR = youtrack_get()
        client = ytclient(youtrackurl_get())
        currentissue = getissue(client,Project_ID,str(client.base_url),YTTOKR)
        #print(currentissue.keys())
        ProjectTitle = currentissue['Project_Title']
        if ProjectTitle is None:
            ProjectTitle = 'noprojecttitle'
        if ProjectTitle == 'noprojecttitle' or currentissue['OverwriteRegistration'] == 'Yes': 
            summary = analysis[0]['Project_ID']# + "-" +  + "-" + Analysis_Type + "-" + keywords[0]
            if analysis[0]['VIBAffiliation'] is not None:
              VIBAffiliation = analysis[0]['VIBAffiliation']
            else:
              VIBAffiliation = ''
            if analysis[0]['Other_institution'] is not None:
              Other_institution = analysis[0]['Other_institution']
            else:
              Other_institution = ''
            sdbfg = False
            if analysis[2]['Sequence_database_name'] is not None:
              Sequence_database_name = analysis[2]['Sequence_database_name']
            else:
              Sequence_database_name = ''
            sdbf = False
            if analysis[2]['Sequence_database_file'] is not None:
              Sequence_database_file= analysis[2]['Sequence_database_file']
              sdbf=True
            else:
              Sequence_database_file = ''
            if analysis[2]['Buffer_composition'] is not None:
              Buffer_composition= analysis[2]['Buffer_composition']
            else:
              Buffer_composition = ''
            if analysis[3]['Isotopic_labeling_details'] is not None:
              Isotopic_labeling_details = analysis[3]['Isotopic_labeling_details']
            else:
              Isotopic_labeling_details = ''
            if analysis[3]['Other_information'] is not None:
              Other_information = analysis[3]['Other_information']
            else:
              Other_information = ''
            description = "# Sample Preparation notes\nProtocol: \nOther notes:\n"\
                  + "\n# User Details\nInstitute/Organization: " + str(analysis[0]['Affiliation']) + "\nVIB Affiliation: " +VIBAffiliation + "\nOther institution" +Other_institution + "\nAddress: " + analysis[0]['Address']+ "\nPhone nr: " + analysis[0]['Phone'] + "\n\n# Analysis overview\nExperiment Summary: " + analysis[1]['Project_summary']+"\nProject_title: " + analysis[1]['Project_title'] + "\nData_Analysis: "+ str(analysis[1]['Data_analysis']) + "\n\n# Sample information" \
                  +  "\nPTM(s) under study: "+ analysis[2]['PTM'] + "\nSample_Species: "+ analysis[2]['Species'] + '\nSequence_Database_Public_Availability: ' + str(analysis[2]['Sequence_Database_Public_Availability']) \
                  + "\nSequence_Database_Name:" + Sequence_database_name+"\nSequence_database_file:" + str(Sequence_database_file) + "\nSample_Type:" + analysis[2]['Sample_Type']  + "\nBuffer_composition:" + Buffer_composition + "\n\n# Experimental Design information\nConditions_to_compare: " + analysis[3]['Conditions_to_compare'] +"\nIsotopic labeling: " + str(analysis[3]['Isotopic_labeling'])+ "\nIsotopic labeling details: " + Isotopic_labeling_details + "\nOther information: " \
                  + Other_information
            responsemain = updateissuemainSG(client,Project_ID,str(client.base_url),YTTOKR,description,analysis)
            print(responsemain.status_code)
            # yt.update_issue(Project_ID, summary = "ContactPerson-GroupLeader-analysistype-keyword1",
            #         description=description)

            # yt.execute_command(Project_ID, "Contact_Person " + analysis[0]['Name'])
            # yt.execute_command(Project_ID, "GroupLeader "+ str(analysis[0]['Group_leader']  ))
            # if analysis[0]['Affiliation'] == 'Industry':
            #     yt.execute_command(Project_ID, "Study_Type Non-Academic") #+ str(analysis[0]['Affiliation_Type']) )
            # elif analysis[0]['Affiliation'].find("VIB") != -1:
            #     yt.execute_command(Project_ID, "Study_Type VIB") #+ str(analysis[0]['Affiliation_Type']) )
            # else:
            #     yt.execute_command(Project_ID, "Study_Type Academic") #+ str(analysis[0]['Affiliation_Type']) )
            # yt.execute_command(Project_ID, "No_Samples "+ str(analysis[3]['Nb_samples']))
            # yt.execute_command(Project_ID, "Project_Title "+ analysis[1]['Project_title'])
            # if analysis[1]['Sample_preparation']:
            #      yt.execute_command(Project_ID, "tag nSP")
            # if analysis[1]['Data_analysis']:
            #      yt.execute_command(Project_ID, "tag nDA")
            # yt.execute_command(Project_ID, "tag PTM")
            responsetags = updateissuetagsSG(client,Project_ID,str(client.base_url),YTTOKR,analysis)
            #print(responsetags.status_code)
            # if sdbf:
            #     yt.create_attachment(Project_ID,name=Sequence_database_file,content=analysis[2]['Sequence_database_file'],author_login ="root", group="PRC-team") 
            # yt.create_attachment(Project_ID,name=str(analysis[4]['EDfile']),content=analysis[4]['EDfile'],author_login ="root", group="PRC-team") 
            attachmentsrequest = updateissueattachmentsSG(client,Project_ID,str(client.base_url),YTTOKR, analysis, sdbf, sdbfg)
            print(attachmentsrequest.status_code)
            # send project registration confirmation email
            subject = 'VIB Proteomics Core, Project registration confirmation - Read carefully'
            html_message = render_to_string('confirmation_email.html', {'formdict': formdict,'Project_ID': Project_ID,'Contact_Person': Contact_Person})
            from_email=settings.EMAIL_HOST_USER
            to_list = [self.request.user.email]
            bcc = [settings.ADMINS[0][1],settings.ADMINS[1][1]]
            msg=EmailMessage(subject, html_message, from_email, to_list, bcc)
            msg.content_subtype = "html"
            msg.attach_file(os.path.join(settings.BASE_DIR,'static/TermsofUse_VIBProteomicsCore.pdf'))
            msg.attach_file(os.path.join(settings.BASE_DIR,'static/documents/Sender_Receiver_information.docx'))
            msg.send()
            return render(self.request,'done.html',{
                'formdict': formdict,
                })
        else:
            return render(self.request,'done4ar.html',{
                'formdict': formdict,

                })

    def get_form_initial(self, step):
        """
        Set projet id and email for step1
        Set extra parameter for step2, which is from clean data of step1.
        """
        initial = self.initial_dict.get(step, {})
        if step=='0':
            form_class=self.form_list[step]
            Project_ID = self.request.user.username
            Email = self.request.user.email
            #Analysis_Type = self.request.user.profile.Main_Analysis_Type
            initial.update({'Project_ID':Project_ID, 'Email':Email})
            return initial
        if step=='1':
            form_class=self.form_list[step]
            Main_analysis_type = self.request.user.Main_analysis_type
            #Analysis_Type = self.request.user.profile.Main_Analysis_Type
            initial.update({'Main_analysis_type':Main_analysis_type})
            return initial
        # #if step == '3':
         #   form_class = self.form_list[step]
            #Issue = self.request.user.profile.Issue + '-S' 
            #form_class['Generic_Sample_Name'] = self.request.user.profile.Issue 
            #initial.update({'Generic_Sample_Name':Analysis_Type})
            #return initial
        if step == '4':
            form_class = self.form_list[step]
            #print(dir(self.storage))
            #prev_data1 = self.storage.get_step_data('0')
            #print(str(prev_data1))
            #pid=prev_data1["0-Project_ID"]
            #print("pid"+pid)
            prev_data2 = self.storage.get_step_data('2')
            #print(str(prev_data2))
            prev_data3 = self.storage.get_step_data('3')
            #print(str(prev_data3))
            prev_data = {**prev_data2, **prev_data3}
            #print("s"+str(self.request.user.username))
            prev_data["PID"] = str(self.request.user.username)
            #print(prev_data["PID"])
            xlsx_data = WriteToExcel(prev_data)
            #response.write(xlsx_data)
            #get_cleaned_data_for_step
            #samplename = prev_data.get('Generic_Sample_Name','')
            #return samplename
            return self.initial_dict.get(step, prev_data)
            #return self.initial_dict.get(step, {samplename:'samplename'})

  #  @method_decorator(login_required)
   # def dispatch(self, *args, **kwargs):
    #    return super(ContactWizardPTM, self).dispatch(*args, **kwargs)      
#projectregistrationsg = ContactWizardSG.as_view([AnalysisForm, Specimen_SGForm, ExperimentForm])

class ContactWizardAPMS(SessionWizardView):
    instance=None
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT,'seqdbs'))
    def get_template_names(self):
        return [TEMPLATESAPMS[self.steps.current]]
    #def process_form_data(form_list):
     #   form_data = [form.get_cleaned_data for form in form_list] 
      #  return form_data
        #logr.debug(form_data[0])['subject']
        #logr.debug(form_data[1])['sender']
        #logr.debug(form_data[2])['message']
    def done(self, form_list,form_dict, **kwargs):
       # list of dictionaries of results
        analysis = [form.cleaned_data for form in form_list]
        userid = get_user(self.request)
        customer,created = Profile.objects.update_or_create(user_id=self.request.user, defaults=analysis[0])
        analise,created = Analysis.objects.update_or_create(user_id=userid.id, defaults=analysis[1])
        # file field
        formtitles = ["User details", "Analysis overview", "Sample information", "Experimental Design information",
        "Experimental Design and Sample details", "Terms of Use"]
        formdict=dict()
        for i in range(len(formtitles)):
            formdict[formtitles[i]]=analysis[i]
        print('formdict' + str(formdict))
        Project_ID = analysis[0]['Project_ID']
        Contact_Person = analysis[0]['Name'].split(',')[0]
        # block1
        YTTOKR = youtrack_get()
        client = ytclient(youtrackurl_get())
        currentissue = getissue(client,Project_ID,str(client.base_url),YTTOKR)
        print(currentissue.keys())
        ProjectTitle = currentissue['Project_Title']
        if ProjectTitle is None:
            ProjectTitle = 'noprojecttitle'
        if ProjectTitle == 'noprojecttitle' or currentissue['OverwriteRegistration'] == 'Yes': 
            summary = analysis[0]['Project_ID']# + "-" +  + "-" + Analysis_Type + "-" + keywords[0]
            if analysis[0]['VIBAffiliation'] is not None:
              VIBAffiliation = analysis[0]['VIBAffiliation']
            else:
              VIBAffiliation = ''
            if analysis[0]['Other_institution'] is not None:
              Other_institution = analysis[0]['Other_institution']
            else:
              Other_institution = ''
            sdbfg = False
            if analysis[2]['Buffer_composition'] is not None:
              Buffer_composition= analysis[2]['Buffer_composition']
            else:
              Buffer_composition = ''
            if analysis[2]['Bait_Molecule_Protein'] is not None:
              Bait_Molecule_Protein = analysis[2]['Bait_Molecule_Protein']
            else:
              Bait_Molecule_Protein = ''
            if analysis[2]['Bait_Molecule']=='True':
              Bait_Molecule = 'Protein'
            else:
              Bait_Molecule = 'Other type of bait'
            sdbf = False
            if analysis[2]['Bait_sequence_file'] is not None:
                Bait_sequence_file= str(analysis[2]['Bait_sequence_file'])
                sdbf=True
            else:
                Bait_sequence_file = ''
            if analysis[2]['Bait_Molecule_other'] is not None:
                Bait_Molecule_other= analysis[2]['Bait_Molecule_other']
            else:
                Bait_Molecule_other = ''
            if analysis[2]['Antibodies'] is not None:
                Antibodies= analysis[2]['Antibodies']
            else:
                Antibodies = ''         
            if analysis[2]['AbSource'] is not None:
                AbSource= analysis[2]['AbSource']
            else:
                AbSource = ''         
            if analysis[2]['AbAmount'] is not None:
                AbAmount= analysis[2]['AbAmount']
            else:
                AbAmount = ''  
            if analysis[3]['Other_information'] is not None:
                Other_information = analysis[3]['Other_information']
                if 'tmt' in Other_information.lower():
                    Isotopic_labeling_details = 'tmt'
            else:
                Other_information = ''
            description = "# Sample Preparation notes\nProtocol: OnBead Digest\n"\
"Sample type: washed beads\nTrypsin: 1 µg \nOther notes:\n"\
            "\n# User Details\nInstitute/Organization: " + str(analysis[0]['Affiliation']) + "\nVIB Affiliation: " +VIBAffiliation + "\nOther institution" +Other_institution + "\nAddress: " + analysis[0]['Address']+ "\nPhone nr: " + analysis[0]['Phone'] + "\n\n# Analysis overview\nExperiment Summary: " + analysis[1]['Project_summary']+"\nProject_title: " + analysis[1]['Project_title'] + "\nData_Analysis: "+ str(analysis[1]['Data_analysis']) + "\n\n# Sample information" \
                  + "\nSample_Species: "+ analysis[2]['Species'] + "\nSample_Type: " + analysis[2]['Sample_Type'] + "\nBuffer_composition: " + Buffer_composition + "\nBait_Molecule: "+ Bait_Molecule + "\nBait_Molecule_Protein: "+ Bait_Molecule_Protein + "\nBait_sequence_file: "+ Bait_sequence_file + "\nBait_Molecule_other: "+ Bait_Molecule_other \
                  + "\nAntibodies: "+Antibodies + "\nAbSource: "+ AbSource + "\nAbAmount: "+ AbAmount \
                  + "\nBeads: "+ analysis[2]['Beads'] + "\nBeadsSource: "+ analysis[2]['BeadsSource'] + "\nBeadsAmount: "+ analysis[2]['BeadsAmount'] \
                  + "\n\n# Experimental Design information\nConditions_to_compare: " + analysis[3]['Conditions_to_compare'] + "\nOther information: " \
                  + Other_information
            #yt.update_issue(Project_ID, summary = "ContactPerson-GroupLeader-analysistype-keyword1",
             #       description=description)
            responsemain = updateissuemainSG(client,Project_ID,str(client.base_url),YTTOKR,description,analysis)
            print(responsemain.status_code)
            # yt.execute_command(Project_ID, "Contact_Person " + analysis[0]['Name'])
            # yt.execute_command(Project_ID, "GroupLeader "+ str(analysis[0]['Group_leader']  ))
            # if analysis[0]['Affiliation'] == 'Industry':
            #     yt.execute_command(Project_ID, "Study_Type Non-Academic") #+ str(analysis[0]['Affiliation_Type']) )
            # elif analysis[0]['Affiliation'].find("VIB") != -1:
            #     yt.execute_command(Project_ID, "Study_Type VIB") #+ str(analysis[0]['Affiliation_Type']) )
            # else:
            #     yt.execute_command(Project_ID, "Study_Type Academic") #+ str(analysis[0]['Affiliation_Type']) )
            # yt.execute_command(Project_ID, "No_Samples "+ str(analysis[3]['Nb_samples']))
            # yt.execute_command(Project_ID, "Project_Title "+ analysis[1]['Project_title'])
            responsetags = updateissuetagsSG(client,Project_ID,str(client.base_url),YTTOKR,analysis)
            # if sdbf:
            #     yt.create_attachment(Project_ID,name=Bait_sequence_file,content=analysis[2]['Bait_sequence_file'],author_login ="root", group="PRC-team") 
            # yt.create_attachment(Project_ID,name=str(analysis[4]['EDfile']),content=analysis[4]['EDfile'],author_login ="root", group="PRC-team") 
            # # send project registration confirmation email
            attachmentsrequest = updateissueattachmentsSG(client,Project_ID,str(client.base_url),YTTOKR, analysis, sdbf,sdbfg)
            subject = 'VIB Proteomics Core, Project registration confirmation - Read carefully'
            html_message = render_to_string('confirmation_email.html', {'formdict': formdict,'Project_ID': Project_ID,'Contact_Person': Contact_Person})
            from_email=settings.EMAIL_HOST_USER
            to_list = [self.request.user.email]
            bcc = [settings.ADMINS[0][1],settings.ADMINS[1][1]]
            msg=EmailMessage(subject, html_message, from_email, to_list, bcc)
            msg.content_subtype = "html"
            msg.attach_file(os.path.join(settings.BASE_DIR,'static/TermsofUse_VIBProteomicsCore.pdf'))
            msg.attach_file(os.path.join(settings.BASE_DIR,'static/documents/Sender_Receiver_information.docx'))
            msg.send()
            return render(self.request,'done.html',{
                'formdict': formdict,
                })
        else:
            return render(self.request,'done4ar.html',{
                'formdict': formdict,

                })

    def get_form_initial(self, step):
        """
        Set projet id and email for step1
        Set extra parameter for step2, which is from clean data of step1.
        """
        initial = self.initial_dict.get(step, {})
        if step=='0':
            form_class=self.form_list[step]
            Project_ID = self.request.user.username
            Email = self.request.user.email
            #Analysis_Type = self.request.user.profile.Main_Analysis_Type
            initial.update({'Project_ID':Project_ID, 'Email':Email})
            return initial
        if step=='1':
            form_class=self.form_list[step]
            Main_analysis_type = self.request.user.Main_analysis_type
            #Analysis_Type = self.request.user.profile.Main_Analysis_Type
            initial.update({'Main_analysis_type':Main_analysis_type})
            return initial
        if step == '4':
            form_class = self.form_list[step]
            #print(dir(self.storage))
            #prev_data1 = self.storage.get_step_data('0')
            #print(str(prev_data1))
            #pid=prev_data1["0-Project_ID"]
            #print("pid"+pid)
            prev_data2 = self.storage.get_step_data('2')
            #print(str(prev_data2))
            prev_data3 = self.storage.get_step_data('3')
            #print(str(prev_data3))
            prev_data = {**prev_data2, **prev_data3}
            #print("s"+str(self.request.user.username))
            prev_data["PID"] = str(self.request.user.username)
            xlsx_data = WriteToExcel2(prev_data)
            #response.write(xlsx_data)
            #get_cleaned_data_for_step
            #samplename = prev_data.get('Generic_Sample_Name','')
            #return samplename
            return self.initial_dict.get(step, prev_data) 
            #return self.initial_dict.get(step, {samplename:'samplename'})
    #@method_decorator(login_required)
    #def dispatch(self, *args, **kwargs):
    #    return super(ContactWizardGB, self).dispatch(*args, **kwargs)


class ContactWizardGB(SessionWizardView):
    instance=None
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT,'seqdbs'))
    def get_template_names(self):
        return [TEMPLATESGB[self.steps.current]]
    #def process_form_data(form_list):
     #   form_data = [form.get_cleaned_data for form in form_list] 
      #  return form_data
        #logr.debug(form_data[0])['subject']
        #logr.debug(form_data[1])['sender']
        #logr.debug(form_data[2])['message']
    def done(self, form_list,form_dict, **kwargs):
       # list of dictionaries of results
        analysis = [form.cleaned_data for form in form_list]
        userid = get_user(self.request)
        customer,created = Profile.objects.update_or_create(user_id=self.request.user, defaults=analysis[0])
        analise,created = Analysis.objects.update_or_create(user_id=userid.id, defaults=analysis[1])
        # file field
        formtitles = ["User details", "Analysis overview", "Sample information", "Experimental Design information",
        "Experimental Design and Sample details", "Terms of Use"]
        formdict=dict()
        for i in range(len(formtitles)):
            formdict[formtitles[i]]=analysis[i]
        print('formdict' + str(formdict))
        Project_ID = analysis[0]['Project_ID']
        Contact_Person = analysis[0]['Name'].split(',')[0]
        YTTOKR = youtrack_get()
        client = ytclient(youtrackurl_get())
        currentissue = getissue(client,Project_ID,str(client.base_url),YTTOKR)
        print(currentissue.keys())
        ProjectTitle = currentissue['Project_Title']
        if ProjectTitle is None:
            ProjectTitle = 'noprojecttitle'        
        if ProjectTitle == 'noprojecttitle' or currentissue['OverwriteRegistration'] == 'Yes': 
            summary = analysis[0]['Project_ID']# + "-" +  + "-" + Analysis_Type + "-" + keywords[0]
            if analysis[0]['VIBAffiliation'] is not None:
              VIBAffiliation = analysis[0]['VIBAffiliation']
            else:
              VIBAffiliation = ''
            if analysis[0]['Other_institution'] is not None:
              Other_institution = analysis[0]['Other_institution']
            else:
              Other_institution = ''
            sdbfg = False
            if analysis[2]['Gel_file'] is not None:
              #Gel_file= analysis[2]['Gel_file']
              sdbfg=True
            else:
              Gel_file = ''
            if analysis[2]['Sequence_database_name'] is not None:
              Sequence_database_name = analysis[2]['Sequence_database_name']
            else:
              Sequence_database_name = ''
            sdbf = False
            if analysis[2]['Sequence_database_file'] is not None:
              Sequence_database_file= analysis[2]['Sequence_database_file']
              sdbf=True
            else:
              Sequence_database_file = ''
            if analysis[3]['Isotopic_labeling_details'] is not None:
              Isotopic_labeling_details = analysis[3]['Isotopic_labeling_details']
            else:
              Isotopic_labeling_details = ''
            if analysis[3]['Other_information'] is not None:
              Other_information = analysis[3]['Other_information']
            else:
              Other_information = ''

            description =  "# Sample Preparation notes\nProtocol: In Gel Digestion\nACN wash: 50 %\n"\
"Trypsin solution volume: 15 µl\nOther notes:\n"\
            "\n# User Details\nInstitute/Organization: " + str(analysis[0]['Affiliation']) +"\nVIB Affiliation: " +VIBAffiliation + "\nOther institution" +Other_institution + "\nAddress: " + analysis[0]['Address']+ "\nPhone nr: " + analysis[0]['Phone'] + "\n\n# Analysis overview\nExperiment Summary: " + analysis[1]['Project_summary']+"\nProject_title: " + analysis[1]['Project_title'] + "\nData_Analysis: "+ str(analysis[1]['Data_analysis']) + "\n\n# Sample information" \
                  + "\nSetup: "+ analysis[2]['Setup'] + '\nGel_file: ' + str(analysis[2]['Gel_file']) \
                  + "\nSample_Species: "+ analysis[2]['Species'] + '\nSequence_Database_Public_Availability: ' + str(analysis[2]['Sequence_Database_Public_Availability']) \
                  + "\nSequence_Database_Name: " + Sequence_database_name+"\nSequence_database_file: " + str(Sequence_database_file) \
                  + "\nPAGE Info: "+ analysis[2]['PAGEInfo'] + '\nPA-Percentage: ' + str(analysis[2]['PolyAcrylPercentage']) \
                  + "\nStaining Method: "+ analysis[2]['StainingMethod'] + '\nPAGEType: ' + str(analysis[2]['PAGEType']) \
                  + "\n\n# Experimental Design information\nConditions_to_compare: " + analysis[3]['Conditions_to_compare'] +"\nIsotopic labeling: " + str(analysis[3]['Isotopic_labeling'])+ "\nIsotopic labeling details: " + Isotopic_labeling_details + "\nOther information: " \
                  + Other_information

            # yt.update_issue(Project_ID, summary = "ContactPerson-GroupLeader-analysistype-keyword1",
            #         description=description)

            # yt.execute_command(Project_ID, "Contact_Person " + analysis[0]['Name'])
            # yt.execute_command(Project_ID, "GroupLeader "+ str(analysis[0]['Group_leader']  ))
            # if analysis[0]['Affiliation'] == 'Industry':
            #     yt.execute_command(Project_ID, "Study_Type Non-Academic") #+ str(analysis[0]['Affiliation_Type']) )
            # elif analysis[0]['Affiliation'].find("VIB") != -1:
            #     yt.execute_command(Project_ID, "Study_Type VIB") #+ str(analysis[0]['Affiliation_Type']) )
            # else:
            #     yt.execute_command(Project_ID, "Study_Type Academic") #+ str(analysis[0]['Affiliation_Type']) )
            # yt.execute_command(Project_ID, "No_Samples "+ str(analysis[3]['Nb_samples']))
            # yt.execute_command(Project_ID, "Project_Title "+ analysis[1]['Project_title'])
            responsemain = updateissuemainSG(client,Project_ID,str(client.base_url),YTTOKR,description,analysis)
            print(responsemain.status_code)
            # if analysis[1]['Sample_preparation']:
            #      yt.execute_command(Project_ID, "tag nSP")
            # if analysis[1]['Data_analysis']:
            #      yt.execute_command(Project_ID, "tag nDA")
            responsetags = updateissuetagsSG(client,Project_ID,str(client.base_url),YTTOKR,analysis)
            # if sdbfg:
            #     yt.create_attachment(Project_ID,name=Gel_file,content=analysis[2]['Gel_file'],author_login ="root", group="PRC-team") 
            # if sdbf:
            #     yt.create_attachment(Project_ID,name=Sequence_database_file,content=analysis[2]['Sequence_database_file'],author_login ="root", group="PRC-team") 
            # yt.create_attachment(Project_ID,name=str(analysis[4]['EDfile']),content=analysis[4]['EDfile'],author_login ="root", group="PRC-team") 
            attachmentsrequest = updateissueattachmentsSG(client,Project_ID,str(client.base_url),YTTOKR, analysis, sdbf,sdbfg)
            print(attachmentsrequest.status_code)
            # send project registration confirmation email
            subject = 'VIB Proteomics Core, Project registration confirmation - Read carefully'
            html_message = render_to_string('confirmation_email.html', {'formdict': formdict,'Project_ID': Project_ID,'Contact_Person': Contact_Person})
            from_email=settings.EMAIL_HOST_USER
            to_list = [self.request.user.email]
            bcc = [settings.ADMINS[0][1],settings.ADMINS[1][1]]
            msg=EmailMessage(subject, html_message, from_email, to_list, bcc)
            msg.content_subtype = "html"
            msg.attach_file(os.path.join(settings.BASE_DIR,'static/TermsofUse_VIBProteomicsCore.pdf'))
            msg.attach_file(os.path.join(settings.BASE_DIR,'static/documents/Sender_Receiver_information.docx'))
            msg.send()
            return render(self.request,'done.html',{
                'formdict': formdict,
                #'analysisd':form_dict,
                #'formnames':formnames,
                #'formtitles':formtitles,
                #'fieldnames':fieldvalues,
                #'upload_file' : upload_file,
                })
        else:
            return render(self.request,'done4ar.html',{
                'formdict': formdict,

                })


    def get_form_initial(self, step):
        """
        Set projet id and email for step1
        Set extra parameter for step2, which is from clean data of step1.
        """
        initial = self.initial_dict.get(step, {})
        if step=='0':
            form_class=self.form_list[step]
            Project_ID = self.request.user.username
            Email = self.request.user.email
            #Analysis_Type = self.request.user.profile.Main_Analysis_Type
            initial.update({'Project_ID':Project_ID, 'Email':Email})
            return initial
        if step=='1':
            form_class=self.form_list[step]
            Main_analysis_type = self.request.user.Main_analysis_type
            #Analysis_Type = self.request.user.profile.Main_Analysis_Type
            initial.update({'Main_analysis_type':Main_analysis_type})
            return initial
        #if step == '3':
         #   form_class = self.form_list[step]
            #Issue = self.request.user.profile.Issue + '-S' 
            #form_class['Generic_Sample_Name'] = self.request.user.profile.Issue 
            #initial.update({'Generic_Sample_Name':Analysis_Type})
            #return initial
        if step == '4':
            form_class = self.form_list[step]
            #print(dir(self.storage))
            #prev_data1 = self.storage.get_step_data('0')
            #print(str(prev_data1))
            #pid=prev_data1["0-Project_ID"]
            #print("pid"+pid)
            prev_data2 = self.storage.get_step_data('2')
            #print(str(prev_data2))
            prev_data3 = self.storage.get_step_data('3')
            #print(str(prev_data3))
            prev_data = {**prev_data2, **prev_data3}
            #print("s"+str(self.request.user.username))
            prev_data["PID"] = str(self.request.user.username)
            #print(prev_data["PID"])
            xlsx_data = WriteToExcel3(prev_data)
            #response.write(xlsx_data)
            #get_cleaned_data_for_step
            #samplename = prev_data.get('Generic_Sample_Name','')
            #return samplename
            return self.initial_dict.get(step, prev_data)

# User profile
# =============================
def get_user_profile(request):
	#user = request.user.get(username)
	args={"user":request.user}
	return render(request,'profile.html', args)
	#return render(request, 'profile.html',{"user":user})

#	@method_decorator(login_required)
#	def dispatch(self, *args, **kwargs):#
#		return super(LoginView, self).dispatch(*args, **kwargs)

#def get_user_projectinfo(request):
	#user = request.user.get(username)
#	args={"user":request.user}#
#	return render(request,'projectinfo.html', args)
	#return render(request, 'profile.html',{"user":user})




#class ProjectInfoView(ListView):
class ProjectInfoView(TemplateView):
    template_name = 'project-info.html'
    # @method_decorator(login_required)
    # def dispatch(self, *args, **kwargs):
    #     return super(ProjectInfoView, self).dispatch(*args, **kwargs)

    # def get_queryset(self):
    #     qs = Profile.objects.filter(user=self.request.user.profile.user)
    #     print(qs)
    #     print(dir(qs[0]))
    #def get_queryset(self, request, *args, **kwargs):
    #def get_queryset(self):
     #   self.object=User.objects.filter(username=self.request.user.username).get()
        #self.object=self.get_object(queryset=User.objects.filter(user=self.request.user))
      #  return
        #return super().get(request,*args, **kwargs)

    #def get_object(queryset=None):
        #self.object=self.get_object(queryset=Profile.objects.filter(user=self.request.user.profile.user))
        #self.object=self.get_object(queryset=User.objects.filter(user=self.request.user))
        #return 
        #Profile.objects.filter(user=self.request.user.profile.user)
    
    #def get_queryset(self):
     #   return self.object.
      #  Profile.objects.filter(user=self.request.user.profile.user)

    def get_context_data(self,*args,**kwargs):
        #url = static("PRC_issues_dailyreport2.csv")
        #print(url)
        context=super(ProjectInfoView,self).get_context_data(*args,**kwargs)
        filepath = os.path.join(settings.BASE_DIR,"static/PRC_issues_dailyreport2all.csv")
        filepath2 = os.path.join(settings.BASE_DIR,"static/PRC_MassSpecs.csv")
        with open(filepath, "r", encoding='utf-8') as csvfile:
            csvfile_reader=csv.DictReader(csvfile)
            issuefound = False
            for row in csvfile_reader:
                if row["YouTrack_id"]==self.request.user.username:
                    print("yes")
                    issuefound = True
                #if row["YouTrack_id"]=="PRC-4495":
                    context["Project_ID"] = row["YouTrack_id"]
                    context["State"] = row["State"]
                    context["Scheduling_State"] = row["Scheduling_State"]
                    context["Mass_Spectrometer"] = row["Mass_Spectrometer"]
                    if row["Scheduling_State"]=='NotScheduled':
                        context["Scheduling_StateName"] = ', waiting to be processed.'
                    else:
                        context["Scheduling_StateName"] = ', currently being processed.'
                    context["Median_wTime"] = row["Median_wTime"]
                    #context["Min_wTime"] = row["Min_wTime"]
                    context["today"] = datetime.datetime.now().strftime("%A, %b, %d, %Y")
                    #today = context["today"]
                    #pass
            if not issuefound:
                    print("no")
                #if row["YouTrack_id"]=="PRC-4495":
                    context["Project_ID"] = self.request.user.username
                    context["State"] = "Closed"
                    context["Scheduling_State"] = "NotScheduled"
                    context["Mass_Spectrometer"] = "Undefined"
                    if row["Scheduling_State"]=='NotScheduled':
                        context["Scheduling_StateName"] = ' and has already been processed.'

                    context["Median_wTime"] = "45"
                    #context["Min_wTime"] = row["Min_wTime"]
                    context["today"] = datetime.datetime.now().strftime("%A, %b, %d, %Y")




       # print(context["Project_ID"])
        statesoutfile =os.path.join(settings.BASE_DIR,"static/PRCCMBPSB_States.json")
        with open(statesoutfile) as data_file:
            data_loaded = json.load(data_file)
            context.update(data_loaded)
            #print(type(data_loaded["Waiting"]))
            #return render(request, 'chartjs.html',data_loaded)
        #print(context["Project_ID"])
        ms_lst =['lumos','qehf','qehfb','qe','elite']

        with open(filepath2, "r", encoding='utf-8') as csvfile:
            #csvfile_reader=csv.DictReader(csvfile)
            csvfile_reader=csv.reader(csvfile)
            next(csvfile_reader)
            i = 0
            context["projectmsstatusdescription"] = "__ "
            for row in csvfile_reader:
                #temp = int(row["total_running_time_days"])
                temp = row
                #status = int(row["status"])
                #status_description = int(row["status_description"])
                #print("temp")
                #print(temp)
                if int(temp[1]) > 5:
                    temp[1]=5
                print(context["Mass_Spectrometer"])
                print(temp[0])
                if temp[0]==context["Mass_Spectrometer"]:
                    #print("yes")
                    #print(temp[3])
                    context["projectmsstatusdescription"] = temp[3]

                temp[1] = "Gauge" + str(temp[1])
                #print(temp[2])
                #print(len(temp))
                context[ms_lst[i]]=temp[0:4]
                print(context[ms_lst[i]])
                i+=1
        print(context)
        return context


class ProjectInfoGuestView(ListView):
    template_name = 'project-info-guest.html'
    # @method_decorator(login_required)
    # def dispatch(self, *args, **kwargs):
    #     return super(ProjectInfoView, self).dispatch(*args, **kwargs)

    # def get_queryset(self):
    #     qs = Profile.objects.filter(user=self.request.user.profile.user)
    #     print(qs)
    #     print(dir(qs[0]))
    #def get_queryset(self, request, *args, **kwargs):
    def get_queryset(self):
        self.object=User.objects.filter(username=self.request.user.username).get()
        #return super().get(request,*args, **kwargs)

    #def get_object(queryset=None):
        #self.object=self.get_object(queryset=Profile.objects.filter(user=self.request.user.profile.user))
        return 
        #Profile.objects.filter(user=self.request.user.profile.user)
    
    #def get_queryset(self):
     #   return self.object.
      #  Profile.objects.filter(user=self.request.user.profile.user)

    def get_context_data(self,**kwargs):
        #url = static("PRC_issues_dailyreport2.csv")
        #print(url)
        context=super().get_context_data(**kwargs)
        filepath = os.path.join(settings.BASE_DIR,"static/PRC_issues_dailyreport.csv")
        with open(filepath, "r", encoding='utf-8') as csvfile:   
            csvfile_reader=csv.DictReader(csvfile)
            for row in csvfile_reader:
                if row["YouTrack_id"]==self.object.username:
                    context["Issue"] = row["YouTrack_id"]
                    context["State"] = row["State"]
                    context["Scheduling_State"] = row["SchedulingState"]
                    context["Median_wTime"] = row["Median_wTime"]
                    context["Min_wTime"] = row["Min_wTime"]
                    context["today"] = datetime.datetime.now().strftime("%A, %b, %d, %Y")
                    #today = context["today"]
                    pass
        #print(context)
        return context

class ProjectInfoGaugeView(ListView):
    template_name = 'project-infogauge.html'
    # @method_decorator(login_required)
    # def dispatch(self, *args, **kwargs):
    #     return super(ProjectInfoView, self).dispatch(*args, **kwargs)

    # def get_queryset(self):
    #     qs = Profile.objects.filter(user=self.request.user.profile.user)
    #     print(qs)
    #     print(dir(qs[0]))
    #def get_queryset(self, request, *args, **kwargs):
    def get_queryset(self):
        self.object=Profile.objects.filter(user=self.request.user.profile.user)
        #return super().get(request,*args, **kwargs)

    #def get_object(queryset=None):
        #self.object=self.get_object(queryset=Profile.objects.filter(user=self.request.user.profile.user))
        return 
        #Profile.objects.filter(user=self.request.user.profile.user)
    
    #def get_queryset(self):
     #   return self.object.
      #  Profile.objects.filter(user=self.request.user.profile.user)

    def get_context_data(self,**kwargs):
        #url = static("PRC_issues_dailyreport2.csv")
        #print(url)
        context=super().get_context_data(**kwargs)
        filepath = os.path.join(settings.BASE_DIR,"static/PRC_issues_dailyreport.csv")
        with open(filepath, "r") as csvfile:
            csvfile_reader=csv.DictReader(csvfile)
            for row in csvfile_reader:
                if row["YouTrack_id"]==self.object[0].Issue:
                    context["Issue"] = row["YouTrack_id"]
                    context["State"] = row["State"]
                    context["Scheduling_State"] = row["SchedulingState"]
                    context["Median_wTime"] = row["Median_wTime"]
                    context["Min_wTime"] = row["Min_wTime"]
                    context["today"] = datetime.datetime.now().strftime("%A, %b, %d, %Y")
                    #today = context["today"]
                    pass
        print(context)
        return context


class HomeView(TemplateView):
 	template_name = 'home.html'

class PreparationView(TemplateView):
   template_name = 'protocols.html'

	#def get_context_data(request,self, *args, **kwargs):
	# 	#context = super(HomeView, self).get_context_data(*args, **kwargs)
	# 	context = {}
	# 	print context
	# 	return context

	#return render(request, 'home.html', {'gulag':'context variable'}) # resonse option 1
	#return HttpResponse('Hello')
	##	context = {}
	#	return render(request, 'home.html', context)
# def get_form_initial(self, step):
#         """
#         Set extra parameter for step2, which is from clean data of step1.
#         """
#         initial = self.initial_dict.get(step, {})
#         if step == '2':
#             form_class = self.form_list[step]
#             Issue = self.request.user.profile.Issue 
#             #form_class['Generic_Sample_Name'] = self.request.user.profile.Issue 
#             initial.update({'Generic_Sample_Name':Issue})
#             return initial
class TermsOfUseView(TemplateView):
    template_name = 'TermsOfUse.html'

class ShippingInstructionsView(TemplateView):
    template_name = 'sample-delivery3.html'

# def about(request):
# 	context = {}
# 	return render(request, 'about.html', context)

class InfoView(TemplateView):
    template_name = 'information.html'
    
class AboutTheCoreView(TemplateView):
    template_name = 'AboutTheCore.html'


class ReportsView(TemplateView):
    template_name = 'MM.html'


class ContactView(TemplateView):
    template_name = 'contact.html'

# def about(request):
#   context = {}
#   return render(request, 'about.html', context)

class QuestionsView(TemplateView):
    template_name = 'questions.html'

class MoveView(TemplateView):
    template_name = 'move.html'

import datetime

# def about(request):
#   context = {}
#   return render(request, 'about.html', context)

class AboutView(TemplateView):
    template_name = 'about.html'
# def get(self, request, *args, **kargs):
# context = {}
# return render(request, 'about.html', context)
    def get_context_data(self,*args, **kwargs):
        context = super(AboutView, self).get_context_data(*args, **kwargs)
        context["today"] = datetime.datetime.now().strftime("%A, %b, %d, %Y")
        return context

##################################################################################################3
# def weather_history(request):
#     weather_period = Weather.objects.all()
#     town = None
#     if request.method == 'POST':
#         form = EDForm(data=request.POST)
#         if form.is_valid():
#             town_id = form.data['town']
#             town = Town.objects.get(pk=town_id)
#             weather_period = Weather.objects.filter(town=town_id)
#         if 'excel' in request.POST:
#             response = HttpResponse(content_type='application/vnd.ms-excel')
#             response['Content-Disposition'] = 'attachment; filename=Report.xlsx'
#             xlsx_data = WriteToExcel(weather_period, town)
#             response.write(xlsx_data)
#             return response
#         if 'pdf' in request.POST:
#             response = HttpResponse(content_type='application/pdf')
#             today = date.today()
#             filename = 'pdf_demo' + today.strftime('%Y-%m-%d')
#             response['Content-Disposition'] =\
#                 'attachement; filename={0}.pdf'.format(filename)
#             buffer = BytesIO()
#             report = PdfPrint(buffer, 'A4')
#             pdf = report.report(weather_period, 'Weather statistics data')
#             response.write(pdf)
#             return response
#     else:
#         form = WeatherForm()

#     template_name = "exportingfiles/weather_history.html"
#     context = {
#         'form': form,
#         'town': town,
#         'weather_period': weather_period,
#     }
#     return render(request, template_name, context)

# def request_page(request):
#     weather_period = 's'
#     if request.method=='GET':
#         #form = EDForm()
#         #i#f form.is_valid():
#         #town_id = form.data['town']
#         #town = Town.objects.get(pk=town_id)
#           #  weather_period = 'ss'
#         if "excel" in request.GET:
#             response = HttpResponse(content_type='application/vnd.ms-excel')
#             response['Content-Disposition'] = 'attachment; filename=ExperimentalDesig4.xlsx'
#             xlsx_data = WriteToExcel()
#             response.write(xlsx_data)
#             return response
#         #if request.method == 'GET':
#             #form = EDForm(data=request.POST)
#             #if form.is_valid():
#              #   weather_period = ContactWizardSG.get_form_instance('1')
#         #if form.is_valid():
#          #   town_id = form.data['town']
#           #  town = Town.objects.get(pk=town_id)
#            # weather_period = Weather.objects.filter(town=town_id)
#             # if 'excel' in request.GET:
#             #     response = HttpResponse(content_type='application/vnd.ms-excel')
#             #     response['Content-Disposition'] = 'attachment; filename=Report.xlsx'
#             #     xlsx_data = WriteToExcel()
#             #     response.write(xlsx_data)
#             #     return response
#             #else:
#             #    form = WeatherForm()
#     else:
#         form = EDForm()
#     template_name = "project-regis_oo.html"
#     context = {
#             'form': form,
#       #  'town': town,
#             'weather_period': weather_period,
#     }             
#     return render(request, template_name, weather_period) 

  
    
#class UserRegistrationView(TemplateView):
#	form_class = UserForm
#	template_name = 'project-registration.html'
	#success_url = "/project-registration/"


# class CustomerRegistrationView(CreateView):
# 	#url = '/project-registration-2/'
# 	#permanent = False
# 	form_class = CustomerForm
# 	template_name = 'project-registration.html'

# 	# def get_redirect_url(self, *args, **kwargs):
# 	# 	userform1 = get_object_or_404(UserRegistrationView, pk=kwargs['pk'])
# 	# 	# post or update method as a post... defined in template
# 	# 	return super(UserRegistrationView, self).get_redirect_url(*args, **kwargs)
# 	# #template_name = 'project-registration.html'
# 	success_url = "/project-registration-2/"


	#success_url = reverse_lazy('back to calling url')
	
	#def form_valid(self, form):
	#	instance = form.save()
     #	if redirect:
     #		self.success_url = redirect()
     #	return super(RegistrationView, self).form_valid(form)


	#return HttpResponseRedirect("/project-registration")
	# def get_form_kwargs(self, **kwargs):
	# 	kwargs = super(RegistrationView, self).get_form_kwargs()
 #        redirect = self.request.GET.get('next')
 #        if redirect:
 #            if 'initial' in kwargs.keys():
 #                kwargs['initial'].update({'next': redirect})
 #            else:
 #                kwargs['initial'] = {'next': redirect}
 #        return kwargs

 #    def form_invalid(self, form):
 #        import pdb;pdb.set_trace()  # debug example
 #        # inspect the errors by typing the variable form.errors
 #        # in your command line debugger. See the pdb package for
 #        # more useful keystrokes
 # #        return super(RegistrationView, self).form_invalid(form)
 # 	def form_valid(self, form):
 # 		#redirect = form.cleaned_data.get('next')
 #    	instance = form.save
 #    	if redirect:
 #    		self.success_url = redirect()
 #    	return super(RegistrationView, self).form_valid(form)
 #	def update(request):
# 		sampleForm = SampleForm()
# 		return render(request, 'project-registration.html', sampleForm)

class AnalysisRegistrationView(CreateView):
	form_class = AnalysisForm
	template_name = 'project-registration.html'
	success_url = "/project-registration-3/"

# class AnalysisRegistrationView2(CreateView):
# 	form_class = AnalysisForm2
# 	template_name = 'project-registration.html'
# 	success_url = "/project-registration-3/"

# class ExperimentalDesignRegistrationView(CreateView):
# 	form_class = ExperimentalDesignForm
# 	template_name = 'project-registration.html'
# 	success_url = "/"

# class SampleSetRegistrationView(CreateView):
# 	form_class = SampleFormSet
# 	template_name = 'project-registration.html'
# 	success_url = "/"

#class SampleFormSetView(CreateView):
#	form_class = SampleFormSet
#	template_name
def manage_users(request):
	SampleFormSet = formset_factory(SampleForm)

	if request.method=="POST":
		formset = SampleFormSet(data=request.POST)
		if formset.is_valid():
			formset.save()
	else:
		formset = SampleFormSet()
	return render(request,"project-registration-sampleset.html",{"formset":formset})



# class ExpDesignRegistrationView(CreateView):
# 	form_class = ExpDesignForm
# 	template_name = 'project-registration.html'
# 	success_url = "/"

#
#import io
#from django.http import StreamingHttpResponse
from django.views.generic import View
#import xlsxwriter
from django.http import JsonResponse
class StatesView(View):
    def get(self, request, *args, **kwargs):
        statesoutfile ="/home/pportal/dev2Sep18/prcsite/vibproteomicscore/static/PRCCMBPSB_States.json" 
        with open(statesoutfile) as data_file:
            data_loaded = json.load(data_file)
            print(type(data_loaded["Waiting"]))
            return render(request, 'chartjs.html',data_loaded)
            # return render(request, 'chartjs.html',{'Waiting':data_loaded['Waiting'],
            #                                         'Processed':data_loaded['Processed']})

def get_data(request, *args, **kwargs):
    data = {
        "Sample Preparation":40,
        "LC-MS/MS":32,

    }
    return JsonResponse(data)
