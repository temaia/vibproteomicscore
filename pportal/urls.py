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
from django.urls import reverse_lazy
#from django.views.generic import TemplateView

from django.contrib import admin
from django.contrib import auth
from django.contrib.auth import views as auth_views
from requests.forms import AnalysisForm, ProfileForm, Specimen_SGForm,Specimen_APMSForm,Specimen_PTMForm,Specimen_GBForm, EDForm
#from requests.views import AboutView,HomeView, CustomerRegistrationView,AnalysisRegistrationView, AnalysisForm, CustomerForm, Specimen_SGForm, ContactWizard
from requests.views import AboutView,HomeView, sample_deliveryView,contactView, AnalysisRegistrationView, questionsView, AnalysisForm,ExperimentForm,Specimen_SGForm, ContactWizardSG,ContactWizardPTM,ContactWizardAPMS,ContactWizardGB, LoginView,SGView#,ProjectRegistrationView
from django.views.generic import TemplateView
#from requests.views import AboutView,HomeView, AnalysisRegistrationView, AnalysisForm, CustomerForm, Specimen_SGForm, ContactWizard

from requests import views
#from requests.views import HomeView, AboutView, UserRegistrationView,AnalysisRegistrationView,SampleRegistrationView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^sampledelivery/',  sample_deliveryView.as_view(template_name='sample-delivery3.html'),name='sample_delivery'),
    #url(r'^pportal/',include('pportal.urls')),
    url(r'^$', HomeView.as_view(template_name='home.html'), name='home'),
    url(r'^questions/',  questionsView.as_view(template_name='questions.html'),name='questions'),
    #url(r'^project-registration/$', ContactWizard.as_view([CustomerForm,AnalysisForm, Specimen_SGForm]),name='project-registration'),
    #url(r'^project-registration/$', ContactWizard.as_view([AnalysisForm, Specimen_SGForm, ExperimentForm]),name='project-registration'),
    #url(r'^project-registration/$', HomeView.as_view(template_name='home.html') ,name='project-registration'),
    #url(r'^project-registrationsg/$', ContactWizardSG.as_view([AnalysisForm, Specimen_SGForm, ExperimentForm]),name='projectregistrationsg'),
    #url(r'^project-registrationsg/$', 'projectregistrationsg',name='projectregistrationsg'),
    url(r'^project-registrationsg/$', ContactWizardSG.as_view([AnalysisForm, Specimen_SGForm, ExperimentForm]),name='projectregistrationsg'),
    url(r'^project-registrationapms/$', ContactWizardAPMS.as_view([AnalysisForm, Specimen_APMSForm, ExperimentForm]),name='projectregistrationapms'),
    url(r'^project-registrationptm/$', ContactWizardPTM.as_view([AnalysisForm, Specimen_PTMForm, ExperimentForm]),name='projectregistrationptm'),
    url(r'^project-registrationgb/$', ContactWizardGB.as_view([AnalysisForm, Specimen_GBForm, ExperimentForm]),name='projectregistrationgel'),
    #url(r'^profile/(?P<email>[a-zA-Z0-9]+)/$', views.get_user_profile, name='profile'),
    #url(r'^profile/$', views.get_user_profile, name='profile'),
    url(r'^project-registration/$', login_required(views.get_user_profile), name='projectregistration'),
    url(r'^requestt_page/$', views.requestt_page, name='requestt_page'),
    #url(r'^project-registration/$', views.get_user_profile, name='projectregistration'),
    url(r'^contact/',  contactView.as_view(template_name='contact.html'),name='contact'),
    #url(r'^project-info/$', views.get_user_projectinfo, name='projectinfo'),
    #url(r'^profile/(?P<email>\w+)/$', views.get_user_profile, name='profile'),
    url(r'^about/$', AboutView.as_view(template_name='about.html'),name='about'),
    url(r'^bootstrap/$', TemplateView.as_view(template_name='bootstrap/example.html'),name='bootstrap'),
    url(r'^login/$', LoginView.as_view(template_name='login.html'),name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(next_page=reverse_lazy('login')),name='logout'),
    url(r'^sgform/$', SGView.as_view(template_name='project-regis_sg.html'),name='sg_form'),
    #url(r'^logout/$', auth_views.logout,{'next_page':'/'},name='logout'),
    #url(r'^logout/$', auth_views.logout,{template_name:'logout.html'},name='logout'),
    #url(r'^login/$', auth.auth_views.login,name='login'),
    #url(r'^login/$', LoginView.as_view(template_name='login.html'),name='login'),
    # url(r'^project-registration/$', RegistrationView.as_view()),
    #url(r'^project-registration/$', CustomerRegistrationView.as_view(template_name='project-registration_2.html')),
    #url(r'^project-registration-2/$', AnalysisRegistrationView.as_view(template_name='project-registration_2.html')),
    #static(settings.STATIC_URL,document_root =settings.STATIC_ROOT),
    #url(r'^project-registration-3/$', AnalysisRegistrationView2.as_view(template_name='project-registration.html')),
    #url(r'^project-registration-5/$', views.manage_users, name='manage_users'),
    #url(r'^project-registration-3/$', ExperimentalDesignRegistrationView.as_view(template_name='project-registration.html')),
]

# if DEBUG is on
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root =settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,document_root =settings.MEDIA_ROOT)

