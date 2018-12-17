#!/usr/bin/python
# -*- coding: UTF-8 -*-

from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
#from uploads.core.models import Document
#from django.forms.models import modelformset_factory
#from .models import Customer, Analysis, Specimen_SG, Specimen_GB, Specimen_APMS, Specimen_PTM
from .models import Analysis,Profile,Specimen_SG, Specimen_GB, Specimen_APMS, Specimen_PTM, User, Experiment
from crispy_forms.helper import FormHelper
#from crispy_forms.bootstrap import Field, InlineRadios, TabHolder, Tab
from crispy_forms.bootstrap import FormActions, AppendedText
from crispy_forms.layout import Submit, Layout, Div, Fieldset, Hidden , Field

#from .models import User, Analysis,Experiment

#from django.forms.formsets import formset_factory
# class ProductForm(forms.Form):
#     name = forms.CharField()
#     quantity = forms.IntegerField()
#     price = forms.IntegerField()

# ProductFormset = forms.formsets.formset_factory(ProductForm)

# class DistributorForm(forms.Form):
#    name= forms.CharField()
#    products= ProductFormset()

# class CustomerForm(forms.ModelForm):
# 	class Meta:
# 		model = Customer
# 		fields = ['Issue', 'Name', 'Email', 'Group_Leader','Affiliation' ]
# 		#INPUT_CLASS = 'form-control'
# 		#def __unicode__(self):
# 		#	return self.name
# 		#widgets = {'name' : forms.TextInput(attrs={'class':INPUT_CLASS,
# 		#	'placeholder':'Enter title here'})
# 		#}
# 		def clean(self):
# 			cleaned_data = super(CustomerForm, self).clean()
# 			Issue = cleaned_data.get('Issue')
# 			Name = cleaned_data.get('Nameapp# 			Email = cleaned_data.get('Email')
# 			Group_Leader = cleaned_data.get('Group_Leader')
# 			Affiliation = cleaned_data.get('Affiliation')
# 			if not Issue and not Name and not Email and not Group_Leader and not Affiliation:
# 				raise forms.ValidationError('Please fill in the form')
#  class 1 - form 1


class AnalysisForm(forms.ModelForm):
	#Analysis_type = forms.CharField(choices = Analysis.ANALYSISTYPES)
	class Meta:
		model = Analysis
		fields = ('Project_summary',
			'Project_keywords', 'Address','Affiliation')
		widgets = {'Project_summary': forms.Textarea(attrs={'placeholder': 'Provide a 4 line summary of the project explaining the purpose of the analysis'}),
					'Project_keywords': forms.TextInput(attrs={'placeholder': 'e.g. autophagy, sumoylation, cell cycle'}),
					'Address': forms.TextInput(attrs={'placeholder': 'Institutional address'}),
					'Affiliation':forms.TextInput(attrs={'placeholder':'Academic institution or Company name'})
					}
		def clean(self):
			cleaned_data = super(AnalysisForm, self).clean()
			Project_summary = cleaned_data.get('Project_summary')
			Project_keywords = cleaned_data.get('Project_keywords')
			Address = cleaned_data.get('Address')
			Affiliation = cleaned_data.get('Affiliation')
			if not Address and not Affiliation and not Project_summary and not Project_keywords:
				raise forms.ValidationError('Please fill in the form')
				
		def get_all_cleaned_data(self):
			cleaned_data = super(AnalysisForm, self).clean()
			Project_summary = cleaned_data.get('Project_summary')
			Project_keywords = cleaned_data.get('Project_keywords')
			Address = cleaned_data.get('Address')
			Affiliation = cleaned_data.get('Affiliation')
			if not Address and not Affiliation and not Project_summary and not Project_keywords:
				raise forms.ValidationError('Please fill in the form')
				
		def get_cleaned_data(self):
			cleaned_data = super(AnalysisForm, self).clean()
			Project_summary = cleaned_data.get('Project_summary')
			Project_keywords = cleaned_data.get('Project_keywords')
			Address = cleaned_data.get('Address')
			Affiliation = cleaned_data.get('Affiliation')
			if not Address and not Affiliation and not Project_summary and not Project_keywords:
				raise forms.ValidationError('Please fill in the form')

		#labels = {'Project_summary':'Project_summary'}
		#help_texts = {'Project_summary':'Provide a 4 line summary'}

