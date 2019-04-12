#!/usr/bin/python
# -*- coding: UTF-8 -*-

from django import forms
from django.utils.safestring import mark_safe
from django.contrib.auth.forms import ReadOnlyPasswordHashField
#from uploads.core.models import Document
#from django.forms.models import modelformset_factory
#from .models import Customer, Analysis, Specimen_SG, Specimen_GB, Specimen_APMS, Specimen_PTM
#from .models import Analysis,Profile,Specimen_SG, Specimen_GB, Specimen_APMS, Specimen_PTM, User, Experiment
from .models import User, Analysis,Profile#,Specimen_SG#, Specimen_GB, Specimen_APMS, Specimen_PTM, Experiment
from django.contrib.auth.tokens import default_token_generator
#from .models import Analysis,User,Profile#,Specimen_SG#, Specimen_GB, Specimen_APMS, Specimen_PTM, Experiment
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

#from django import forms
# class ContactForm1(forms.Form):
# 	subject = forms.CharField(max_length=100)
# 	sender = forms.EmailField()

# class ContactForm2(forms.Form):
# 	message = forms.CharField(widget=forms.Textarea)

# class Profile(models.Model):
# 	user=models.OneToOneField(User, null=True, blank=True)
# 	#user=models.OneToOneField(User, on_delete=models.CASCADE)
# 	Name = models.CharField(max_length=120, null=True, blank=True)
# 	#Email = models.EmailField(max_length=120, null=True) # pre-filled
# 	Group_Leader = models.CharField(max_length=120, null=True, blank=True)
# 	Affiliation_Type = models.CharField(max_length=50, choices=AFFILIATIONTYPES, null=True, blank=True)
# 	Affiliation = models.CharField(max_length=60, null=True, blank=True)
# 	Address = models.CharField(max_length=300, null=True, blank=True)
# 	Project_ID = models.CharField(max_length=200, null=True) # pre-filled displayed on form template on the corner
# 	Main_Analysis_Type = models.CharField(max_length=50 , choices=ANALYSISTYPES, null=True)
class CustomerForm(forms.ModelForm):
	class Meta:
		model = Profile
		#user = User.objects.filter(pk=request.user)
		Project_ID=None
		Email = None
		fields = ['Project_ID','Name','Email', 'Group_leader','Affiliation','Other_institution', 'Address']
		labels={'Group_leader':'Name of group leader',
		}
		widgets = {'Project_ID': forms.TextInput(),
					'Name': forms.TextInput(attrs={'placeholder':'e.g. Anne Breituch'}),
					'Email': forms.TextInput(),
					'Group_leader': forms.TextInput(attrs={'placeholder':'e.g. Claudia Berts'}),
					#'Affiliation': forms.TextInput(attrs={'placeholder':'Institution/Organization'}),
					'Address': forms.Textarea(attrs={'placeholder':'Institutional address','rows':3, 'cols':1}),}
	def __init__(self, *args, **kwargs):
		super(CustomerForm, self).__init__(*args, **kwargs)

		#self.Project_ID = Profile().getProjectID()
		#self.Email = Profile().getEmail()
		print("bu")
						        	
		#self.helper = FormHelper()
		#self.helper.layout= Layout(
			# Fieldset(
			# 'Project_ID',
			# 'Name',
			# 'Email',
			# 'Group_leader',
			# 'Affiliation',
			# 'Other_institution',
			# 'Address'
			# ),
		#	Field('Other_institution', id='ifother')
		#)

						        	
	
		
		#Project_ID=user.profile.getProjectID()
		#Email=user.email
		#Main_analysis_type=getAnalysisType()
		#fields = ['Project_ID','Main_analysis_type','Name','Email', 'Group_leader','Affiliation','Other_institution', 'Address']
		#fields = ['Project_ID', 'Name', 'Email', 'Group_Leader','Affiliation','Other_Institution', 'Address']
		#INPUT_CLASS = 'form-control'
		#def __unicode__(self):
		#	return self.name
		# widgets = {'Project_ID': forms.TextInput(),
		# 			'Name': forms.TextInput(attrs={'placeholder':'e.g. Anne Breituch'}),
		# 			'Email': forms.TextInput(),
		# 			'Group_Leader': forms.TextInput(attrs={'placeholder':'e.g. Claudia Berts'}),
		# 			#'Affiliation': forms.TextInput(attrs={'placeholder':'Institution/Organization'}),
		# 			'Address': forms.Textarea(attrs={'placeholder':'Institutional address','rows':3, 'cols':1}),

		#}
