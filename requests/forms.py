#!/usr/bin/python
# -*- coding: UTF-8 -*-

from django import forms
from django.utils.safestring import mark_safe
from django.contrib.auth.forms import ReadOnlyPasswordHashField
#from uploads.core.models import Document
#from django.forms.models import modelformset_factory
#from .models import Customer, Analysis, Specimen_SG, Specimen_GB, Specimen_APMS, Specimen_PTM
#from .models import Analysis,Profile,Specimen_SG, Specimen_GB, Specimen_APMS, Specimen_PTM, User, Experiment
from .models import Analysis,Profile,User#,Specimen_SG#, Specimen_GB, Specimen_APMS, Specimen_PTM, Experiment
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

class CustomerForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['Project_ID', 'Name', 'Email', 'Group_Leader','Affiliation', 'Address','Affiliation_Type']
		#INPUT_CLASS = 'form-control'
		#def __unicode__(self):
		#	return self.name
		labels={'Group_Leader':'Name of group leader'
		}
		widgets = {'Project_ID': forms.TextInput(),
					'Name': forms.TextInput(attrs={'placeholder':'e.g. Anne Breituch'}),
					'Email': forms.TextInput(),
					'Group_Leader': forms.TextInput(attrs={'placeholder':'e.g. Claudia Berts'}),
					'Affiliation': forms.TextInput(attrs={'placeholder':'Institution/Organization'}),
					'Address': forms.Textarea(attrs={'placeholder':'Institutional address','rows':3, 'cols':1}),

		}
		def clean(self):
			cleaned_data = super(CustomerForm, self).clean()
			Project_ID = cleaned_data.get('Project_ID')
			Name = cleaned_data.get('Name')
			Email = cleaned_data.get('Email')
			Group_Leader = cleaned_data.get('Group_Leader')
			Affiliation = cleaned_data.get('Affiliation')
			Address = cleaned_data.get('Address')
			if not Issue and not Name and not Email and not Group_Leader and not Affiliation:
				raise forms.ValidationError('Please fill in the form')
 #class 1 - form 1
	#Project_summary = models.CharField(max_length=300)
	#Project_keywords = models.CharField(max_length=120)
	#Analysis_Type = models.CharField(max_length=50 , choices=ANALYSISTYPES, null=True) # pre-filled?!
	#Study_Type = models.CharField(max_length=50, choices=STUDYTYPES, null=True)
	#timestamp = models.DateTimeField(auto_now_add=True)

class AnalysisForm(forms.ModelForm):
	#Analysis_type = forms.CharField(choices = Analysis.ANALYSISTYPES)
	class Meta:
		model = Analysis
		fields = ('Project_summary',
			'Project_keywords', 'Analysis_type','Analysis_type2',"Data_analysis")
		widgets = {'Project_summary': forms.Textarea(attrs={'placeholder': 'Provide a 4 line summary of the project explaining the purpose of the analysis',
			'cols':1,'rows':6}),
					'Project_keywords': forms.TextInput(attrs={'placeholder': 'e.g. autophagy, sumoylation, BRCA clinical variants'},),
					}
		labels = {'Data_analysis':'Check this box if you wish to receive a data analysis report.'}			
		def clean(self):
			cleaned_data = super(AnalysisForm, self).clean()
			Project_summary = cleaned_data.get('Project_summary')
			Project_keywords = cleaned_data.get('Project_keywords')
			Analysis_type = cleaned_data.get('Analysis_type')
			Analysis_type2 = cleaned_data.get('Analysis_type2')
			if not Analysis_type and not Project_summary and not Project_keywords:
				raise forms.ValidationError('Please fill in the form')
				
		def get_all_cleaned_data(self):
			cleaned_data = super(AnalysisForm, self).clean()
			Project_summary = cleaned_data.get('Project_summary')
			Project_keywords = cleaned_data.get('Project_keywords')
			Analysis_type = cleaned_data.get('Analysis_type')
			Analysis_type2 = cleaned_data.get('Analysis_type2')
			#Study_Type = cleaned_data.get('Study_type')
			if not Analysis_type and not Project_summary and not Project_keywords:
				raise forms.ValidationError('Please fill in the form')
				
		def get_cleaned_data(self):
			cleaned_data = super(AnalysisForm, self).clean()
			Project_summary = cleaned_data.get('Project_summary')
			Project_keywords = cleaned_data.get('Project_keywords')
			Analysis_type = cleaned_data.get('Analysis_type')
			Analysis_type2 = cleaned_data.get('Analysis_type2')
			#Study_Type = cleaned_data.get('Study_type')
			if not Analysis_type and not Project_summary and not Project_keywords:
				raise forms.ValidationError('Please fill in the form')

		#labels = {'Project_summary':'Project_summary'}
		#help_texts = {'Project_summary':'Provide a 4 line summary'}
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
	Sequence_database_name = forms.CharField(max_length=50, required=False, label="If 'Yes', sequence database name:",
		widget=forms.TextInput(attrs={'placeholder': 'e.g. TAIR, UNIPROT, SWISSPROT, REFSEQ, EMBL'}))
	#Sequence_database_file = forms.FileField(blank=True, storage=FileSystemStorage(location=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'media')))
	Sequence_database_file = forms.FileField( required=False,label="If 'No', please provide a document with protein sequences and corresponding species necessary for database searching, preferentially in FASTA format.")
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
	Sequence_database_name = forms.CharField(max_length=50, required=False, label="If 'Yes', sequence database name:",
		widget=forms.TextInput(attrs={'placeholder': 'e.g. TAIR, UNIPROT, SWISSPROT, REFSEQ, EMBL'}))
	#Sequence_database_file = forms.FileField(blank=True, storage=FileSystemStorage(location=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'media')))
	Sequence_database_file = forms.FileField( required=False,label="If 'No', please provide a document with protein sequences and corresponding species necessary for database searching, preferentially in FASTA format.")
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
	