class Specimen_SGForm(forms.ModelForm):
	#Analysis_type = forms.CharField(choices = Analysis.ANALYSISTYPES)
	def __init__(self, *args, **kwargs):

		self.helper = FormHelper()
		self.helper.form_tag = False
		self.helper.form_method = "post"
		self.helper.form_class = 'blueforms'
		self.helper.id = 'sg_form'
		self.helper.layout = Layout(
			'Species','Taxon_id','Sequence_Database_Public_Availability',
			'Sequence_Database_Source',#'Sequence_Database_File',
			'Sample_Type','Sample_Vial','Buffer_Composition',
		AppendedText('Volume', 'μl'),
		AppendedText('Protein_Concentration', 'mg/μl'))
		self.helper.add_input(Submit('submit', 'Submit'))
		super(Specimen_SGForm,self).__init__(*args, **kwargs)
		#self.helper.layout.append(Submit('save','save'))
		#self.helper.layout = Layout(
		#PrependedText('Volume', 'ul'),
		#PrependedText('Protein_Concentration', 'mg/ul'))
	class Meta:
		model = Specimen_SG
		fields = ('Species',
		'Taxon_id', 'Sequence_Database_Public_Availability',
		'Sequence_Database_Source', #'Sequence_Database_File',
		'Sample_Type','Sample_Vial','Buffer_Composition','Volume',
		'Protein_Concentration')
	#fields = ('Species',
#		'Taxon_id', 'Sequence_Database_Public_Availability',
#		'Sequence_Database_Source','Sequence_Database_File', 
#		'Sample_Type','Sample_Vial')
		widgets = {'Species': forms.TextInput(attrs={'placeholder': 'e.g. Arabidopsis thaliana, human'}),
				'Taxon_id':forms.TextInput(attrs={'placeholder':'e.g. 3701, 9606'}),
				'Sequence_Database_Public_Availability':forms.RadioSelect,
	 			'Sequence_Database_Source': forms.TextInput(attrs={'placeholder': 'e.g. TAIR, UNIPROT, REFSEQ, EMBL'}),
	 			'Sample_Vial':forms.TextInput(attrs={'placeholder':'e.g. eppendorf tube, 15-ml falcon tube'}),
	 			'Buffer_Composition':forms.TextInput(attrs={'placeholder':'e.g. Tris-HCl 0.1M pH8.0'})}



			#	Field('VUnit'),
			#	Div(PrependedText('VUnit')))

class Specimen_PTMForm(forms.ModelForm):
	#Analysis_type = forms.CharField(choices = Analysis.ANALYSISTYPES)
	class Meta:
		model = Specimen_PTM
		fields = ('Modification_Under_Investigation','Species',
			'Taxon_id', 'Sequence_Database_Public_Availability',
			'Sequence_Database_Source', 
			'Sample_Type','Sample_Vial','Buffer_Composition','Volume','VUnit',
			'Protein_Concentration','CUnit')
	#		'Taxon_id', 'Sequence_Database_Public_Availability',
	#		'Sequence_Database_Source','Sequence_Database_File', 
	#		'Sample_Type','Sample_Vial')
		widgets = {'Modification_Under_Investigation': forms.TextInput(attrs={'placeholder':'e.g. phosphorylation, ubiquitylation'}),
					'Species': forms.TextInput(attrs={'placeholder': 'e.g. Arabidopsis thaliana, human'}),
					'Taxon_id':forms.TextInput(attrs={'placeholder':'e.g. 3701, 9606'}),
					'Sequence_Database_Public_Availability':forms.RadioSelect,
		 			'Sequence_Database_Source': forms.TextInput(attrs={'placeholder': 'e.g. TAIR, UNIPROT, REFSEQ, EMBL'}),
		 			'Sample_Vial':forms.TextInput(attrs={'placeholder':'e.g. eppendorf tube, 15-ml falcon tube'})}


