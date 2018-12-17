# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
#####from django.core.urlresolvers import reverse
from django.urls import reverse
#from django.contrib.auth import logout
#from django.views.generic import RedirectView

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.http import is_safe_url
####from django.utils.http import is_safe_url
###from django.contrib.auth.forms import AuthenticationForm
###from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login

from django.views.generic import TemplateView, CreateView, FormView
from django.views.generic.base import TemplateResponseMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

#from .forms import CustomerForm, AnalysisForm,ExpDesignForm
#from .forms import UserForm, AnalysisForm, ExperimentalDesignForm
from django.forms import formset_factory
#from .forms import CustomerForm, AnalysisForm,Specimen_SGForm
from .forms import AnalysisForm,Specimen_SGForm,Specimen_APMSForm,Specimen_PTMForm, Specimen_GBForm,LoginForm, ExperimentForm, EDForm
from django.views.generic.base import RedirectView
from formtools.wizard.views import SessionWizardView
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from .excel_utils import WriteToExcel

from django.core.mail import send_mail
#import logging
#logr=logging.getlogger(__name__)

import os
from django.core.mail import send_mail

import sys
sys.path.insert(0, '/home/pportal/dev2/src/lib/python2.7/site-packages/youtrack/')
# authenticating
import http.client, urllib.request, urllib.error

#import socks
from youtrack import connection

#import logging
##logr=logging.getlogger(__name__)
#from django.contrib.formtools.wizard.views import SessionWizardView

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
		next_=request.GET.get('/login')
		next_post=request.POST.get('/profile')
		redirect_path = next_ or next_post or None
		email=form.cleaned_data.get('email')
		password=form.cleaned_data.get('password')
		user = authenticate(request,username=email,password=password)
		if user is not None:
			login(request, user)
			return redirect('/project-registration')
		else:
			if is_safe_url(redirect_path, request.get_host()):
				return redirect('/project-registration')
			else:
				return redirect("/login")
		return super(LoginView, self).form_invalid(form)  


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

FORMSSG = [("0", AnalysisForm),
         ("1", Specimen_SGForm),
         ("2",ExperimentForm)]#,
#         ("3", EDForm)]


TEMPLATESSG = {"0": "project-regis_1.html",
             "1": "project-regis_2.html",
             "2": "project-regis_3.html"}#,
#             "3": "project-regis.html"}


#TEMPLATESSG = {"0": "project-regis_1.html",
#             "1": "project-regis_22.html",
#             "2": "project-regis_3.html",
#             "3": "project-regis_4.html"}


FORMSAPMS = [("0", AnalysisForm),
         ("1", Specimen_APMSForm),
         ("2",ExperimentForm)]

TEMPLATESAPMS = {"0": "project-regis.html",
             "1": "project-regis.html",
             "2": "project-regis.html"}

FORMSPTM = [("0", AnalysisForm),
         ("1", Specimen_PTMForm),
         ("2",ExperimentForm)]

TEMPLATESPTM = {"0": "project-regis.html",
             "1": "project-regis.html",
             "2": "project-regis.html"}

FORMSGB = [("0", AnalysisForm),
         ("1", Specimen_GBForm),
         ("2", ExperimentForm)]

TEMPLATESGB = {"0": "project-regis.html",
             "1": "project-regis.html",
             "2": "project-regis.html"}             

class ContactWizardSG(SessionWizardView):

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
        analysis = [form.cleaned_data for form in form_list]
        # file field
        upload_file = form_list[2].cleaned_data['Nb_samples']
        yt = connection.Connection(url='https://youtrack.ugent.be', login='prcsite', token='perm:cHJjc2l0ZQ==.cHJjc2l0ZS10b2s=.XCNRP5yqauYkjFiFzj2VGYybpS3DJy')
        yt.executeCommand("PRC-321", "No_Samples 23", group="PRC-website")
        return render(self.request,'done.html',{
            'form_data': analysis[0],
            'analysisd':form_dict,
            'upload_file' : upload_file,
            })
        #return render(self.request,'done.html',{'form_data': form_data,})
   # def form_initial(request):
    #	if step=='3':
    #		temp = Profile.objects.get(issue=self.request.user.profile.Issue)
    		#{'Generic_Sample_Name', temp} 
    #		return Profile
    	#instance = Experiment(owner=request.user.email)
    	#form = ExperimentForm(instance=instance)
    	#initial = self.initial_dict.get(step,{})
    	#issue = self.request.GET.get.("Issue")

    #     send_mail(form_data[0])['subject'],
    #             form_data[1])['message'],
    #             form_data[2])['sender'],
    #             ['mariatem@gmail.com'],fail_silently=False)
    #    return form_data

    def get_form_initial(self, step):
        """
        Set extra parameter for step2, which is from clean data of step1.
        """
        initial = self.initial_dict.get(step, {})
        if step == '2':
            form_class = self.form_list[step]
            Issue = self.request.user.profile.Issue + '-S' 
            #form_class['Generic_Sample_Name'] = self.request.user.profile.Issue 
            initial.update({'Generic_Sample_Name':Issue})
            return initial
        if step == '3':
            form_class = self.form_list[step]
            prev_data = self.storage.get_step_data('1')
            samplename = prev_data.get('Generic_Sample_Name','')
            #return samplename
            return self.initial_dict.get(step, {samplename:'samplename'})

       