# shotgun Specimen
# class Specimen_SG(models.Model):
# 	Species = models.CharField(max_length=120)
# 	Taxon_id = models.CharField(max_length=120, null=True)
# 	Protein_sequence_database_publically_available = models.BooleanField(choices=DATAANALYSIS, null=False,
# 		default=True)
# 	Sequence_database_name = models.CharField(max_length=50)
# 	Sequence_database_file = models.FileField(blank=True, storage=FileSystemStorage(location=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'media')))
# 	Sample_type_delivered = models.CharField(max_length=50, null=False)
# 	Buffer_Composition = models.CharField(max_length=300)
# 	Volume = models.DecimalField(decimal_places=2, max_digits=6)
# 	VUnit = models.BooleanField(choices=VUNITS, default='μl', null=False,)
# 	Protein_concentration = models.DecimalField(decimal_places=2, max_digits=6)
# 	CUnit = models.CharField(max_length=10 , choices=CUNITS,null=False,default='μg/μl', blank=False)
# 	def __unicode__(self):
# 		return self.Species 	
# 	def get_absolute_url(self):
# 		return reverse('pportal:home')

			#	Field('VUnit'),
			#	Div(PrependedText('VUnit')))


# class Specimen_APMSForm(forms.ModelForm):
# 	#Analysis_type = forms.CharField(choices = Analysis.ANALYSISTYPES)
# 	class Meta:
# 		model = Specimen_APMS
# 		fields = ('Bait_Molecule','IPAntibodies_names',
# 			'Species',
# 			'Taxon_id', 'Sequence_Database_Public_Availability',
# 			'IPAntibodies_Supplier','IPAntibodies_CatalogNumber',
# 			'Sequence_Database_Source', 
# 			'Sample_Type','Sample_Vial','Buffer_Composition','Volume','VUnit',
# 			'Protein_Concentration','CUnit')
# 		#fields = ('Species',
# 	#		'Taxon_id', 'Sequence_Database_Public_Availability',
# 	#		'Sequence_Database_Source','Sequence_Database_File', 
# 	#		'Sample_Type','Sample_Vial')
# 		widgets = {'Species': forms.TextInput(attrs={'placeholder': 'e.g. Arabidopsis thaliana, human'}),
# 					'Taxon_id':forms.TextInput(attrs={'placeholder':'e.g. 3701, 9606'}),
# 					'Sequence_Database_Public_Availability':forms.RadioSelect,
# 		 			'Sequence_Database_Source': forms.TextInput(attrs={'placeholder': 'e.g. TAIR, UNIPROT, REFSEQ, EMBL'}),
# 		 			'Sample_Vial':forms.TextInput(attrs={'placeholder':'e.g. eppendorf tube, 15-ml falcon tube'}),
# 		 			'Volume':forms.TextInput(attrs={'placeholder':'e.g. eppendorf tube, 15-ml falcon tube'}),
# 		 			'Protein_Concentration':forms.NumberInput(attrs={ 'step':'0.1'})}


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
	#town = forms
    #queryset=Town.objects.all(),
    #widget=forms.Select(attrs={'class': 'form-control'}))
	# file to download
	# it should have content from form1 and form2
	###input dont know
    # file to upload with experimental design final version
    #DownloadButton = forms.FileField(widget=HiddenInput())
    #DownloadButton = forms.CharField()
    # Experimental Design file
   
    EDfile = forms.FileField(label="Please upload the experimental design file.")
    TermsOfUse = forms.BooleanField(error_messages={'required': 'You must agree with the Terms of Use'},label=mark_safe('I have read and agree with the <a href="http://127.0.0.1:8000/termsofuse" target="_blank">Terms of Use</a> of the VIB Proteomics Core.'))
    #def clean(self):
    #	data = self.cleaned_data()
    #	TermsOfUse = self.cleaned_data.get('TermsOfUse')
    #	print(TermsOfUse is False)
    #	if TermsOfUse==False:
    #		raise forms.ValidationError("You have to agree with the Terms of Use of the VIB Proteomics Core")
    # def __init__(self, *args, **kwargs):
    #      super(EDForm,self).__init__(*args, **kwargs)
    #      self.helper = FormHelper()
    #      self.helper.form_method = "post"
    #      self.DownloadButton = Layout(Field('EDfile',type = 'hidden'))
    #      self.helper.add_input(Submit('submit', 'Upload Experimental Design file', css_class='btn-success'))
    

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

class ProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['Project_ID', 'Name', 'Email', 'Group_Leader','Affiliation', 'Address','Affiliation_Type']
		#INPUT_CLASS = 'form-control'
		#def __unicode__(self):
		#	return self.name
		widgets = {'Project_ID': forms.TextInput(),
					'Name': forms.TextInput(attrs={'placeholder':'e.g. Anne Breituch'}),
					'Email': forms.TextInput(),
					'Group_Leader': forms.TextInput(attrs={'placeholder':'e.g. Claudia Berts'}),
					'Affiliation': forms.TextInput(attrs={'placeholder':'Institution/Organization'}),
					'Address': forms.Textarea(attrs={'placeholder':'Institutional address',
						'rows':3, 'cols':1}),

		}
		def clean(self):
			cleaned_data = super(CustomerForm, self).clean()
			Project_ID = cleaned_data.get('Project_ID')
			Name = cleaned_data.get('Name')
			Email = cleaned_data.get('Email')
			Group_Leader = cleaned_data.get('Group_Leader')
			Affiliation = cleaned_data.get('Affiliation')
			Address = cleaned_data.get('Address')
			if not Project_ID and not Name and not Email and not Group_Leader and not Affiliation:
				raise forms.ValidationError('Please fill in the form')

#examples/one_to_one
class ExperimentForm(forms.Form):

	Experimental_conditions = forms.CharField(label = "Experimental conditions", widget=forms.Textarea(attrs={'placeholder':'e.g. p53KO, p53WT, p53OE',
		'rows':2, 'cols':1}))
	Conditions_to_compare = forms.CharField(label = "Experimental conditions to compare", widget=forms.Textarea(attrs={'placeholder':'e.g. p53KO vs p53WT, p53OE vs p53WT, p53KO vs p53OE',
		 'rows':3, 'cols':1}))

	#Nb_Experimental_conditions = models.IntegerField()
	# maybe instantiate another model called efactor (experimental factor) n times, n (Nb_factors)
	#Factor_name_lst = models.CharField(max_length=120, null=True)
	#Conditions_list = models.CharField(max_length=120, null=True)
	Nb_replicates_per_condition = forms.IntegerField(label = "Number of replicate samples per condition",widget=forms.NumberInput(attrs={'placeholder':'e.g. 3'}))
	Nb_samples = forms.IntegerField(label = "Total number of MS samples submitted", widget=forms.NumberInput(attrs={'placeholder':'e.g. 9'}))
	Sample_Name = forms.CharField(widget=forms.HiddenInput, required=False)
	Isotopic_labeling = forms.ChoiceField(choices=DATAANALYSIS , label="Is any isotopic labeling procedure used?", required=False, widget=forms.RadioSelect)
	Isotopic_labeling_details = forms.CharField(label="If 'Yes', which labeling procedure was used?", required=False,
	 widget=forms.Textarea(attrs={'placeholder':'e.g. SILAC; heavy(Arg6,Lys4), light()','rows':3, 'cols':1}))
	Other_infomation = forms.CharField(label = "Other relevant information about the samples", required=False, widget=forms.TextInput(attrs={'placeholder':'e.g. presence of PTMs'}))