# 		def clean(self):
# 			cleaned_data = super(CustomerForm, self).clean()
# 			Project_id = cleaned_data.get('Project_id')
# 			Name = cleaned_data.get('Name')
# 			Email = cleaned_data.get('Email')
# 			Group_leader = cleaned_data.get('Group_leader')
# 			Affiliation = cleaned_data.get('Affiliation')
# 			Address = cleaned_data.get('Address')
# 			if not Issue and not Name and not Email and not Group_leader and not Affiliation:
# 				raise forms.ValidationError('Please fill in the form')
 # class 1 - form 1
	# Project_summary = models.CharField(max_length=300)
	# Project_keywords = models.CharField(max_length=120)
	# Analysis_Type = models.CharField(max_length=50 , choices=ANALYSISTYPES, null=True) # pre-filled?!
	# Study_Type = models.CharField(max_length=50, choices=STUDYTYPES, null=True)
	# timestamp = models.DateTimeField(auto_now_add=True)

class AnalysisForm(forms.ModelForm):
#	Main_analysis_type = forms.ModelChoiceField(queryset=None)
	#Field('password', id="password-field", css_class="passwordfields", title="Explanation")
	#self.fields['Main_analysis_type'].queryset = {choice:user.Main_analysis_type.choices[choice] for choice in user.Main_analysis_type.choices}
	#choices = user.Main_analysis_type.choices
	#Main_analysis_type = forms.ModelChoiceField(queryset=None)
	#Main_analysis_type = forms.CharField()

	class Meta:
		model = Analysis
		#Analysis.objects.get_or_create(user=user.username)

		fields = ("Project_title",'Project_summary', "Main_analysis_type","Data_analysis",
			'Main_analysis_type')
		widgets = {'Project_summary': forms.Textarea(attrs={'placeholder': 'Provide a 4 line summary of the project explaining the purpose of the analysis',
			'cols':1,'rows':6}),"Main_analysis_type":forms.HiddenInput}
					#}
		labels = {'Data_analysis':'Check this box if you only need to receive raw data.'}	

	def __init__(self,  *args, **kwargs):
		#self.user = kwargs.pop('user', None)
		super().__init__(*args, **kwargs)
		#choices = self.user.Main_analysis_type.choices
		#print("choices"+str(choices))
		#self.Main_analysis_type.choices = {choice:user.Main_analysis_type.choice[choice] for choice in user.Main_analysis_type}
		#self.fields['Main_analysis_type'].queryset = {choice:user.Main_analysis_type.choices[choice] for choice in user.Main_analysis_type}
	
		
		#def clean(self):
		#	cleaned_data = super(AnalysisForm, self).clean()
		#	Project_summary = cleaned_data.get('Project_summary')
			#Project_keywords = cleaned_data.get('Project_keywords')
			#Analysis_type = cleaned_data.get('Analysis_type')
			#Analysis_type2 = cleaned_data.get('Analysis_type2')
			#if not Project_summary and not Project_keywords:
			#	raise forms.ValidationError('Please fill in the form')
	
		#def get_all_cleaned_data(self):
		#	cleaned_data = super(AnalysisForm, self).clean()
		#	Project_summary = cleaned_data.get('Project_summary')
			#Project_keywords = cleaned_data.get('Project_keywords')
			#Analysis_type = cleaned_data.get('Analysis_type')
			#Analysis_type2 = cleaned_data.get('Analysis_type2')
			#Study_Type = cleaned_data.get('Study_type')
			#if not Analysis_type and not Project_summary and not Project_keywords:
			#	raise forms.ValidationError('Please fill in the form')
				
		#def get_cleaned_data(self):
		#	cleaned_data = super(AnalysisForm, self).clean()
		#	Project_summary = cleaned_data.get('Project_summary')
			#Project_keywords = cleaned_data.get('Project_keywords')
			#Analysis_type = cleaned_data.get('Analysis_type')
			#Analysis_type2 = cleaned_data.get('Analysis_type2')
			#Study_Type = cleaned_data.get('Study_type')
			#if not Analysis_type and not Project_summary and not Project_keywords:
			#	raise forms.ValidationError('Please fill in the form')

		#labels = {'Project_summary':'Project_summary'}
		#help_texts = {'Project_summary':'Provide a 4 line summary'}