#projectregistrationsg = ContactWizardSG.as_view([AnalysisForm, Specimen_SGForm, ExperimentForm])


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

def requestt_page(request):
    weather_period = 's'
    if request.method =='GET':
        form = EDForm()
        #i#f form.is_valid():
        #town_id = form.data['town']
        #town = Town.objects.get(pk=town_id)
          #  weather_period = 'ss'
        if "excel" in request.GET:
            response = HttpResponse(content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename=ExperimentalDesign.xlsx'
            xlsx_data = WriteToExcel()
            response.write(xlsx_data)
            return response
        #if request.method == 'GET':
            #form = EDForm(data=request.POST)
            #if form.is_valid():
             #   weather_period = ContactWizardSG.get_form_instance('1')
        #if form.is_valid():
         #   town_id = form.data['town']
          #  town = Town.objects.get(pk=town_id)
           # weather_period = Weather.objects.filter(town=town_id)
            # if 'excel' in request.GET:
            #     response = HttpResponse(content_type='application/vnd.ms-excel')
            #     response['Content-Disposition'] = 'attachment; filename=Report.xlsx'
            #     xlsx_data = WriteToExcel()
            #     response.write(xlsx_data)
            #     return response
            #else:
            #    form = WeatherForm()
    else:
        form = EDForm()
    template_name = "project-regis_oo.html"
    context = {
            'form': form,
      #  'town': town,
            'weather_period': weather_period,
    }   
    return render(request, template_name, context)            
    


class ContactWizardAPMS(SessionWizardView):

    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT,'seqdbs'))
    def get_template_names(self):
        return [TEMPLATESAPMS[self.steps.current]]

    def done(self, form_list, **kwargs):
        #form_list = [CustomerForm, AnalysisForm, Specimen_SGForm]
        #form_list = [AnalysisForm, Specimen_SGForm, ExperimentForm]
        #form_list = [AnalysisForm, Specimen_SGForm]
        return render(self.request,"done.html",{
        'form_data': [form.get_cleaned_data for form in form_list],})
   # def form_initial(request):
    #	if step=='3':
    #		temp = Profile.objects.get(issue=self.request.user.profile.Issue)
    		#{'Generic_Sample_Name', temp} 
    #		return Profile
    	#instance = Experiment(owner=request.user.email)
    	#form = ExperimentForm(instance=instance)
    	#initial = self.initial_dict.get(step,{})
    	#issue = self.request.GET.get.("Issue")
    def get_form_initial(self, step):
        """
        Set extra parameter for step2, which is from clean data of step1.
        """
        initial = self.initial_dict.get(step, {})
        if step == '2':
            form_class = self.form_list[step]
            Issue = self.request.user.profile.Issue 
            #form_class['Generic_Sample_Name'] = self.request.user.profile.Issue 
            initial.update({'Generic_Sample_Name':Issue})
            return initial
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ContactWizardAPMS, self).dispatch(*args, **kwargs)

