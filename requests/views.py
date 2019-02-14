# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
#####from django.core.urlresolvers import reverse
from django.urls import reverse
from django.conf import settings
from youtrack.connection import Connection
#from django.contrib.auth import logout
#from django.views.generic import RedirectView

# if form.is_valid():
#     save_it = form.save(commit=False)
#     save_it.save()
#     #send_mail(subject, message, from_email, to_list, fail_silently=False)
#     subject = 'Thank you for your'
#     message = 'Welcome to ,,, we very much appeiate. we wil be in touch soon'
#     from_email=settings.EMAIL_HOST_USER
#     to_list = [settings.EMAIL_HOST_USER]
#     send_mail(subject, message, from_email, to_list, fail_silently=False)

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.http import is_safe_url
####from django.utils.http import is_safe_url
###from django.contrib.auth.forms import AuthenticationForm
###from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login

from django.views.generic import TemplateView, CreateView, FormView, ListView,RedirectView
from django.views.generic.detail import SingleObjectMixin 
from django.views.generic.base import TemplateResponseMixin
from django.contrib.auth import authenticate, login, logout
#from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import User#,Profile
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

#from .forms import CustomerForm, AnalysisForm,ExpDesignForm
#from .forms import UserForm, AnalysisForm, ExperimentalDesignForm
from django.forms import formset_factory
#from .forms import CustomerForm, AnalysisForm,Specimen_SGForm
#from .forms import CustomerForm, AnalysisForm,Specimen_SGForm,Specimen_APMSForm,Specimen_PTMForm, Specimen_GBForm,LoginForm, ExperimentForm, EDForm
from .forms import AnalysisForm,LoginForm, CustomerForm
from .forms import Specimen_APMSForm, Specimen_SGForm,Specimen_PTMForm, ExperimentForm,ExperimentPTMForm,ExperimentAPMSForm, EDForm,TOUForm
from formtools.wizard.views import SessionWizardView
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from .excel_utils import WriteToExcel
from .excel_utilsapms import WriteToExcel2
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.mail import send_mail
#import logging
#logr=logging.getlogger(__name__)

import os
from django.core.mail import send_mail

import sys
#sys.path.insert(0, '/home/pportal/dev2/src/lib/python2.7/site-packages/youtrack/')
# authenticating
import http.client, urllib.request, urllib.error

#import socks
from youtrack import connection
import csv
#import logging
##logr=logging.getlogger(__name__)
#from django.contrib.formtools.wizard.views import SessionWizardView

from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings

# def index(request):
#     return render(request, 'ss.html')


# class CWizard(SessionWizardView):
#     def done(self, form_list, **kwargs):
#       return render(self.request, 'donee.html', {
#       'form_data': [form.cleaned_data for form in form_list],
#       })

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


class LogoutView(RedirectView):
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
        if self.request.user.is_authenticated():
            logout(self.request)
        return super(LogoutView, self).get_redirect_url(*args, **kwargs)
# def login_page(request):
# 	if user is not None:
# 		login(request,user)
# 		try:
# 			del request.session

#@login_required
#@transaction.atomic

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

          

class ContactWizard(SessionWizardView):

    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT,'dbs'))
    #form_list = 
    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]
    def done(self, form_list,form_dict, **kwargs):
        analysis = [form.cleaned_data for form in form_list]
        # file field
        print(type(form_list))
        #form_list=
        upload_file = form_list[2].cleaned_data['Nb_samples']
        yt = connection.Connection(url='https://youtrack.ugent.be', api_key='perm:cHJjc2l0ZQ==.cHJjc2l0ZS10b2s=.XCNRP5yqauYkjFiFzj2VGYybpS3DJy')
        yt.execute_command("PRC-321", "No_Samples 19", group="PRC-website")
        return render(self.request,'done.html',{
            'form_data': analysis[0],
            'analysisd':form_dict,
            'upload_file' : upload_file,
            })
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
    #def process_form_data(form_list):
     #   form_data = [form.get_cleaned_data for form in form_list] 
      #  return form_data
        #logr.debug(form_data[0])['subject']
        #logr.debug(form_data[1])['sender']
        #logr.debug(form_data[2])['message']
    def done(self, form_list,form_dict, **kwargs):
        #form_list = [CustomerForm, AnalysisForm, Specimen_SGForm]
        #form_list = [AnalysisForm, Specimen_SGForm, ExperimentForm]
        #form_list = [AnalysisForm, Specimen_SGForm]
       ## form_data = process_form_data(form_list)
        #return form_data
       ## return render("done.html",{'form_data':form_data})
       # list of dictionaries of results
        analysis = [form.cleaned_data for form in form_list]
        #formnames = form_dict.keys()
        #print(formnames)
        # file field
        formtitles = ["User details", "Analysis overview", "Sample information", "Experimental Design information",
        "Experimental Design sheet"]
        formdict=dict()
        for i in range(len(formtitles)):
            formdict[formtitles[i]]=analysis[i]
        print('formdict' + str(formdict))
        #fieldvalues = [value for value in form_dict.values()]
        #print(fieldvalues)
        # is an odict structure with attributes fields and  
        # dict maxi
        #dictforms = 

        #form_list=
        # if form_list[2].cleaned_data['Sequence_Database_File']:
        #     upload_file = form_list[2].cleaned_data['Sequence_Database_File']
        # else:
        #     upload_file = ['No Sequence_Database_File']
        # if form.is_valid():