class PasswordResetForm(forms.Form):
    #email = forms.EmailField(label=("Email"), max_length=254)
    username = forms.CharField(label=("Project_ID"), max_length=254)

    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        """
        Send a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)

        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        if html_email_template_name is not None:
            html_email = loader.render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, 'text/html')

        email_message.send()

    def get_users(self, email):
        """Given an email, return matching user(s) who should receive a reset.

        This allows subclasses to more easily customize the default policies
        that prevent inactive users and users with unusable passwords from
        resetting their password.
        """
        print("bu")
        active_users = UserModel._default_manager.filter(**{
            '%s__iexact' % UserModel.get_username_field_name(): username,
            'is_active': True,
        })
        print(active_users)
        # active_users = UserModel._default_manager.filter(**{
        #     '%s__iexact' % UserModel.get_email_field_name(): email,
        #     'is_active': True,
        # })
        return (u for u in active_users if u.has_usable_password())

    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None, html_email_template_name=None,
             extra_email_context=None):
        """
        Generate a one-use only link for resetting password and send it to the
        user.
        """
        email = self.cleaned_data["email"]
        for user in self.get_users(email):
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override
            context = {
                'email': email,
                'domain': domain,
                'site_name': site_name,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': 'https' if use_https else 'http',
                **(extra_email_context or {}),
            }
            self.send_mail(
                subject_template_name, email_template_name, context, from_email,
                email, html_email_template_name=html_email_template_name,
            )

DATAANALYSIS = (
	(True,'Yes'),
	(False,'No')
	)

SAMPLETYPES = (
	('cell_pellet','cell pellet'),
	('tissue','tissue'), 
	('protein_extract','protein extract'),
	)


VUNITS = (
	(True,'μl'),
	(False,'ml'),
	)
CUNITS = (
	('nmol/ul','ng/μl'),
	('umol/ul','μg/μl'),
	('mmol/ul','mg/μl'),
	)
class Specimen_SGForm(forms.Form):
	Species = forms.CharField(max_length=120, label="Sample species and taxonomy ID", widget=forms.TextInput(attrs={'placeholder': 'e.g. Homo sapiens, taxid: 9606'}))
	#Taxon_id = forms.CharField(max_length=120, required=True)
	Sequence_Database_Public_Availability = forms.ChoiceField(choices=DATAANALYSIS,
		 label="Protein sequence database publically available?", widget=forms.RadioSelect)
	Sequence_database_name = forms.CharField(max_length=50, required=False, label="If 'Yes', sequence database source and/or name:",
		widget=forms.TextInput(attrs={'placeholder': 'e.g. UNIPROT, "UNIPROT UP000005640 reference proteome"'}))
	#Sequence_database_file = forms.FileField(blank=True, storage=FileSystemStorage(location=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'media')))
	Sequence_database_file = forms.FileField( required=False,label="If 'No', please provide a document with protein sequences necessary for database searching, preferentially in FASTA format.")
	Sample_Type = forms.CharField(max_length=50, label="Sample_type_delivered",widget=forms.TextInput(attrs={'placeholder': 'e.g. cell pellet/tissue/protein extract in eppendorf/15 ml tube'}))
	#Sample_Type = forms.CharField(max_length=50, label="Sample_type_delivered",widget=forms.TextInput(attrs={'placeholder': 'e.g. cell pellet, tissue, protein extract in eppendorf or 15 ml tube'}))
	#Sample_Vial = forms.CharField(max_length=50, label="Sample_type_delivered",widget=forms.TextInput(attrs={'placeholder': 'e.g. cell pellet, tissue, protein extract in eppendorf or 15 ml tube'}))
	
	Buffer_composition = forms.CharField(max_length=300, widget=forms.Textarea(attrs={'placeholder':'e.g. 0.1M Tris-HCl pH8.0', 'rows':3, 'cols':1}),
	 label="In case of liquid samples, please provide the exact buffer composition.", 	required=False)

class Specimen_PTMForm(forms.Form):
	PTM = forms.CharField(max_length=120, label="Modification(s) under investigation", widget=forms.TextInput(attrs={'placeholder': 'e.g. lysine acetylation, tyrosine phosphorylation'}))
	Species = forms.CharField(max_length=120, label="Sample species and taxonomy ID", widget=forms.TextInput(attrs={'placeholder': 'e.g. Homo sapiens, taxid: 9606'}))
	#Taxon_id = forms.CharField(max_length=120, required=True)
	Sequence_Database_Public_Availability = forms.ChoiceField(choices=DATAANALYSIS,
		 label="Protein sequence database publically available?", widget=forms.RadioSelect)
	Sequence_database_name = forms.CharField(max_length=50, required=False, label="If 'Yes', sequence database source and/or name:",
		widget=forms.TextInput(attrs={'placeholder': 'e.g. UNIPROT, "UNIPROT UP000005640 reference proteome"'}))
	#Sequence_database_file = forms.FileField(blank=True, storage=FileSystemStorage(location=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'media')))
	Sequence_database_file = forms.FileField( required=False,label="If 'No', please provide a document with protein sequences necessary for database searching, preferentially in FASTA format.")
	Sample_Type = forms.CharField(max_length=50, label="Sample_type_delivered",widget=forms.TextInput(attrs={'placeholder': 'e.g. cell pellet/tissue/protein extract in eppendorf/15 ml tube'}))
	#Sample_Type = forms.CharField(max_length=50, label="Sample_type_delivered",widget=forms.TextInput(attrs={'placeholder': 'e.g. cell pellet, tissue, protein extract in eppendorf or 15 ml tube'}))
	#Sample_Vial = forms.CharField(max_length=50, label="Sample_type_delivered",widget=forms.TextInput(attrs={'placeholder': 'e.g. cell pellet, tissue, protein extract in eppendorf or 15 ml tube'}))
	
	Buffer_composition = forms.CharField(max_length=300, widget=forms.Textarea(attrs={'placeholder':'e.g. 0.1M Tris-HCl pH8.0', 'rows':3, 'cols':1}),
	 label="In case of liquid samples, please provide the exact buffer composition.", 	required=False)



SAMPLETYPESAPMS = (
	('washed_beads','Washed beads'),
	('eluate','Eluate'),
	)
class Specimen_APMSForm(forms.Form):
	Bait_Molecule = forms.ChoiceField(choices=DATAANALYSIS, label="Bait molecule is a protein?", widget=forms.RadioSelect) 
	Bait_Molecule_Protein = forms.CharField(max_length=300,
		 label="If 'Yes', please provide the protein name, a database accession if existing and information on bait expression level.", 
		 widget=forms.TextInput(attrs={'placeholder': 'e.g. Actin, Uniprot P60709, overexpression of a FLAG-tagged variant from vector/promoter x'}))
	Bait_sequence_file = forms.FileField( required=False,label="For a tagged or engineered bait protein, please provide a document with its full length sequence, preferentially in FASTA format.")
	Bait_Molecule_other = forms.CharField(max_length=50, required=False, label="If 'No', describe the bait molecule",
		widget=forms.TextInput(attrs={'placeholder': 'e.g. biotinylated DNA sequence'}))
	#Sequence_database_file = forms.FileField(blank=True, storage=FileSystemStorage(location=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'media')))
	Antibodies = forms.CharField(max_length=120, label="Antibody(ies) used for IP", widget=forms.TextInput(attrs={'placeholder': 'e.g. anti-GFP Ab'}))#, 
		#help_text="Company and catalog number (e.g. Sigma-Aldrich, G1544/nAmount (or estimation of))")
	AbSource = forms.CharField(max_length=120, label="Antibody(ies) company and catalog number", widget=forms.TextInput(attrs={'placeholder':'e.g. Sigma-Aldrich, G1544'}))
	AbAmount = forms.CharField(max_length=120, label="Amount of antibody(ies) (or estimation of)", widget=forms.TextInput(attrs={'placeholder':'e.g. 1 μg Ab for 1 ml of lysate'}))
	Beads = forms.CharField(max_length=120, label="Beads used for IP", widget=forms.TextInput(attrs={'placeholder': 'e.g. Protein G Sepharose beads'})) 
	BeadsSource = forms.CharField(max_length=120, label="Beads company and catalog number", widget=forms.TextInput(attrs={'placeholder': 'e.g. Sigma-Aldrich, P3296'}))
	BeadsAmount = forms.CharField(max_length=120, label="Amount of settled beads (or estimation of)",widget=forms.TextInput(attrs={'placeholder':'e.g. 20 μl beads for 1 ml of lysate'}))
	Species = forms.CharField(max_length=120, label="Species and taxonomy ID for interacting protein", widget=forms.TextInput(attrs={'placeholder': 'e.g. Homo sapiens, taxid: 9606'}))
	#Taxon_id = forms.CharField(max_length=120, required=True)
	#Sequence_database_name = forms.CharField(max_length=50, required=False, label="",
#		widget=forms.TextInput(attrs={'placeholder': 'e.g. TAIR, UNIPROT, SWISSPROT, REFSEQ, EMBL'}))
	#Sequence_database_file = forms.FileField(blank=True, storage=FileSystemStorage(location=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'media')))
	Sample_Type = forms.ChoiceField(choices=SAMPLETYPESAPMS, label="Sample_type_delivered",widget=forms.Select())
	Buffer_composition = forms.CharField(max_length=300, widget=forms.Textarea(attrs={'placeholder':'e.g. 20 mM Tris-HCl pH8.0, 2 mM CaCl2', 'rows':3, 'cols':1}),
	 label="Please provide the exact buffer composition of the samples", required=False)
	#Buffer_composition_El = forms.CharField(max_length=300, widget=forms.Textarea(attrs={'placeholder':'e.g. 50 mM Tris-HCl pH8.0, 2mM CaCl2, 20 μg 3X FLAG peptide', 'rows':3, 'cols':1}),
	 #label="Eluate, buffer composition", required=False)

	#Sample_Type = forms.CharField(max_length=50, label="Sample_type_delivered",widget=forms.TextInput(attrs={'placeholder': 'e.g. cell pellet, tissue, protein extract in eppendorf or 15 ml tube'}))
	#Sample_Vial = forms.CharField(max_length=50, label="Sample_type_delivered",widget=forms.TextInput(attrs={'placeholder': 'e.g. cell pellet, tissue, protein extract in eppendorf or 15 ml tube'}))


class Specimen_GBForm(forms.Form):
	#Setup = forms.CharField(max_length=120, label="Brief description of the experimental setup & sample preparation", widget=forms.TextInput)
	Setup = forms.CharField(max_length=300, widget=forms.Textarea(attrs={'placeholder':'', 'rows':2, 'cols':1}),
	 label="Brief description of the experimental setup & sample preparation", required=False)
	Gel_file = forms.FileField( required=False,label="Please submit a picture of the gel from which the bands or spots were excised")
	Species = forms.CharField(max_length=120, label="Sample species and taxonomy ID", widget=forms.TextInput(attrs={'placeholder': 'e.g. Homo sapiens, taxid: 9606'}))
	#Taxon_id = forms.CharField(max_length=120, required=True)
	Sequence_Database_Public_Availability = forms.ChoiceField(choices=DATAANALYSIS,
		 label="Protein sequence database publically available?", widget=forms.RadioSelect)
	Sequence_database_name = forms.CharField(max_length=50, required=False, label="If 'Yes', sequence database source and/or name:",
		widget=forms.TextInput(attrs={'placeholder': 'e.g. UNIPROT, "UNIPROT UP000005640 reference proteome"'}))
	#Sequence_database_file = forms.FileField(blank=True, storage=FileSystemStorage(location=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'media')))
	Sequence_database_file = forms.FileField( required=False,label="If 'No', please provide a document with protein sequences necessary for database searching, preferentially in FASTA format.")
	PAGEInfo = forms.CharField(max_length=120, label="Company and catalog number of pre-cast gel", widget=forms.TextInput(attrs={'placeholder': 'e.g. Bio-Rad Mini-Protean, 4561084'})) 
	PolyAcrylPercentage = forms.CharField(max_length=120, label="Percentage polyacrylamide", widget=forms.TextInput(attrs={'placeholder': 'e.g. 4-15 %'}))
	StainingMethod = forms.CharField(max_length=120, label="Staining Method",widget=forms.TextInput(attrs={'placeholder':'e.g. Coomassie G-250, Thermo SimplyBlue SafeStain LC6060'}))
	PAGEType = forms.CharField(max_length=120, label="PAGE type",widget=forms.TextInput(attrs={'placeholder':'e.g. SDS-PAGE or native PAGE'}))
	#Sample_Type = forms.CharField(max_length=50, label="Sample_type_delivered",widget=forms.TextInput(attrs={'placeholder': 'e.g. cell pellet/tissue/protein extract in eppendorf/15 ml tube'}))
	#Sample_Type = forms.CharField(max_length=50, label="Sample_type_delivered",widget=forms.TextInput(attrs={'placeholder': 'e.g. cell pellet, tissue, protein extract in eppendorf or 15 ml tube'}))
	#Sample_Vial = forms.CharField(max_length=50, label="Sample_type_delivered",widget=forms.TextInput(attrs={'placeholder': 'e.g. cell pellet, tissue, protein extract in eppendorf or 15 ml tube'}))





# class Specimen_GBForm(forms.ModelForm):
# 	#Analysis_type = forms.CharField(choices = Analysis.ANALYSISTYPES)
# 	class Meta:
# 		model = Specimen_GB
# 		fields = ('Experimental_Setup_Sample_Preparation', 'Gel_GelBand_Image',
# 			'Species',
# 			'Taxon_id', 'Sequence_Database_Public_Availability',
# 			'Sequence_Database_Source', 
# 			'Gel_Type','Gel_Supplier','Gel_CatalogNumber', 'Gel_Staining_Method','Electrophoresis_Type',
# 			'Sample_Vial','Amount_Of_Protein_Loaded','Amount_Of_Protein_Loaded_Type','CUnit')
# 		#fields = ('Species',
# 	#		'Taxon_id', 'Sequence_Database_Public_Availability',
# 	#		'Sequence_Database_Source','Sequence_Database_File', 
# 	#		'Sample_Type','Sample_Vial')
# 		widgets = {'Species': forms.TextInput(attrs={'placeholder': 'e.g. Arabidopsis thaliana, human'}),
# 					'Taxon_id':forms.TextInput(attrs={'placeholder':'e.g. 3701, 9606'}),
# 					'Sequence_Database_Public_Availability':forms.RadioSelect,
# 		 			'Sequence_Database_Source': forms.TextInput(attrs={'placeholder': 'e.g. TAIR, UNIPROT, REFSEQ, EMBL'}),
# 		 			'Sample_Vial':forms.TextInput(attrs={'placeholder':'e.g. eppendorf tube, 15-ml falcon tube'})}

from django.forms.widgets import HiddenInput	




class EDForm(forms.Form):
    EDfile = forms.FileField(label="Please upload the experimental design file.")
   

class TOUForm(forms.Form):
	TermsOfUse = forms.BooleanField(error_messages={'required': 'You must agree with the Terms of Use'},label=mark_safe('I have read and agree with the Terms of Use of the VIB Proteomics Core.'))
	#TermsOfUse = forms.BooleanField(error_messages={'required': 'You must agree with the Terms of Use'},label=mark_safe('I have read and agree with the <a href="http://127.0.0.1:8000/termsofuse" target="_blank">Terms of Use</a> of the VIB Proteomics Core.'))

   
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

# class ProfileForm(forms.ModelForm):
# 	class Meta:
# 		model = Profile
# 		fields = ('Name', 'Issue','Study_Type','Group_Leader', 'Analysis_Type')
# 		widgets = {'Name': forms.TextInput(attrs={'placeholder': 'Your name'}),'Issue':forms.TextInput(attrs={'placeholder':'e.g. PRC-20'}),
# 		 			'Group_Leader': forms.TextInput(attrs={'placeholder':'Name of principal investigator responsible for the study'})}
# 		def clean(self):
# 			cleaned_data = super(ProfileForm, self).clean()
# 			Issue = cleaned_data.get('Issue')
# 			Name = cleaned_data.get('Name')
# 			Study_Type = cleaned_data.get('Study_Type')
# 			Group_Leader = cleaned_data.get('Group_Leader')
# 			Analysis_Type = cleaned_data.get('Analysis_Type')
# 			#if not Issue and not Name and not Study_Type and not Group_Leader and not Analysis_Type:
# 			#	raise forms.ValidationError('Please fill in the form')
# 		def get_all_cleaned_data(self):
# 			cleaned_data = super(ProfileForm, self).clean()
# 			Issue = cleaned_data.get('Issue')
# 			Name = cleaned_data.get('Name')
# 			Study_Type = cleaned_data.get('Study_Type')
# 			Group_Leader = cleaned_data.get('Group_Leader')
# 			Analysis_Type = cleaned_data.get('Analysis_Type')

# class ProfileForm(forms.ModelForm):
# 	class Meta:
# 		model = Profile
# 		fields = ['Project_ID', 'Name', 'Email', 'Group_Leader','Affiliation', 'Address','Affiliation_Type']
# 		#INPUT_CLASS = 'form-control'
# 		#def __unicode__(self):
# 		#	return self.name
# 		widgets = {'Project_ID': forms.TextInput(),
# 					'Name': forms.TextInput(attrs={'placeholder':'e.g. Anne Breituch'}),
# 					'Email': forms.TextInput(),
# 					'Group_Leader': forms.TextInput(attrs={'placeholder':'e.g. Claudia Berts'}),
# 					'Affiliation': forms.TextInput(attrs={'placeholder':'Institution/Organization'}),
# 					'Address': forms.Textarea(attrs={'placeholder':'Institutional address',
# 						'rows':3, 'cols':1}),

# 		}
# 		def clean(self):
# 			cleaned_data = super(CustomerForm, self).clean()
# 			Project_ID = cleaned_data.get('Project_ID')
# 			Name = cleaned_data.get('Name')
# 			Email = cleaned_data.get('Email')
# 			Group_Leader = cleaned_data.get('Group_Leader')
# 			Affiliation = cleaned_data.get('Affiliation')
# 			Address = cleaned_data.get('Address')
# 			if not Project_ID and not Name and not Email and not Group_Leader and not Affiliation:
# 				raise forms.ValidationError('Please fill in the form')

#examples/one_to_one
class ExperimentForm(forms.Form):

	Experimental_conditions = forms.CharField(label = "Experimental conditions (separated with commas)", widget=forms.Textarea(attrs={'placeholder':'e.g. p53KO, p53WT, p53OE',
		'rows':2, 'cols':1}))
	Conditions_to_compare = forms.CharField(label = "Experimental conditions to compare", widget=forms.Textarea(attrs={'placeholder':'e.g. p53KO vs p53WT, p53OE vs p53WT, p53KO vs p53OE',
		 'rows':3, 'cols':1}))

	#Nb_Experimental_conditions = models.IntegerField()
	# maybe instantiate another model called efactor (experimental factor) n times, n (Nb_factors)
	#Factor_name_lst = models.CharField(max_length=120, null=True)
	#Conditions_list = models.CharField(max_length=120, null=True)
	Nb_replicates_per_condition = forms.IntegerField(label = "Number of replicate samples per condition",widget=forms.NumberInput(attrs={'placeholder':'e.g. 3'}))
	Nb_samples = forms.IntegerField(label = "Total number of MS samples submitted", widget=forms.NumberInput(attrs={'placeholder':'e.g. 9'}))
	#Sample_Name = forms.CharField(widget=forms.HiddenInput, required=False)
	Isotopic_labeling = forms.ChoiceField(choices=DATAANALYSIS , label="Is any isotopic labeling procedure used?", required=True, widget=forms.RadioSelect)
	Isotopic_labeling_details = forms.CharField(label="If 'Yes', which labeling procedure was used?", required=False,
	 widget=forms.Textarea(attrs={'placeholder':'e.g. SILAC; heavy(Arg6,Lys4), light()','rows':3, 'cols':1}))
	Other_information = forms.CharField(label = "Other relevant information about the samples", required=False, widget=forms.TextInput(attrs={'placeholder':'e.g. presence of PTMs'}))


class ExperimentPTMForm(forms.Form):

	Experimental_conditions = forms.CharField(label = "Experimental conditions (separated with commas)", widget=forms.Textarea(attrs={'placeholder':'e.g. p53KO, p53WT, p53OE',
		'rows':2, 'cols':1}))
	Conditions_to_compare = forms.CharField(label = "Experimental conditions to compare", widget=forms.Textarea(attrs={'placeholder':'e.g. kinase inhibitor treatment vs control',
		 'rows':3, 'cols':1}))

	#Nb_Experimental_conditions = models.IntegerField()
	# maybe instantiate another model called efactor (experimental factor) n times, n (Nb_factors)
	#Factor_name_lst = models.CharField(max_length=120, null=True)
	#Conditions_list = models.CharField(max_length=120, null=True)
	Nb_replicates_per_condition = forms.IntegerField(label = "Number of replicate samples per condition",widget=forms.NumberInput(attrs={'placeholder':'e.g. 3'}))
	Nb_samples = forms.IntegerField(label = "Total number of MS samples submitted", widget=forms.NumberInput(attrs={'placeholder':'e.g. 9'}))
	#Sample_Name = forms.CharField(widget=forms.HiddenInput, required=False)
	Isotopic_labeling = forms.ChoiceField(choices=DATAANALYSIS , label="Is any isotopic labeling procedure used?", required=True, widget=forms.RadioSelect)
	Isotopic_labeling_details = forms.CharField(label="If 'Yes', which labeling procedure was used?", required=False,
	 widget=forms.Textarea(attrs={'placeholder':'e.g. SILAC; heavy(Arg6,Lys4), light()','rows':3, 'cols':1}))
	Other_information = forms.CharField(label = "Other relevant information about the samples", required=False)

class ExperimentAPMSForm(forms.Form):

	Experimental_conditions = forms.CharField(label = "Experimental conditions (separated with commas)", widget=forms.Textarea(attrs={'placeholder':'e.g. WT IP, neg. control IP',
		'rows':2, 'cols':1}))
	Conditions_to_compare = forms.CharField(label = "Experimental conditions to compare", widget=forms.Textarea(attrs={'placeholder':'e.g. IP with wild type bait vs IP with deletion mutant as negative control',
		 'rows':3, 'cols':1}))
	#Nb_Experimental_conditions = models.IntegerField()
	# maybe instantiate another model called efactor (experimental factor) n times, n (Nb_factors)
	#Factor_name_lst = models.CharField(max_length=120, null=True)
	#Conditions_list = models.CharField(max_length=120, null=True)
	Nb_replicates_per_condition = forms.IntegerField(label = "Number of replicate samples per condition",widget=forms.NumberInput(attrs={'placeholder':'e.g. 3'}))
	Nb_samples = forms.IntegerField(label = "Total number of MS samples submitted", widget=forms.NumberInput(attrs={'placeholder':'e.g. 9'}))
	#Sample_Name = forms.CharField(widget=forms.HiddenInput, required=False)
	#Isotopic_labeling = forms.ChoiceField(choices=DATAANALYSIS , label="Is any isotopic labeling procedure used?", required=False, widget=forms.RadioSelect)
	#Isotopic_labeling_details = forms.CharField(label="If 'Yes', which labeling procedure was used?", required=False,
	# widget=forms.Textarea(attrs={'placeholder':'e.g. SILAC; heavy(Arg6,Lys4), light()','rows':3, 'cols':1}))
	Other_information = forms.CharField(label = "Other relevant information about the samples", required=False, widget=forms.TextInput(attrs={'placeholder':'e.g. presence of PTMs, isotopic labeling procedures'}))


class ExperimentGBForm(forms.Form):

	Experimental_conditions = forms.CharField(label = "Experimental conditions (separated with commas)", widget=forms.Textarea(attrs={'placeholder':'e.g. WT protein, mutant protein',
		'rows':2, 'cols':1}))
	Conditions_to_compare = forms.CharField(label = "Experimental conditions to compare", widget=forms.Textarea(attrs={'placeholder':'e.g.WT protein vs mutant protein',
		 'rows':3, 'cols':1}), required=False)
	#Nb_Experimental_conditions = models.IntegerField()
	# maybe instantiate another model called efactor (experimental factor) n times, n (Nb_factors)
	#Factor_name_lst = models.CharField(max_length=120, null=True)
	#Conditions_list = models.CharField(max_length=120, null=True)
	Nb_replicates_per_condition = forms.IntegerField(label = "Number of replicate samples per condition",widget=forms.NumberInput(attrs={'placeholder':'e.g. 3'}))
	Nb_samples = forms.IntegerField(label = "Total number of gel bands submitted", widget=forms.NumberInput(attrs={'placeholder':'e.g. 6'}))
	#Sample_Name = forms.CharField(widget=forms.HiddenInput, required=False)
	Isotopic_labeling = forms.ChoiceField(choices=DATAANALYSIS , label="Is any isotopic labeling procedure used?", required=True, widget=forms.RadioSelect)
	Isotopic_labeling_details = forms.CharField(label="If 'Yes', which labeling procedure was used?", required=False,
	 widget=forms.Textarea(attrs={'placeholder':'e.g. SILAC; heavy(Arg6,Lys4), light()','rows':3, 'cols':1}))	
	Other_information = forms.CharField(label = "Other relevant information about the samples", required=False, widget=forms.TextInput(attrs={'placeholder':'e.g. presence of PTMs, isotopic labeling procedures'}))


	#fields = ('Isotopic_labeling', 'Isotopic_labeling_details','Nb_conditions', 'Conditions_list', 'Nb_samples')
	# p53KO_drugD, WT_drugD, p53KO_vehicle, WT_vehicle
			 			
	#def __init__(self, *args, **kwargs):
		#super(EDForm,self).__init__(*args, **kwargs)	
	# def clean(self):
	# 	cleaned_data = super('ExperimentForm', self).clean()
	# 	Experimental_conditions = cleaned_data('Experimental_conditions', self).clean()
	# 	Conditions_to_compare = cleaned_data('Conditions_to_compare', self).clean()
	# 	Nb_replicates_per_condition = cleaned_data('Nb_replicates_per_condition', self).clean()
	# 	Nb_samples = cleaned_data.get('Nb_samples')
	# 	Isotopic_labeling = cleaned_data.get('Isotopic_labeling')
	# 	Isotopic_labeling_details = cleaned_data.get('Isotopic_labeling_details')
			#Nb_conditions = cleaned_data.get('Nb_factors')
			#Factor_name_lst = cleaned_data.get('Factor_name_lst')
			
			#Generic_Sample_Name = cleaned_data.get('Generic_Sample_Name')
			#Sample_Name = cleaned_data.get('Sample_Name')
			#if not Isotopic_labeling and not Nb_conditions and not Conditions_lst and not Nb_samples:
			#	raise forms.ValidationError('Please fill in the form')
		#labels = {'Nb_conditions':'No. of Experimental Conditions',
		#'Nb_samples':'No. of samples for mass spectrometry',
		#}
		#help_texts = {'Project_summary':'Provide a 4 line summary'}

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
    #class Meta:
    #model=User
    #fields = ["username", "password"]
    #email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'placeholder':'email address'}))
    #password = forms.CharField(label='Project ID', widget=forms.TextInput(attrs={'placeholder':'e.g. PRC-214'}))
    username = forms.CharField(label='Project_ID', widget=forms.TextInput(attrs={'placeholder':''}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':''}))


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

# class UserAdminCreationForm(forms.ModelForm):
#     """A form for creating new users. Includes all the required
#     fields, plus a repeated password."""
#     password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
#     password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

#     class Meta:
#         model = User
#         fields = ('username',)

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
#         if commit:
#             user.save()
#         return user


# class UserAdminChangeForm(forms.ModelForm):
#     """A form for updating users. Includes all the fields on
#     the user, but replaces the password field with admin's
#     password hash display field.
#     """
#     password = ReadOnlyPasswordHashField()

#     class Meta:
#         model = User
#         fields = ('username', 'password', 'active', 'admin')

#     def clean_password(self):
#         # Regardless of what the user provides, return the initial value.
#         # This is done here, rather than on the field, because the
#         # field does not have access to the initial value
#         return self.initial["password"]