class Specimen_APMSForm(forms.ModelForm):
	#Analysis_type = forms.CharField(choices = Analysis.ANALYSISTYPES)
	class Meta:
		model = Specimen_APMS
		fields = ('Bait_Molecule','IPAntibodies_names',
			'Species',
			'Taxon_id', 'Sequence_Database_Public_Availability',
			'IPAntibodies_Supplier','IPAntibodies_CatalogNumber',
			'Sequence_Database_Source', 
			'Sample_Type','Sample_Vial','Buffer_Composition','Volume','VUnit',
			'Protein_Concentration','CUnit')
		#fields = ('Species',
	#		'Taxon_id', 'Sequence_Database_Public_Availability',
	#		'Sequence_Database_Source','Sequence_Database_File', 
	#		'Sample_Type','Sample_Vial')
		widgets = {'Species': forms.TextInput(attrs={'placeholder': 'e.g. Arabidopsis thaliana, human'}),
					'Taxon_id':forms.TextInput(attrs={'placeholder':'e.g. 3701, 9606'}),
					'Sequence_Database_Public_Availability':forms.RadioSelect,
		 			'Sequence_Database_Source': forms.TextInput(attrs={'placeholder': 'e.g. TAIR, UNIPROT, REFSEQ, EMBL'}),
		 			'Sample_Vial':forms.TextInput(attrs={'placeholder':'e.g. eppendorf tube, 15-ml falcon tube'})}


class Specimen_GBForm(forms.ModelForm):
	#Analysis_type = forms.CharField(choices = Analysis.ANALYSISTYPES)
	class Meta:
		model = Specimen_GB
		fields = ('Experimental_Setup_Sample_Preparation', 'Gel_GelBand_Image',
			'Species',
			'Taxon_id', 'Sequence_Database_Public_Availability',
			'Sequence_Database_Source', 
			'Gel_Type','Gel_Supplier','Gel_CatalogNumber', 'Gel_Staining_Method','Electrophoresis_Type',
			'Sample_Vial','Amount_Of_Protein_Loaded','Amount_Of_Protein_Loaded_Type','CUnit')
		#fields = ('Species',
	#		'Taxon_id', 'Sequence_Database_Public_Availability',
	#		'Sequence_Database_Source','Sequence_Database_File', 
	#		'Sample_Type','Sample_Vial')
		widgets = {'Species': forms.TextInput(attrs={'placeholder': 'e.g. Arabidopsis thaliana, human'}),
					'Taxon_id':forms.TextInput(attrs={'placeholder':'e.g. 3701, 9606'}),
					'Sequence_Database_Public_Availability':forms.RadioSelect,
		 			'Sequence_Database_Source': forms.TextInput(attrs={'placeholder': 'e.g. TAIR, UNIPROT, REFSEQ, EMBL'}),
		 			'Sample_Vial':forms.TextInput(attrs={'placeholder':'e.g. eppendorf tube, 15-ml falcon tube'})}

from django.forms.widgets import HiddenInput	

class EDForm(forms.Form):
	#town = forms
    #queryset=Town.objects.all(),
    #widget=forms.Select(attrs={'class': 'form-control'}))
	# file to download
	# it should have content from form1 and form2
	###input dont know
    # file to upload with experimental design final version
    DownloadButton = forms.CharField(widget=HiddenInput())
    Experimental_Design_file = forms.FileField(allow_empty_file=True)
    def __init__(self, *args, **kwargs):
         super(EDForm,self).__init__(*args, **kwargs)
         self.helper = FormHelper()
         self.helper.form_method = "get"
         self.DownloadButton = Layout(Field('DownloadButton',type = 'hidden'))
         #self.helper.add_input(Submit('submit', 'Submitt', css_class='btn-success'))
    