class ExperimentPTMForm(forms.Form):

	Experimental_conditions = forms.CharField(label = "Experimental conditions", widget=forms.Textarea(attrs={'placeholder':'e.g. kinase inhibitor treatment, control',
		'rows':2, 'cols':1}))
	Conditions_to_compare = forms.CharField(label = "Experimental conditions to compare", widget=forms.Textarea(attrs={'placeholder':'e.g. kinase inhibitor treatment vs control',
		 'rows':3, 'cols':1}))

	#Nb_Experimental_conditions = models.IntegerField()
	# maybe instantiate another model called efactor (experimental factor) n times, n (Nb_factors)
	#Factor_name_lst = models.CharField(max_length=120, null=True)
	#Conditions_list = models.CharField(max_length=120, null=True)
	Nb_replicates_per_condition = forms.IntegerField(label = "Number of replicate samples per condition",widget=forms.NumberInput(attrs={'placeholder':'e.g. 3'}))
	Nb_samples = forms.IntegerField(label = "Total number of MS samples submitted", widget=forms.NumberInput(attrs={'placeholder':'e.g. 9'}))
	Sample_Name = forms.CharField(widget=forms.HiddenInput, required=False)
	Isotopic_labeling = forms.ChoiceField(choices=DATAANALYSIS , label="Is any isotopic labeling procedure used?", required=False, widget=forms.RadioSelect)
	Isotopic_labeling_details = forms.CharField(label="If 'Yes', which labeling procedure was used?", required=False,
	 widget=forms.Textarea(attrs={'placeholder':'e.g. SILAC; heavy(Arg6,Lys4), light()','rows':3, 'cols':1}))
	Other_infomation = forms.CharField(label = "Other relevant information about the samples", required=False)

class ExperimentAPMSForm(forms.Form):

	Experimental_conditions = forms.CharField(label = "Experimental conditions", widget=forms.Textarea(attrs={'placeholder':'e.g. WT IP, neg. control IP',
		'rows':2, 'cols':1}))
	Conditions_to_compare = forms.CharField(label = "Experimental conditions to compare", widget=forms.Textarea(attrs={'placeholder':'e.g. IP with wild type bait vs IP with deletion mutant as negative control',
		 'rows':3, 'cols':1}))
	#Nb_Experimental_conditions = models.IntegerField()
	# maybe instantiate another model called efactor (experimental factor) n times, n (Nb_factors)
	#Factor_name_lst = models.CharField(max_length=120, null=True)
	#Conditions_list = models.CharField(max_length=120, null=True)
	Nb_replicates_per_condition = forms.IntegerField(label = "Number of replicate samples per condition",widget=forms.NumberInput(attrs={'placeholder':'e.g. 3'}))
	Nb_samples = forms.IntegerField(label = "Total number of MS samples submitted", widget=forms.NumberInput(attrs={'placeholder':'e.g. 9'}))
	Sample_Name = forms.CharField(widget=forms.HiddenInput, required=False)
	#Isotopic_labeling = forms.ChoiceField(choices=DATAANALYSIS , label="Is any isotopic labeling procedure used?", required=False, widget=forms.RadioSelect)
	#Isotopic_labeling_details = forms.CharField(label="If 'Yes', which labeling procedure was used?", required=False,
	# widget=forms.Textarea(attrs={'placeholder':'e.g. SILAC; heavy(Arg6,Lys4), light()','rows':3, 'cols':1}))
	Other_infomation = forms.CharField(label = "Other relevant information about the samples", required=False, widget=forms.TextInput(attrs={'placeholder':'e.g. presence of PTMs, isotopic labeling procedures'}))



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


