"""pportal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.urls import reverse_lazy, path
#from django.views.generic import TemplateView

from django.contrib import admin
from django.contrib import auth
from django.contrib.auth import views as auth_views

from prcprojects.forms import AnalysisForm
#from prcprojects.forms import CustomerForm, Specimen_SGForm, Specimen_PTMForm, ExperimentForm,ExperimentPTMForm,ExperimentAPMSForm, EDForm,Specimen_APMSForm,Specimen_APMSForm,EDForm#,Specimen_GBForm, EDForm
from prcprojects.forms import CustomerForm, AnalysisForm, Specimen_SGForm,Specimen_APMSForm,Specimen_PTMForm,EDPMDForm, Specimen_GBForm, ExperimentForm,ExperimentPTMForm,ExperimentAPMSForm,ExperimentGBForm, ExperimentPMDForm, EDForm, TOUForm#,Specimen_GBForm, EDForm

#from prcprojects.views import AboutView,HomeView, CustomerRegistrationView,AnalysisRegistrationView, AnalysisForm, CustomerForm, Specimen_SGForm, ContactWizard
from prcprojects.views import get_data,StatesView, ProjectInfoGaugeView, PreparationView, ReportsView, TermsOfUseView, AboutTheCoreView, AboutView, HomeView, ProjectInfoView, ProjectInfoGuestView, ShippingInstructionsView, ContactView, AnalysisRegistrationView,InfoView, QuestionsView, MoveView, AnalysisForm, ExperimentForm, Specimen_SGForm, LoginView, ContactWizard, ContactWizardSG, ContactWizardPTM, ContactWizardAPMS,ContactWizardGB,ContactWizardPMD#,SGView#,ProjectRegistrationView
from django.views.generic import TemplateView
#from prcprojects.views import AboutView,HomeView, AnalysisRegistrationView, AnalysisForm, CustomerForm, Specimen_SGForm, ContactWizard

from prcprojects import views
#from prcprojects.views import HomeView, AboutView, UserRegistrationView,AnalysisRegistrationView,SampleRegistrationView
from django.contrib.auth.decorators import login_required

# from prcprojects.forms import ContactForm1, ContactForm2
# from prcprojects.views import CWizard

urlpatterns = static(settings.MEDIA_URL,document_root =
  settings.MEDIA_ROOT) +[
    url(r'^admin/', admin.site.urls),
   #url(r'^contact/$', CWizard.as_view([ContactForm1, ContactForm2])),
    url(r'^ShippingInstructions/',ShippingInstructionsView.as_view(template_name='sample-delivery3.html'),name='ShippingInstructions'),
    url(r'^questions/', QuestionsView.as_view(template_name='questions.html'),name='questions'),
    url(r'^protocols/',PreparationView.as_view(template_name='protocols.html'), name='protocols'),
    url(r'^reports/',ReportsView.as_view(template_name='MM.html'), name='reports'),
    url(r'^information/$', InfoView.as_view(template_name='information2.html'), name='information'),
    url(r'^$', HomeView.as_view(template_name='home.html'), name='home'),
    url(r'^questions/', QuestionsView.as_view(template_name='questions.html'),name='questions'),
    url(r'^move/', MoveView.as_view(template_name='move.html'),name='move'),
    url(r'^AboutTheCore/',AboutTheCoreView.as_view(template_name='AboutTheCore.html'), name='AboutTheCore'),
        #url(r'^password_reset/done/$', auth_views.password_reset(), name='password_reset_done'),
    url(r'^project-registration/$', login_required(ContactWizard.as_view([CustomerForm,CustomerForm,CustomerForm,CustomerForm,CustomerForm])),name='projectregistration'),
  #   #url(r'^project-registrationsg/$', ContactWizardSG.as_view([CustomerForm, Specimen_SGForm, Specimen_SGForm]),name='projectregistrationsg'),
  #   #url(r'^project-registration-1/$', ContactWizardSG.as_view([CustomerForm,AnalysisForm, Specimen_SGForm, ExperimentForm, EDForm]),name='projectregistrationsg'),
    url(r'^project-registration1/$', ContactWizardSG.as_view([CustomerForm,AnalysisForm, Specimen_SGForm, ExperimentForm, EDForm,TOUForm]),name='projectregistrationsg'),
    #url(r'^project-registration1/$', ContactWizardSG.as_view([CustomerForm,AnalysisForm, Specimen_SGForm, EDForm,TOUForm]),name='projectregistrationsg'),
    url(r'^project-registration2/$', ContactWizardAPMS.as_view([CustomerForm,AnalysisForm, Specimen_APMSForm, ExperimentAPMSForm, EDForm,TOUForm]),name='projectregistrationapms'),
    url(r'^project-registration3/$', ContactWizardPTM.as_view([CustomerForm,AnalysisForm, Specimen_PTMForm, ExperimentPTMForm, EDForm,TOUForm]),name='projectregistrationptm'),
    url(r'^project-registration4/$', ContactWizardGB.as_view([CustomerForm,AnalysisForm, Specimen_GBForm, ExperimentGBForm, EDForm,TOUForm]),name='projectregistrationgel'),
    url(r'^project-registration5/$', ContactWizardPMD.as_view([CustomerForm,AnalysisForm, ExperimentPMDForm, EDPMDForm,TOUForm]),name='projectregistrationpmd'),
    url(r'^termsofuse/$', TermsOfUseView.as_view(template_name='TermsOfUse.html'), name='termsofuse'),

   url(r'^contact/',  ContactView.as_view(template_name='contact.html'),name='contact'),
   #url(r'^project-info/$', views.get_user_projectinfo, name='projectinfo'),
   url(r'^project-info/$', login_required(ProjectInfoView.as_view(template_name='project-info.html')), name='project-info'),
   url(r'^project-info-guest/$', ProjectInfoGuestView.as_view(template_name='project-info-guest.html'), name='project-info-guest'),
   url(r'^project-info-d3gauge/$', ProjectInfoGaugeView.as_view(template_name='project-infogauge.html'), name='project-infogauge'),
  #   #url(r'^profile/(?P<email>\w+)/$', views.get_user_profile, name='profile'),
  #   url(r'^about/$', AboutView.as_view(template_name='about.html'),name='about'),
  #   url(r'^bootstrap/$', TemplateView.as_view(template_name='bootstrap/example.html'),name='bootstrap'),
   url(r'^login/$', LoginView.as_view(template_name='login.html'),name='login'),
   #url(r'^logout/$', auth_views.LogoutView.as_view(next_page=reverse_lazy('login')),name='logout'),
   url(r'^logout/$', auth_views.LogoutView.as_view(template_name='logout.html'),name='logout'),

     ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
  #   #+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
 # if DEBUG is on
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root =settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,document_root =settings.MEDIA_ROOT)