# # shotgun Specimen
# class Specimen_SG(models.Model):
	# Species = models.CharField(max_length=120)
	# Taxon_id = models.CharField(max_length=120)
	# Sequence_Database_Public_Availability = models.BooleanField(choices=DATAANALYSIS)
	# Sequence_Database_Source = models.BooleanField()
	# Sequence_Database_File = models.FileField()
	# #Sample_Type_Delivered 
	# Sample_Type = models.CharField(max_length=50 ,choices=SAMPLETYPES)
	# Sample_Vial = models.CharField(max_length=120)
	# # if applicable exact
	# Buffer_Composition = models.CharField(max_length=300)
	# #volume or estimation in ul / ml
	# Volume = models.FloatField()
	# VUnit = models.BooleanField(choices=VUNITS)
	# Protein_Concentration = models.FloatField()
	# CUnit = models.CharField(max_length=10 , choices=CUNITS)
	# def __unicode__(self):
	# 	return self.Species 
# class SpecimenForm(forms.ModelForm):
# 	class Meta:
# 		model = Sample
# 		#fields = ['Generic_Sample_Name','Species',
#  		#'Sample_Type_Delivered','Buffer_composition','Volume','Protein_conc']
#  		exclude=()
#  		extra=3


 # class ExpDesignForm(forms.ModelForm):#
	# class Meta:
	# 	model = Experimental_Design
	# 	fields = ['samples','Nb_samples', 'Nb_factors']

class ProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ('Name', 'Issue','Study_Type','Group_Leader', 'Analysis_Type')
		widgets = {'Name': forms.TextInput(attrs={'placeholder': 'Your name'}),'Issue':forms.TextInput(attrs={'placeholder':'e.g. PRC-20'}),
		 			'Group_Leader': forms.TextInput(attrs={'placeholder':'Name of principal investigator responsible for the study'})}
		def clean(self):
			cleaned_data = super(ProfileForm, self).clean()
			Issue = cleaned_data.get('Issue')
			Name = cleaned_data.get('Name')
			Study_Type = cleaned_data.get('Study_Type')
			Group_Leader = cleaned_data.get('Group_Leader')
			Analysis_Type = cleaned_data.get('Analysis_Type')
			#if not Issue and not Name and not Study_Type and not Group_Leader and not Analysis_Type:
			#	raise forms.ValidationError('Please fill in the form')
		def get_all_cleaned_data(self):
			cleaned_data = super(ProfileForm, self).clean()
			Issue = cleaned_data.get('Issue')
			Name = cleaned_data.get('Name')
			Study_Type = cleaned_data.get('Study_Type')
			Group_Leader = cleaned_data.get('Group_Leader')
			Analysis_Type = cleaned_data.get('Analysis_Type')

# examples/one_to_one
class ExperimentForm(forms.ModelForm):
	class Meta:
		model = Experiment
		fields = ('Isotopic_labeling', 'Isotopic_labeling_details','Nb_conditions', 'Conditions_list', 'Nb_samples')
		widgets = {'Isotopic_labeling': forms.RadioSelect,
					'Isotopic_labeling_details':forms.TextInput(attrs={'placeholder':'e.g. SILAC;heavy(Arg6,Lys4),light()'}),
		 			'Nb_variables': forms.TextInput(attrs={'placeholder':'e.g. 1, 2'}),
		 				'Conditions_list': forms.TextInput(attrs={'placeholder':'e.g. p53KO, drugD treatment, gender'}),
		 					'Nb_samples': forms.TextInput(attrs={'placeholder':'e.g. 1, 2'})}#,