class ContactWizardPTM(SessionWizardView):

    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT,'seqdbs'))
    def get_template_names(self):
        return [TEMPLATESPTM[self.steps.current]]

    def done(self, form_list, **kwargs):
        #form_list = [CustomerForm, AnalysisForm, Specimen_SGForm]
        #form_list = [AnalysisForm, Specimen_SGForm, ExperimentForm]
        #form_list = [AnalysisForm, Specimen_SGForm]
        return render(self.request,"done.html",{
        'form_data': [form.get_all_cleaned_data for form in form_list],})
   # def form_initial(request):
    #	if step=='3':
    #		temp = Profile.objects.get(issue=self.request.user.profile.Issue)
    		#{'Generic_Sample_Name', temp} 
    #		return Profile
    	#instance = Experiment(owner=request.user.email)
    	#form = ExperimentForm(instance=instance)
    	#initial = self.initial_dict.get(step,{})
    	#issue = self.request.GET.get.("Issue")
    def get_form_initial(self, step):
        """
        Set extra parameter for step2, which is from clean data of step1.
        """
        initial = self.initial_dict.get(step, {})
        if step == '2':
            form_class = self.form_list[step]
            Issue = self.request.user.profile.Issue 
            #form_class['Generic_Sample_Name'] = self.request.user.profile.Issue 
            initial.update({'Generic_Sample_Name':Issue})
            return initial
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ContactWizardPTM, self).dispatch(*args, **kwargs)


class ContactWizardGB(SessionWizardView):

    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT,'seqdbs'))
    def get_template_names(self):
        return [TEMPLATESGB[self.steps.current]]

    def done(self, form_list, **kwargs):
        #form_list = [CustomerForm, AnalysisForm, Specimen_SGForm]
        #form_list = [AnalysisForm, Specimen_SGForm, ExperimentForm]
        #form_list = [AnalysisForm, Specimen_SGForm]
        return render(self.request,"done.html",{
        'form_data': [form.get_all_cleaned_data for form in form_list],})
   # def form_initial(request):
    #	if step=='3':
    #		temp = Profile.objects.get(issue=self.request.user.profile.Issue)
    		#{'Generic_Sample_Name', temp} 
    #		return Profile
    	#instance = Experiment(owner=request.user.email)
    	#form = ExperimentForm(instance=instance)
    	#initial = self.initial_dict.get(step,{})
    	#issue = self.request.GET.get.("Issue")
    def get_form_initial(self, step):
        """
        Set extra parameter for step2, which is from clean data of step1.
        """
        initial = self.initial_dict.get(step, {})
        if step == '2':
            form_class = self.form_list[step]
            Issue = self.request.user.profile.Issue 
            #form_class['Generic_Sample_Name'] = self.request.user.profile.Issue 
            initial.update({'Generic_Sample_Name':Issue})
            return initial 
        if step == '3':
            form_class = self.form_list[step]
            prev_data = self.storage.get_step_data('1')
            samplename = prev_data.get('Generic_Sample_Name','')
            #return samplename
            return self.initial_dict.get(step, {samplename:'samplename'})

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ContactWizardGB, self).dispatch(*args, **kwargs)
	

    # def ED_template(request):
    # weather_period = ContactWizardSG.get_form_instance(1)
    # #town = None
    # if request.method == 'POST':
    #     #form = EDForm(data=request.POST)
    #     #if form.is_valid():
    #      #   town_id = form.data['town']
    #       #  town = Town.objects.get(pk=town_id)
    #        # weather_period = Weather.objects.filter(town=town_id)
    #     if 'excel' in request.POST:
    #         response = HttpResponse(content_type='application/vnd.ms-excel')
    #         response['Content-Disposition'] = 'attachment; filename=Report.xlsx'
    #         xlsx_data = WriteToExcel()
    #         response.write(xlsx_data)
    #         return response
    # else:
    #     form = WeatherForm()
    # template_name = "project-regis_4.html"
    # context = {
    #     'form': form,
    #   #  'town': town,
    #     'weather_period': weather_period,
    # }
    # return render(request, template_name, context)

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


class HomeView(TemplateView):
	template_name = 'home.html'
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

class sample_deliveryView(TemplateView):
    template_name = 'sample-delivery3.html'

# def about(request):
# 	context = {}
# 	return render(request, 'about.html', context)

class contactView(TemplateView):
    template_name = 'contact.html'

# def about(request):
#   context = {}
#   return render(request, 'about.html', context)

class questionsView(TemplateView):
    template_name = 'questions.html'

# def about(request):
#   context = {}
#   return render(request, 'about.html', context)

class AboutView(TemplateView):
	template_name = 'about.html'
	# def get(self, request, *args, **kargs):
	# 	context = {}
	#  	return render(request, 'about.html', context)

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
      