#     save_it = form.save(commit=False)
#     save_it.save()
#     #send_mail(subject, message, from_email, to_list, fail_silently=False)
        #subject = '[VIB Proteomics Core, Project registration confirmation] ' + formdict.
        #html_message = '<p>Thank you for registering your proteomics project!</p><p>Please find below a review of the project registration information, as well as a copy of our Terms of Use.</p><p>Your project reference: PRC-20</p></br><hr><h3>Sample submission procedure</h3><p>Please visit our sample shipping guidelines <a href="http://127.0.0.1:8000/sampledelivery">page</a>.</p><p>Before sending the samples, please contact <a href="mailto:delphi.vanhaver@vib-ugent.be">Delphi Van Haver</a> from our team. She will help you pick a good time for the shipment.</p></br><hr><h3>Getting notified about your project status</h3><ul><li>Once your samples arrive to our facility, you will get an email notification.</li><li>Each proteomics project gets a person responsible from our team. He/she will be your main contact point at the Core. The project responsible will get in touch to send you your proteomics results and data analysis report and, whenever needed, to discuss technical details associated with the project.</li><li>To check your project status, please visit <a href="http://127.0.0.1:8000/project-info">this page</a>.</li></ul></br></br><p>Best regards,</p><p>The VIB Proteomics Core</p>'
        #message='<p>Thank you for registering your proteomics project!</p><p>Please find below a review of the project registration information, as well as a copy of our Terms of Use.</p><p>Your project reference: PRC-20</p></br><hr><h3>Sample submission procedure</h3><p>Please visit our sample shipping guidelines <a href="http://127.0.0.1:8000/sampledelivery">page</a>.</p><p>Before sending the samples, please contact <a href="mailto:delphi.vanhaver@vib-ugent.be">Delphi Van Haver</a> from our team. She will help you pick a good time for the shipment.</p></br><hr><h3>Getting notified about your project status</h3><ul><li>Once your samples arrive to our facility, you will get an email notification.</li><li>Each proteomics project gets a person responsible from our team. He/she will be your main contact point at the Core. The project responsible will get in touch to send you your proteomics results and data analysis report and, whenever needed, to discuss technical details associated with the project.</li><li>To check your project status, please visit <a href="http://127.0.0.1:8000/project-info">this page</a>.</li></ul></br></br><p>Best regards,</p><p>The VIB Proteomics Core</p>'
        #{analysis[1]['Project_ID']:'Project_ID', 
        Project_ID = analysis[0]['Project_ID']
        Contact_Person = analysis[0]['Name'].split(',')[0]
        subject = '[VIB Proteomics Core, Project registration confirmation] '+analysis[0]['Project_ID']
        message = render_to_string('confirmation_email.txt', {'formdict': formdict,'Project_ID': Project_ID,'Contact_Person': Contact_Person})
        html_message = render_to_string('confirmation_email.html', {'formdict': formdict,'Project_ID': Project_ID,'Contact_Person': Contact_Person})
        from_email=settings.EMAIL_HOST_USER
        to_list = [settings.EMAIL_HOST_USER]
        send_mail(subject, message, from_email, to_list, html_message=html_message, fail_silently=False)
        #yt = Connection(url='http://127.0.0.1:8112', login='prcsite', token='perm:cHJjc2l0ZQ==.cHJjc2l0ZS10b2s=.XCNRP5yqauYkjFiFzj2VGYybpS3DJy')
        yt = Connection(url='https://youtrack.ugent.be', token='perm:cHJjc2l0ZQ==.cHdlYi10b2s=.epNpU5rPRZxq3rYGhAR3tZozc8w0am')
        summary = analysis[0]['Project_ID']# + "-" +  + "-" + Analysis_Type + "-" + keywords[0]
        Project_ID = "PRC-321"
        #try:
        if analysis[0]['Other_institution'] is not None:
          Other_institution = analysis[0]['Other_institution']
        else:
          Other_institution = ''
        if analysis[2]['Sequence_database_name'] is not None:
          Sequence_database_name = analysis[2]['Sequence_database_name']
        else:
          Sequence_database_name = ''
        if analysis[2]['Sequence_database_file'] is not None:
          Sequence_database_file= analysis[2]['Sequence_database_file']
        else:
          Sequence_database_file = ''
        if analysis[3]['Isotopic_labeling_details'] is not None:
          Isotopic_labeling_details = analysis[3]['Isotopic_labeling_details']
        else:
          Isotopic_labeling_details = ''
        #if analysis[3]['Other_information'] is not None:
        #  Other_information = analysis[3]['Other_information']
        #else:
        #  Other_information = ''
        description = "#User Details\n\nInstitute/Organization: " + str(analysis[0]['Affiliation']) + "\nOther institution" +Other_institution + "\nAddress: " + analysis[0]['Address'] + "\n\n#Analysis overview\nExperiment Summary: " + analysis[1]['Project_summary']+"\nProject_title: " + analysis[1]['Project_title'] + "\nData_Analysis: "+ str(analysis[1]['Data_analysis']) + "\n\n#Sample information" \
              + "\nSample_Species: "+ analysis[2]['Species'] + '\nSequence_Database_Public_Availability: ' + str(analysis[2]['Sequence_Database_Public_Availability']) \
              + "\nSequence_Database_Name:" + Sequence_database_name+"\nSequence_database_file:" + str(Sequence_database_file) + "\n\n#Experimental Design information\nConditions_to_compare: " + analysis[3]['Conditions_to_compare'] +"\nIsotopic labeling: " + str(analysis[3]['Isotopic_labeling'])+ "\nIsotopic labeling details: " + Isotopic_labeling_details + "\nOther information: " \
              + " " #+ Other_information
        yt.update_issue(Project_ID, summary = "ContactPerson-GroupLeader-analysistype-keyword1",
                description=description)
        # fields and tags (structured annotations)
        # Affiliation_Type = analysis[0]['Affiliation_Type']
        #Affiliation = analysis[0]['Affiliation']
    #     if Affiliation_Type=='Academic':
    #         if Affiliation == 'VIB':
    #             Study_Type = 'VIB'
    #         else:
    #             Study_Type = 'Academic'
    #     else:
    #         Study_Type = 'Non-Academic'
    #     Analysis_type = analysis[1]['Analysis_type']
    #     ats= {'shotgun':'shotgun_analysis',
    # 'APMS':'affinity-purification MS (AP-MS)', 
    # 'PTMs':'PTM analysis',
    # 'Virotrap':'Virotrap',
    # 'gelband':'protein gel band analysis',
    # 'proteinmass':'protein mass determination',
    # 'prm':'PRM',
    # 'srm':'SRM',
    # 'dia':'DIA',
    # 'other':'Other'}
    #     for at in Analysis_type:
    #         print(ats[at])
    #         yt.execute_command(Project_ID, "Analysis_Type " + ats[at])
        yt.execute_command(Project_ID, "Contact_Person " + analysis[0]['Name'])
        #yt.execute_command(Project_ID, "GroupLeader "+ str(analysis[0]['Group_Leader']  ))
        #yt.execute_command(Project_ID, "Analysis_Type " +  analysis[1]['Analysis_type'])
        yt.execute_command(Project_ID, "Study_Type Academic") #+ str(analysis[0]['Affiliation_Type']) )
        yt.execute_command(Project_ID, "No_Samples "+ str(analysis[3]['Nb_samples']))

        yt.execute_command(Project_ID, "Project_Title "+ analysis[1]['Project_title'])
        if not analysis[1]['Data_analysis']:
            yt.execute_command(Project_ID, "tag nDA")
        #upload_file = form_list[2].cleaned_data['Sequence_database_file']
        #upload_file = "media/Cumulative2.png"
        #yt.create_attachment("PRC-321",name='Training_logo.png',content=open(upload_file, "rb"),author_login ="prcsite")
        #yt.create_attachment("PRC-321",name='Training_logo.png',content=open(upload_file, "rb"),author_login ="prcsite")
        ##if not analysis[1]['Data_analysis']:
        ##    yt.execute_command(Project_ID, "tag nDA")
        ##if analysis[3]['Isotopic_labeling']=='True':
        ##    yt.execute_command(Project_ID, "tag Isotopic_labelling") # can be left empty and we'll fill in
        #send_mail(subject, message=message, html_message=html_message, from_email, to_list, fail_silently=False)
        #upload_file = form_list[4].cleaned_data['ED_file']
        #yt = Connection(url='http://127.0.0.1:8112', login='prcsite', token='perm:cHJjc2l0ZQ==.cHJjc2l0ZS10b2s=.XCNRP5yqauYkjFiFzj2VGYybpS3DJy')
        #yt = connection.Connection(url='https://youtrack.ugent.be', login='prcsite', token='perm:cm9vdA==.Y29sbGE=.FfNqw1Jw4mi7UgOnAkm2Sh9DldgIbt')
        #yt.execute_command("PRC-321", "No_Samples 27", group="PRC-website")

        # formdict
        # {'User details': {'Project_ID': 'PRC-20', 'Name': 'Anne Breitusch', 'Email': 'teresa.maia@vib-ugent.be', 
        # 'Group_Leader': 'Claudia Berts', 'Affiliation': 'VIB', 'Address': 'asaa', 'Affiliation_Type': 'Industry'}, 

        # 'Analysis overview': {'Project_summary': 'weqw', 'Project_keywords': 'autophagy', 'Analysis_type': ['PTMs'],
        #  'Analysis_type2': [], 'Data_analysis': True}, 
        #  'Sample information': {'Species': 'asd', 'Sequence_Database_Public_Availability': 'True', 
        #  'Sequence_database_name': 'asd', 'Sequence_database_file': None, 'Sample_Type': 'asd', 'Buffer_composition': 'asd'},
        #   'Experimental Design information':
        #    {'Experimental_conditions': 'asd, asda', 'Conditions_to_compare': 'adadasd', 
        #    'Nb_replicates_per_condition': 3, 'Nb_samples': 6, 'Sample_Name': '', 'Isotopic_labeling': 'False',
        #     'Isotopic_labeling_details': 'qewq', 'Other_infomation': 'qew'}, 
        #     'Experimental Design sheet': {'EDfile': <UploadedFile: requirements502.txt (text/plain)>,
        #      'TermsOfUse': True}}

        return render(self.request,'done.html',{
            'formdict': formdict,
            #'analysisd':form_dict,
            #'formnames':formnames,
            #'formtitles':formtitles,
            #'fieldnames':fieldvalues,
            #'upload_file' : upload_file,
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
            xlsx_data = WriteToExcel(prev_data)
            #response.write(xlsx_data)
            #get_cleaned_data_for_step
            #samplename = prev_data.get('Generic_Sample_Name','')
            #return samplename
            return self.initial_dict.get(step, prev_data)
            #return self.initial_dict.get(step, {samplename:'samplename'})

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
        #form_list = [CustomerForm, AnalysisForm, Specimen_SGForm]
        #form_list = [AnalysisForm, Specimen_SGForm, ExperimentForm]
        #form_list = [AnalysisForm, Specimen_SGForm]
       ## form_data = process_form_data(form_list)
        #return form_data
       ## return render("done.html",{'form_data':form_data})
       # list of dictionaries of results
        analysis = [form.cleaned_data for form in form_list]
        #formnames = form_dict.keys()
        #print(formnames)
        # file field
        formtitles = ["User details", "Analysis overview", "Sample information", "Experimental Design information",
        "Experimental Design sheet"]
        formdict=dict()
        for i in range(len(formtitles)):
            formdict[formtitles[i]]=analysis[i]
        print('formdict' + str(formdict))
        #fieldvalues = [value for value in form_dict.values()]
        #print(fieldvalues)
        # is an odict structure with attributes fields and  
        Project_ID = analysis[0]['Project_ID']
        Contact_Person = analysis[0]['Name'].split(',')[0]
        subject = '[VIB Proteomics Core, Project registration confirmation] '+analysis[0]['Project_ID']
        message = render_to_string('confirmation_email.txt', {'formdict': formdict,'Project_ID': Project_ID,'Contact_Person': Contact_Person})
        html_message = render_to_string('confirmation_email.html', {'formdict': formdict,'Project_ID': Project_ID,'Contact_Person': Contact_Person})
        from_email=settings.EMAIL_HOST_USER
        to_list = [settings.EMAIL_HOST_USER]
        send_mail(subject, message, from_email, to_list, html_message=html_message, fail_silently=False)
        #yt = Connection(url='http://127.0.0.1:8112', login='prcsite', token='perm:cHJjc2l0ZQ==.cHJjc2l0ZS10b2s=.XCNRP5yqauYkjFiFzj2VGYybpS3DJy')
        yt = Connection(url='https://youtrack.ugent.be', token='perm:cHJjc2l0ZQ==.cHdlYi10b2s=.epNpU5rPRZxq3rYGhAR3tZozc8w0am')
        summary = analysis[0]['Project_ID']# + "-" +  + "-" + Analysis_Type + "-" + keywords[0]
        Project_ID = "PRC-321"
        description = "#User Details\nInstitute/Organization: " + analysis[0]['Affiliation'] + "\nAddress: " + analysis[0]['Address'] + "\n#Analysis overview\nExperiment Summary: " + analysis[1]['Project_summary']+"\nProject_keywords: " + analysis[1]['Project_keywords'] + "\nData_Analysis: "+ str(analysis[1]['Data_analysis']) + "\n#Sample information \n" \
              + "Sample_Species: "+ analysis[2]['Species'] + '\nSequence_Database_Public_Availability: ' + str(analysis[2]['Sequence_Database_Public_Availability']) \
              + "\nSequence_Database_Name:" + analysis[2]['Sequence_database_name']+"\nSequence_database_file:" + str(analysis[2]['Sequence_database_file']) + "\n#Experimental Design information\nConditions_to_compare: " + analysis[3]['Conditions_to_compare'] +"\nIsotopic labeling: " + analysis[3]['Isotopic_labeling']+ "\nIsotopic labeling details: " + str(analysis[3]['Isotopic_labeling_details']) \
              + "\nOther information: " #+ str(analysis[3]['Other_information'])
        yt.update_issue(Project_ID, summary = "ContactPerson-GroupLeader-analysistype-keyword1",
                description=description)
        # fields and tags (structured annotations)
        Affiliation_Type = analysis[0]['Affiliation_Type']
        Affiliation = analysis[0]['Affiliation']
        if Affiliation_Type=='Academic':
            if Affiliation == 'VIB':
                Study_Type = 'VIB'
            else:
                Study_Type = 'Academic'
        else:
            Study_Type = 'Non-Academic'
        Analysis_type = analysis[1]['Analysis_type']
        ats= {'shotgun':'shotgun_analysis',
    'APMS':'affinity-purification MS (AP-MS)', 
    'PTMs':'PTM analysis',
    'Virotrap':'Virotrap',
    'gelband':'protein gel band analysis',
    'proteinmass':'protein mass determination',
    'prm':'PRM',
    'srm':'SRM',
    'dia':'DIA',
    'other':'Other'}
        for at in Analysis_type:
            print(ats[at])
           # yt.execute_command(Project_ID, "Analysis_Type " + ats[at])
        yt.execute_command(Project_ID, "Contact_Person " + analysis[0]['Name'])
        #yt.execute_command(Project_ID, "Contact_Email " + analysis[0]['Email'] )
        yt.execute_command(Project_ID, "GroupLeader "+ str(analysis[0]['Group_Leader']  ))
        #yt.execute_command(Project_ID, "Analysis_Type " +  analysis[1]['Analysis_type'])
        yt.execute_command(Project_ID, "Study_Type " + Study_Type) #+ str(analysis[0]['Affiliation_Type']) )
        yt.execute_command(Project_ID, "No_Samples "+ str(analysis[3]['Nb_samples']))
        yt.execute_command(Project_ID, "Project_Title "+ analysis[1]['Project_title'])
        if not analysis[1]['Data_analysis']:
            yt.execute_command(Project_ID, "tag nDA")
        upload_file = form_list[2].cleaned_data['Sequence_database_file']
        yt.create_attachment("PRC-321",name='Training_logo.png',content=open(upload_file, "rb"),author_login ="prcsite")
        if analysis[3]['Isotopic_labeling']=='True':
            yt.execute_command(Project_ID, "tag Isotopic_labelling") # can be left empty and we'll fill in
        #     upload_file = form_list[2].cleaned_data['Sequence_Database_File']
        # else:
        #     upload_file = ['No Sequence_Database_File']
        #upload_file = form_list[4].cleaned_data['ED_file']
        #yt = Connection(url='http://127.0.0.1:8112', login='prcsite', token='perm:cHJjc2l0ZQ==.cHJjc2l0ZS10b2s=.XCNRP5yqauYkjFiFzj2VGYybpS3DJy')
        #yt = connection.Connection(url='https://youtrack.ugent.be', login='prcsite', token='perm:cm9vdA==.Y29sbGE=.FfNqw1Jw4mi7UgOnAkm2Sh9DldgIbt')
        #yt.execute_command("PRC-321", "No_Samples 27", group="PRC-website")
        return render(self.request,'done.html',{
            'formdict': formdict,
            #'analysisd':form_dict,
            #'formnames':formnames,
            #'formtitles':formtitles,
            #'fieldnames':fieldvalues,
            #'upload_file' : upload_file,
            })
    def get_form_initial(self, step):
        """
        Set projet id and email for step1
        Set extra parameter for step2, which is from clean data of step1.
        """
        initial = self.initial_dict.get(step, {})
        if step=='0':
            form_class=self.form_list[step]
            Project_ID = self.request.user.profile.Project_ID
            Email = self.request.user.email
            #Analysis_Type = self.request.user.profile.Main_Analysis_Type
            initial.update({'Project_ID':Project_ID, 'Email':Email})
            return initial
        #if step == '3':
         #   form_class = self.form_list[step]
            #Issue = self.request.user.profile.Issue + '-S' 
            #form_class['Generic_Sample_Name'] = self.request.user.profile.Issue 
            #initial.update({'Generic_Sample_Name':Analysis_Type})
           # return initial
        if step == '4':
            form_class = self.form_list[step]
            #print(dir(self.storage))
            prev_data2 = self.storage.get_step_data('2')
            #print(str(prev_data2))
            prev_data3 = self.storage.get_step_data('3')
            #print(str(prev_data3))
            prev_data = {**prev_data2, **prev_data3}
            prev_data["PID"] = self.request.user.profile.Project_ID
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
        #form_list = [CustomerForm, AnalysisForm, Specimen_SGForm]
        #form_list = [AnalysisForm, Specimen_SGForm, ExperimentForm]
        #form_list = [AnalysisForm, Specimen_SGForm]
       ## form_data = process_form_data(form_list)
        #return form_data
       ## return render("done.html",{'form_data':form_data})
       # list of dictionaries of results

        analysis = [form.cleaned_data for form in form_list]
        
        #formnames = form_dict.keys()
        #print(formnames)
        # file field
        formtitles = ["User details", "Analysis overview", "Sample information", "Experimental Design information",
        "Experimental Design sheet"]
        formdict=dict()
        for i in range(len(formtitles)):
            formdict[formtitles[i]]=analysis[i]
        print('formdict' + str(formdict))
        #fieldvalues = [value for value in form_dict.values()]
        #print(fieldvalues)
        # is an odict structure with attributes fields and  
        # dict maxi
        #dictforms = 
        Project_ID = analysis[0]['Project_ID']
        Contact_Person = analysis[0]['Name'].split(',')[0]
        subject = '[VIB Proteomics Core, Project registration confirmation] '+analysis[0]['Project_ID']
        message = render_to_string('confirmation_email.txt', {'formdict': formdict,'Project_ID': Project_ID,'Contact_Person': Contact_Person})
        html_message = render_to_string('confirmation_email.html', {'formdict': formdict,'Project_ID': Project_ID,'Contact_Person': Contact_Person})
        from_email=settings.EMAIL_HOST_USER
        to_list = [settings.EMAIL_HOST_USER]
        send_mail(subject, message, from_email, to_list, html_message=html_message, fail_silently=False)
        #yt = Connection(url='http://127.0.0.1:8112', login='prcsite', token='perm:cHJjc2l0ZQ==.cHJjc2l0ZS10b2s=.XCNRP5yqauYkjFiFzj2VGYybpS3DJy')
        yt = Connection(url='https://youtrack.ugent.be', token='perm:cHJjc2l0ZQ==.cHdlYi10b2s=.epNpU5rPRZxq3rYGhAR3tZozc8w0am')
        summary = analysis[0]['Project_ID']# + "-" +  + "-" + Analysis_Type + "-" + keywords[0]
        Project_ID = "PRC-321"
        description = "#User Details\nInstitute/Organization: " + analysis[0]['Affiliation'] + "\nAddress: " + analysis[0]['Address'] + "\n#Analysis overview\nExperiment Summary: " + analysis[1]['Project_summary']+"\nProject_title: " + analysis[1]['Project_title'] + "\nData_Analysis: "+ str(analysis[1]['Data_analysis']) + "\n#Sample information \n" \
              + "Sample_Species: "+ analysis[2]['Species'] \
              + "\n#Experimental Design information\nConditions_to_compare: " + analysis[3]['Conditions_to_compare'] \
              + "\nOther information: " #+ str(analysis[3]['Other_information'])
        yt.update_issue(Project_ID, summary = "ContactPerson-GroupLeader-analysistype-keyword1",
                description=description)
        # fields and tags (structured annotations)
        #Affiliation_Type = analysis[0]['Affiliation_Type']
        # Affiliation = analysis[0]['Affiliation']
        # if Affiliation_Type=='Academic':
        #     if Affiliation == 'VIB':
        #         Study_Type = 'VIB'
        #     else:
        #         Study_Type = 'Academic'
        # else:
        #     Study_Type = 'Non-Academic'
    #     Analysis_type = analysis[1]['MainAnalysis_type']
    #     ats= {'shotgun':'shotgun_analysis',
    # 'APMS':'affinity-purification MS (AP-MS)', 
    # 'PTMs':'PTM analysis',
    # 'Virotrap':'Virotrap',
    # 'gelband':'protein gel band analysis',
    # 'proteinmass':'protein mass determination',
    # 'prm':'PRM',
    # 'srm':'SRM',
    # 'dia':'DIA',
    # 'other':'Other'}
    #     for at in Analysis_type:
    #         print(ats[at])
           # yt.execute_command(Project_ID, "Analysis_Type " + ats[at])
        yt.execute_command(Project_ID, "Contact_Person " + analysis[0]['Name'])
        yt.execute_command(Project_ID, "Contact_Email " + analysis[0]['Email'] )
        yt.execute_command(Project_ID, "GroupLeader "+ str(analysis[0]['Group_Leader']  ))
        #yt.execute_command(Project_ID, "Analysis_Type " +  analysis[1]['Analysis_type'])
        yt.execute_command(Project_ID, "Study_Type " + Study_Type) #+ str(analysis[0]['Affiliation_Type']) )
        yt.execute_command(Project_ID, "No_Samples "+ str(analysis[3]['Nb_samples']))
        #kw1= analysis[1]['Project_keywords'].replace(' ','').split(',')[0]
        yt.execute_command(Project_ID, "Project_Title "+ analysis[1]['Project_title'])
        if not analysis[1]['Data_analysis']:
            yt.execute_command(Project_ID, "tag nDA")
        upload_file = form_list[2].cleaned_data['Sequence_database_file']
        yt.create_attachment("PRC-321",name='Training_logo.png',content=open(upload_file, "rb"),author_login ="prcsite")
        #if analysis[3]['Isotopic_labeling']=='True':
         #   yt.execute_command(Project_ID, "tag Isotopic_labelling") # can be left empty and we'll fill in        # if form_list[2].cleaned_data['Sequence_Database_File']:
        #     upload_file = form_list[2].cleaned_data['Sequence_Database_File']
        # else:
        #     upload_file = ['No Sequence_Database_File']
        
        #upload_file = form_list[4].cleaned_data['ED_file']
        #yt = Connection(url='http://127.0.0.1:8112', login='prcsite', token='perm:cHJjc2l0ZQ==.cHJjc2l0ZS10b2s=.XCNRP5yqauYkjFiFzj2VGYybpS3DJy')
        #yt = connection.Connection(url='https://youtrack.ugent.be', login='prcsite', token='perm:cm9vdA==.Y29sbGE=.FfNqw1Jw4mi7UgOnAkm2Sh9DldgIbt')
        #yt.execute_command("PRC-321", "No_Samples 27", group="PRC-website")

        return render(self.request,'done.html',{
            'formdict': formdict,
            #'analysisd':form_dict,
            #'formnames':formnames,
            #'formtitles':formtitles,
            #'fieldnames':fieldvalues,
            #'upload_file' : upload_file,
            })
    
    def get_form_initial(self, step):
        """
        Set projet id and email for step1
        Set extra parameter for step2, which is from clean data of step1.
        """
        initial = self.initial_dict.get(step, {})
        if step=='0':
            form_class=self.form_list[step]
            Project_ID = self.request.user.profile.Project_ID
            Email = self.request.user.email
            #Analysis_Type = self.request.user.profile.Main_Analysis_Type
            initial.update({'Project_ID':Project_ID, 'Email':Email})
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
            prev_data2 = self.storage.get_step_data('2')
            #print(str(prev_data2))
            prev_data3 = self.storage.get_step_data('3')
            #print(str(prev_data3))
            prev_data = {**prev_data2, **prev_data3}
            prev_data["PID"] = self.request.user.profile.Project_ID
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


# class ContactWizardGB(SessionWizardView):
#     instance=None
#     file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT,'seqdbs'))
#     def get_template_names(self):
#         return [TEMPLATESGB[self.steps.current]]
#     #def process_form_data(form_list):
#      #   form_data = [form.get_cleaned_data for form in form_list] 
#       #  return form_data
#         #logr.debug(form_data[0])['subject']
#         #logr.debug(form_data[1])['sender']
#         #logr.debug(form_data[2])['message']
#     def done(self, form_list,form_dict, **kwargs):
#         #form_list = [CustomerForm, AnalysisForm, Specimen_SGForm]
#         #form_list = [AnalysisForm, Specimen_SGForm, ExperimentForm]
#         #form_list = [AnalysisForm, Specimen_SGForm]
#        ## form_data = process_form_data(form_list)
#         #return form_data
#        ## return render("done.html",{'form_data':form_data})
#        # list of dictionaries of results

#         analysis = [form.cleaned_data for form in form_list]
        
#         #formnames = form_dict.keys()
#         #print(formnames)
#         # file field
#         formtitles = ["User details", "Analysis overview", "Sample information", "Experimental Design information",
#         "Experimental Design sheet"]
#         formdict=dict()
#         for i in range(len(formtitles)):
#             formdict[formtitles[i]]=analysis[i]
#         print('formdict' + str(formdict))
#         #fieldvalues = [value for value in form_dict.values()]
#         #print(fieldvalues)
#         # is an odict structure with attributes fields and  
#         # dict maxi
#         #dictforms = 

#         #form_list=
#         # if form_list[2].cleaned_data['Sequence_Database_File']:
#         #     upload_file = form_list[2].cleaned_data['Sequence_Database_File']
#         # else:
#         #     upload_file = ['No Sequence_Database_File']
        
#         #upload_file = form_list[4].cleaned_data['ED_file']
#         #yt = Connection(url='http://127.0.0.1:8112', login='prcsite', token='perm:cHJjc2l0ZQ==.cHJjc2l0ZS10b2s=.XCNRP5yqauYkjFiFzj2VGYybpS3DJy')
#         #yt = connection.Connection(url='https://youtrack.ugent.be', login='prcsite', token='perm:cm9vdA==.Y29sbGE=.FfNqw1Jw4mi7UgOnAkm2Sh9DldgIbt')
#         #yt.execute_command("PRC-321", "No_Samples 27", group="PRC-website")

#         return render(self.request,'done.html',{
#             'formdict': formdict,
#             #'analysisd':form_dict,
#             #'formnames':formnames,
#             #'formtitles':formtitles,
#             #'fieldnames':fieldvalues,
#             #'upload_file' : upload_file,
#             })
    
#     def get_form_initial(self, step):
#         """
#         Set projet id and email for step1
#         Set extra parameter for step2, which is from clean data of step1.
#         """
#         initial = self.initial_dict.get(step, {})
#         if step=='0':
#             form_class=self.form_list[step]
#             Project_ID = self.request.user.profile.Project_ID
#             Email = self.request.user.email
#             #Analysis_Type = self.request.user.profile.Main_Analysis_Type
#             initial.update({'Project_ID':Project_ID, 'Email':Email})
#             return initial
#         #if step == '3':
#          #   form_class = self.form_list[step]
#             #Issue = self.request.user.profile.Issue + '-S' 
#             #form_class['Generic_Sample_Name'] = self.request.user.profile.Issue 
#             #initial.update({'Generic_Sample_Name':Analysis_Type})
#             return initial
#         if step == '4':
#             form_class = self.form_list[step]
#             #print(dir(self.storage))
#             prev_data2 = self.storage.get_step_data('2')
#             #print(str(prev_data2))
#             prev_data3 = self.storage.get_step_data('3')
#             #print(str(prev_data3))
#             prev_data = {**prev_data2, **prev_data3}
#             prev_data["PID"] = self.request.user.profile.Project_ID
#             xlsx_data = WriteToExcel(prev_data)
#             #response.write(xlsx_data)
#             #get_cleaned_data_for_step
#             #samplename = prev_data.get('Generic_Sample_Name','')
#             #return samplename
#             return self.initial_dict.get(step, prev_data)
#             #return self.initial_dict.get(step, {samplename:'samplename'})


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




class ProjectInfoView(ListView):
    template_name = 'project-info.html'
    # @method_decorator(login_required)
    # def dispatch(self, *args, **kwargs):
    #     return super(ProjectInfoView, self).dispatch(*args, **kwargs)

    # def get_queryset(self):
    #     qs = Profile.objects.filter(user=self.request.user.profile.user)
    #     print(qs)
    #     print(dir(qs[0]))
    #def get_queryset(self, request, *args, **kwargs):
    def get_queryset(self):
        self.object=User.objects.filter(username=self.request.user.username)
        #self.object=self.get_object(queryset=User.objects.filter(user=self.request.user))
        return
        #return super().get(request,*args, **kwargs)

    #def get_object(queryset=None):
        #self.object=self.get_object(queryset=Profile.objects.filter(user=self.request.user.profile.user))
        #self.object=self.get_object(queryset=User.objects.filter(user=self.request.user))
        #return 
        #Profile.objects.filter(user=self.request.user.profile.user)
    
    #def get_queryset(self):
     #   return self.object.
      #  Profile.objects.filter(user=self.request.user.profile.user)

    def get_context_data(self,**kwargs):
        #url = static("PRC_issues_dailyreport2.csv")
        #print(url)
        context=super().get_context_data(**kwargs)
        with open("static-dev/PRC_issues_dailyreport2.csv", "r") as csvfile:
            csvfile_reader=csv.DictReader(csvfile)
            for row in csvfile_reader:
                if row["YouTrack_id"]==self.object[0].username:
                    context["Project_ID"] = row["YouTrack_id"]
                    context["State"] = row["State"]
                    context["Scheduling_State"] = row["SchedulingState"]
                    context["Median_wTime"] = row["Median_wTime"]
                    context["Min_wTime"] = row["Min_wTime"]
                    context["today"] = datetime.datetime.now().strftime("%A, %b, %d, %Y")
                    #today = context["today"]
                    pass
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
        with open("static-dev/PRC_issues_dailyreport2.csv", "r") as csvfile:
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
        with open("static-dev/PRC_issues_dailyreport2.csv", "r") as csvfile:
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



class SGView(CreateView):
    form_class = Specimen_SGForm
    template_name = 'project-regis_sg.html'
    #def get(self, request, *args, **kargs):
     #  context = {}
      # return render(request, 'project-regis_sg.html', context)


class SGView(CreateView):
    form_class = Specimen_SGForm
    template_name = 'project-regis_sg.html'
    #def get(self, request, *args, **kargs):
     #  context = {}
      # return render(request, 'project-regis_sg.html', context)
      

#
import io
from django.http import StreamingHttpResponse
from django.views.generic import View
import xlsxwriter


# def requestt_page(request):
#     weather_period = 's'
#     if request.method =='GET':
#         form = EDForm()
#         if "excel" in request.GET:
#             response = HttpResponse(content_type='application/vnd.ms-excel')
#             response['Content-Disposition'] = 'attachment; filename=ExperimentalDesign.xlsx'
#             xlsx_data = WriteToExcel()
#             response.write(xlsx_data)
#             return response
#     else:
#         form = EDForm()
#     template_name = "project-regis_oo.html"
#     context = {
#             'form': form,
#       #  'town': town,
#            # 'weather_period': weather_period,
#     }   
#     return render(request, template_name, context)       

# def requestt_page():
#     # Simulate a more complex table read.
#     return [[1, 2, 3],
#             [4, 5, 6],
#             [7, 8, 9]]


# class MyView(View):

#     def get(self, request):

#         # Create an in-memory output file for the new workbook.
#         output = io.BytesIO()

#         # Even though the final file will be in memory the module uses temp
#         # files during assembly for efficiency. To avoid this on servers that
#         # don't allow temp files, for example the Google APP Engine, set the
#         # 'in_memory' Workbook() constructor option as shown in the docs.
#         workbook = xlsxwriter.Workbook(output)
#         worksheet = workbook.add_worksheet()

#         # Get some data to write to the spreadsheet.
#         data = requestt_page()

#         # Write some test data.
#         for row_num, columns in enumerate(data):
#             for col_num, cell_data in enumerate(columns):
#                 worksheet.write(row_num, col_num, cell_data)

#         # Close the workbook before sending the data.
#         workbook.close()

#         # Rewind the buffer.
#         output.seek(0)

#         # Set up the Http response.
#         filename = 'django_simple.xlsx'
#         response = HttpResponse(
#             output,
#             content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
#         )
#         response['Content-Disposition'] = 'attachment; filename=%s' % filename

#         return response


# class ProjectInfoView(ListView):
#     #model = User
#     context=dict()
#     template_name = 'project-info.html'
#     @method_decorator(login_required)
#     def dispatch(self, *args, **kwargs):
#         return super(ProjectInfoView, self).dispatch(*args, **kwargs)

#     def get_queryset(self):
#         qs = Profile.objects.filter(user=self.request.user.profile.user)
#         print(qs)
#         print(dir(qs[0]))
#         #url = static("PRC_issues_dailyreport2.csv")
#         #print(url)
#         context=get_context_data(qs)
#         # with open("PRC_issues_dailyreport2.csv", "r") as csvfile:
#         #     csvfile_reader=csv.DictReader(csvfile)
#         #     for row in csvfile_reader:
#         #         if row["YouTrack_id"]==qs[0].Issue:
#         #             context["Issue"] = row["YouTrack_id"]
#         #             context["State"] = row["State"]
#         #             context["Scheduling_State"] = row["SchedulingState"]
#         #             context["today"] = datetime.datetime.now().strftime("%A, %b, %d, %Y")
#         #             today = context["today"]
#         #             pass
#         print(context)
#         return context

#         def get_context_data(self,**kwargs):
#         #url = static("PRC_issues_dailyreport2.csv")
#         #print(url)
#         context=super(ProjectInfoView, self).get_context_data(**kwargs)
#         with open("PRC_issues_dailyreport2.csv", "r") as csvfile:
#             csvfile_reader=csv.DictReader(csvfile)
#             for row in csvfile_reader:
#                 if row["YouTrack_id"]==qs[0].Issue:
#                     context["Issue"] = row["YouTrack_id"]
#                     context["State"] = row["State"]
#                     context["Scheduling_State"] = row["SchedulingState"]
#                     context["today"] = datetime.datetime.now().strftime("%A, %b, %d, %Y")
#                     today = context["today"]
#                     pass
#         print(context)
#         return context

    # def __init__(self,*args, **kwargs):
    #     super(ProjectInfoView, self).__init__(*args,**kwargs)
    #     self.queryset = User.objects.filter(user=self.request.user)
    #     context = super(ProjectInfoView, self).get_context_data(*args, **kwargs)
    #     context["today"] = datetime.datetime.now().strftime("%A, %b, %d, %Y")
        
    #     with open("PRC_issues_dailyreport2.csv", "r") as csvfile:
    #         csvfile_reader=csv.DictReader(csvfile)
    #         for row in csvfile_reader:
    #             if row["YouTrack_id"]==profile.Issue:
    #                 Issue = user.profile.Issue
    #                 State = row["State"]
    #                 Scheduling_State = row["Scheduling_State"]
    #     context["Issue"] = Issue
    #     context["State"] = State
    #     context["Scheduling_State"] = Scheduling_State
    #     return context 
    # def get_queryset(self):
    #     return User.objects.filter(user=self.request.user)

# class ProjectInfoView(TemplateView, ListView):
#    template_name = 'project-info.html'
#    def get_context_data(self,*args, **kwargs):
#        context = super(ProjectInfoView, self).get_context_data(*args, **kwargs)
#        context["today"] = datetime.datetime.now().strftime("%A, %b, %d, %Y")
#        user = User.objects.filter(user=self.request.user)
#        context["Issue"] = user.Issue
#         with open("PRC_issues_dailyreport2.csv", "r") as csvfile:
#             csvfile_reader=csv.DictReader(csvfile)
#             for row in csvfile_reader:
#                 if row["YouTrack_id"]==user.Issue:
#                    Issue = user.Issue
#                    State = row["State"]
#                    Scheduling_State = row["Scheduling_State"]
#         context["Issue"] = Issue
#         context["State"] = State
#         context["Scheduling_State"] = Scheduling_State
#         return context 
#     def get_queryset(self):
#        return User.objects.filter(user=self.request.user)