#		 						'Sample_Name': forms.TextInput(attrs={'placeholder': 'custom sample name (optional)'})}
		
		def clean(self):
			cleaned_data = super(ExperimentForm, self).clean()
			Isotopic_labeling = cleaned_data.get('Isotopic_labeling')
			Isotopic_labeling_details = cleaned_data.get('Isotopic_labeling_details')
			Nb_conditions = cleaned_data.get('Nb_factors')
			#Factor_name_lst = cleaned_data.get('Factor_name_lst')
			Nb_samples = cleaned_data.get('Nb_samples')
			Generic_Sample_Name = cleaned_data.get('Generic_Sample_Name')
			Sample_Name = cleaned_data.get('Sample_Name')
			if not Isotopic_labeling and not Nb_conditions and not Conditions_lst and not Nb_samples:
				raise forms.ValidationError('Please fill in the form')
		labels = {'Nb_conditions':'No. of Experimental Conditions',
		'Nb_samples':'No. of samples for mass spectrometry',
		}
		#help_texts = {'Project_summary':'Provide a 4 line summary'}


def weather_history(request):
    weather_period = Weather.objects.all()
    town = None
    if request.method == 'POST':
        form = WeatherForm(data=request.POST)
        if form.is_valid():
            town_id = form.data['town']
            town = Town.objects.get(pk=town_id)
            weather_period = Weather.objects.filter(town=town_id)
        if 'excel' in request.POST:
            response = HttpResponse(content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename=Report.xlsx'
            xlsx_data = WriteToExcel(weather_period, town)
            response.write(xlsx_data)
            return response
        if 'pdf' in request.POST:
            response = HttpResponse(content_type='application/pdf')
            today = date.today()
            filename = 'pdf_demo' + today.strftime('%Y-%m-%d')
            response['Content-Disposition'] =\
                'attachement; filename={0}.pdf'.format(filename)
            buffer = BytesIO()
            report = PdfPrint(buffer, 'A4')
            pdf = report.report(weather_period, 'Weather statistics data')
            response.write(pdf)
            return response
    else:
        form = WeatherForm()

    template_name = "exportingfiles/weather_history.html"
    context = {
        'form': form,
        'town': town,
        'weather_period': weather_period,
    }
    return render(request, template_name, context)


# class Profile_extraForm(forms.ModelForm):
# 	class Meta:
# 		model = Profile_extra
# 		fields = ('Affiliation','Address')
# 		widgets = {'Address': forms.TextInput(attrs={'placeholder': 'Institutional address'}),
# 		'Affiliation':forms.TextInput(attrs={'placeholder':'Academic institution or Company name'})}


# 		#INPUT_CLASS = 'form-control'
# 		#def __unicode__(self):
# 		#	return self.name
# 		#widgets = {'name' : forms.TextInput(attrs={'class':INPUT_CLASS,
# 		#	'placeholder':'Enter title here'})
# 		#}
# 		def clean(self):
# 			cleaned_data = super(CustomerForm, self).clean()
# 			Address = cleaned_data.get('Address')
# 			Affiliation = cleaned_data.get('Affiliation')
# 			if not Address and not Affiliation:
# 				raise forms.ValidationError('Please fill in the form')

class LoginForm(forms.Form):
    """A form for user log in. Includes all the required
    fields, plus a repeated password."""
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'placeholder':'email address'}))
    password = forms.CharField(label='Project ID', widget=forms.TextInput(attrs={'placeholder':'e.g. PRC-214'}))

#		 						'Sample_Name': forms.TextInput(attrs={'placeholder': 'custom sample name (optional)'})}


# class RegisterForm(forms.ModelForm):
# 	"""A form to create new users. Includes all the required
#     fields, plus a repeated password."""
#     class Meta:
#         model = User
#         fields = ('email',)

#     def clean_password2(self):
#         # Check that the two password entries match
#         password1 = self.cleaned_data.get("password1")
#         password2 = self.cleaned_data.get("password2")
#         if password1 and password2 and password1 != password2:
#             raise forms.ValidationError("Passwords don't match")
#         return password2

#     def save(self, commit=True):
#         # Save the provided password in hashed format
#         user = super(UserAdminCreationForm, self).save(commit=False)
#         user.set_password(self.cleaned_data["password1"])
#         ##########user.active = True # still send a confirmation email
#         if commit:
#             user.save()
#         return user

class UserAdminCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'active', 'admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


