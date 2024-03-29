# -*- coding: utf-8 -*-


from django.db import models
from django.core.files.storage import FileSystemStorage
import os
#from django.contrib.auth.models import (AbstractBaseUser,
#	BaseUserManager)
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.signals import user_logged_in

#from django.contrib.auth.models import (User)
from django.db.models.signals import post_save
from django.dispatch import receiver
from multiselectfield import MultiSelectField
# Create your models here.
# Create your models here.
#from multiselectfield import MultiSelectField

# ...

# class UserManager(BaseUserManager):
# 	def get_by_natural_key(self, username):
# 		return self.get(username=username)
# 	def create_user(self,username,password=None, is_active=True,is_staff=False,is_admin=False):
# 		if not username:
# 			raise ValueError("You must provide a username")
# 		if not password:
# 			raise ValueError("You must provide a password")
# 		user_obj = self.model()
# 		user_obj.set_password(password)
# 		user_obj.active = is_active
# 		user_obj.staff = is_staff
# 		user_obj.admin = is_admin
# 		user_obj.save(using=self._db)
# 		return user_obj

# 	def create_staff_user(self,username,password=None):
# 		user_obj = self.create_user(
# 			username, password=password,
# 			is_staff=True
# 		)
# 		return user_obj

# 	def create_superuser(self,username,password=None):
# 		user_obj = self.create_user(
# 			username, password=password,
# 			is_staff=True,
# 			is_admin=True
# 		)
# 		return user_obj

ANALYSISTYPES = (
	('shotgun analysis','shotgun analysis'),
	('affinity-purification MS (AP-MS)','affinity-purification MS (AP-MS)'), 
	('PTM analysis','PTM analysis'),('Virotrap','Virotrap'),
	('protein gel band analysis','protein gel band analysis'),
	('protein mass determination','protein mass determination'),
	('PRM','PRM'),
	('SRM','SRM'),
	('DIA','DIA'),
	('other','other'),
	)

ANALYSISTYPES2= (
	('shotgun analysis','shotgun analysis'),
	('affinity-purification MS (AP-MS)','affinity-purification MS (AP-MS)'), 
	('PTM analysis','PTM analysis'),('Virotrap','Virotrap'),
	('protein gel band analysis','protein gel band analysis'),
	('protein mass determination','protein mass determination'),
	('PRM','PRM'),
	('SRM','SRM'),
	('DIA','DIA'),
	('other','other'),
	)
# STUDYTYPES = (
# 	('Academic','Academic'), 
# 	('Industry','Industry'),
# 	)

AFFILIATIONTYPES= (
	('VIB', 'VIB'),
	('UGent-CRIG','UGent-CRIG'),
	('UGent','UGent'),
	('KULeuven','KULeuven'),
	('UAntwerpen','UAntwerpen'),
	('VUB','VUB'),
	('UHasselt','UHasselt'),
	('Industry','Industry'),
	('Other','Other'),
	)

VIBAFFILIATIONTYPES= (
	('PSB Ghent', 'PSB Ghent'),
	('IRC, Ghent', 'IRC, Ghent'),
	('HQ & CFs', 'HQ & CFs'),
	('BDR, Leuven', 'BDR, Leuven'),
	('CCB, Leuven', 'CCB, Leuven'),
	('CM, Leuven', 'CM, Leuven'),
	('SB, Brussels', 'SB, Brussels'),
	('CMN, Antwerp', 'CMN, Antwerp'),
	('Discovery Sciences', 'Discovery Sciences'),
	)

# AFFILIATIONTYPES= (
# 	('UGent-VIB','UGent-VIB'),
# 	('UGent-CRIG','UGent-CRIG'),
# 	('UGent','UGent'),
# 	('KULeuven-VIB','KULeuven-VIB'),
# 	('KULeuven','KULeuven'),
# 	('UAntwerpen-VIB', 'UAntwerpen-VIB'),
# 	('UAntwerpen','UAntwerpen'),
# 	('VUB-VIB','VUB-VIB'),
# 	('VUB','VUB'),
# 	('UHasselt-VIB','UHasselt-VIB'),
# 	('UHasselt','UHasselt'),
# 	('Industry','Industry'),
# 	('Other','Other'),
# 	)

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
BAITS = (
	(True,'a protein'),
	(False,'another type of molecule'),
	)
SAMPLETYPESAPMS = (
	(True,'washed beads'),
	(False,'eluate'),
	)
PAGETYPES = (
	(True,'SDS-PAGE'),
	(False,'native PAGE'),
	)
GBCHOICES = (
	(True,'loaded on gel'),
	(False,'estimate about gel band'),
	)

class User(AbstractUser):
	# = models.CharField(max_length=50 , choices=ANALYSISTYPES, null=True, blank=True)
	Main_analysis_type = MultiSelectField(choices=ANALYSISTYPES, null=True, blank=True,max_choices=4) # pre-filled?!
	#Main_analysis_type2 = MultiSelectField(choices=ANALYSISTYPES2,
	#								max_choices=4,
     #                            	max_length=4, blank=True, null=True) # pre-filled?!
	#USERNAME_FIELD = 'username'
	#REQUIRED_FIELD=['']
	#def __str__(self):
	#	return self.username
# class User(AbstractBaseUser):
# 	username = models.CharField(max_length = 12, unique=True)
# 	email = models.EmailField(max_length=120)
# 	active = models.BooleanField(default=True)
# 	staff = models.BooleanField(default=False)
# 	admin = models.BooleanField(default=False)
# 	update = models.DateTimeField(auto_now=True)
# 	timestamp = models.DateTimeField(auto_now_add=True)
# 	USERNAME_FIELD='username'
# 	REQUIRED_FIELD=[]
# 	objects= UserManager()
# 	def __str__(self):
# 		return self.username
# 	def get_full_name(self):
# 		return self.email
# 	def get_short_name(self):
# 		return self.email
# 	def get_username(self):
# 		return self.username
# 	def get_last_name(self):
# 		return self.email
# 	def has_perm(self, perm,obj=None):
# 		return True
# 	def has_module_perms(self, app_label):
# 		return True
# 	@property
# 	def is_staff(self):
# 		return self.staff
# 	@property
# 	def is_admin(self):
# 		return self.admin
# 	@property
# 	def is_active(self):
# 		return self.active

# class User(AbstractBaseUser):
# 	email = models.EmailField(unique=True, max_length=120)
# 	active = models.BooleanField(default=True)
# 	staff = models.BooleanField(default=False)
# 	admin = models.BooleanField(default=False)
# 	timestamp = models.DateTimeField(auto_now_add=True)
# 	USERNAME_FIELD='email'
# 	REQUIRED_FIELD=[]
# 	objects= UserManager()
# 	def __str__(self):
# 		return self.email
# 	def get_full_name(self):
# 		return self.email
# 	def get_short_name(self):
# 		return self.email
# 	def get_username(self):
# 		return self.email
# 	def get_last_name(self):
# 		return self.email
# 	def has_perm(self, perm,obj=None):
# 		return True
# 	def has_module_perms(self, app_label):
# 		return True
# 	@property
# 	def is_staff(self):
# 		return self.staff
# 	@property
# 	def is_admin(self):
# 		return self.admin


#  class 1 - form 1
# ANALYSISTYPES = (
# 	('shotgun','Shotgun analysis'),
# 	('APMS','Affinity-Purification MS (AP-MS)'), 
# 	('PTMs','PTM analysis'),
# 	('gelband','Protein gel band analysis'),
# 	('proteinmass','Protein mass determination'),
# 	('other','Other'),
# 	)

    # .....


# list of custom fields
#User = get_user_model()
class Profile(models.Model):
	#user=models.OneToOneField(User, null=True, blank=True)
	#Name = models.CharField(max_length=120, null=True, blank=True)
	#Project_ID = user.get_username()
	#Email = user.get_full_name() # pre-filled
	user=models.OneToOneField(User, on_delete=models.CASCADE)
	Project_ID=models.CharField(max_length = 12, null=True, blank=True)
	Email=models.EmailField(max_length=120, null=True, blank=True)
# 	email = models.EmailField(max_length=120)
	#Main_analysis_type=user.Main_analysis_type
	Name = models.CharField(max_length=120, null=True)
	Group_leader = models.CharField(max_length=120, null=True)
	Affiliation = models.CharField(max_length=50, choices=AFFILIATIONTYPES, null=True)
	VIBAffiliation = models.CharField(max_length=60, choices=VIBAFFILIATIONTYPES, null=True, blank=True)
	Other_institution = models.CharField(max_length=60, null=True, blank=True)
	Phone = models.CharField(max_length=30, null=True)
	Address = models.CharField(max_length=300, null=True)
	#Project_ID = models.CharField(max_length=200, null=True) # pre-filled displayed on form template on the corner
	update = models.DateTimeField(auto_now=True)
	timestamp = models.DateTimeField(auto_now_add=True)
	login_count = models.PositiveIntegerField(default=0)
	def __unicode__(self):
		return self.user.username
	def __str__(self):
		return self.user.username
	#def getAnalysisType(self):
	#	return dict(Profile.ANALYSISTYPES)[self.Main_analysis_type]
	def getAnalysisType(self):
		return self.user.Main_analysis_type
	def getProjectID(self):
		return self.user.username
	def getEmail(self):
		return self.user.email

def login_user(sender,request, user, **kwargs):
	user.profile.login_count = user.profile.login_count + 1
	user.profile.save()

user_logged_in.connect(login_user)

@receiver(post_save, sender=User)
def create_user_profile(sender,instance,created, **kwargs):
	if created:
		Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender,instance, **kwargs):
	instance.profile.save()

# class Profile(models.Model):
# 	user=models.OneToOneField(User, on_delete=models.CASCADE)
# 	Name = models.CharField(max_length=120, null=True)
# 	Email = models.EmailField(max_length=120, null=True) # pre-filled
# 	Group_Leader = models.CharField(max_length=120, null=True)
# 	Affiliation = models.CharField(max_length=120 ,null=True)
# 	Affiliation_Type = models.CharField(max_length=50, choices=STUDYTYPES, null=True)
# 	Address = models.CharField(max_length=300, null=True)
# 	Project_ID = models.CharField(max_length=200, null=True) # pre-filled displayed on form template on the corner
# 	Main_Analysis_Type = models.CharField(max_length=50 , choices=ANALYSISTYPES, null=True)
# 	timestamp = models.DateTimeField(auto_now_add=True)
# 	def __unicode__(self):
# 		return self.Name
# 	def __str__(self):
# 		return self.Name
# 	def getAnalysisType(self):
# 		return dict(Profile.ANALYSISTYPES)[self.Main_analysis_type]

# @receiver(post_save, sender=User)
# def create_user_profile(sender,instance,created, **kwargs):
# 	if created:
# 		Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender,instance, **kwargs):
# 	instance.profile.save()


class Analysis(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	Project_title = models.CharField(max_length=50)
	Project_summary = models.CharField(max_length=1000)
	#Project_keywords = models.CharField(max_length=120)
	#Analysis_type = MultiSelectField(choices=ANALYSISTYPES) # pre-filled?!
	#Analysis_type2 = MultiSelectField(choices=ANALYSISTYPES2,
	#								max_choices=3,
     #                            	max_length=3, blank=True, null=True) # pre-filled?!
	Main_analysis_type = MultiSelectField(choices=ANALYSISTYPES, null=True, blank=True,max_choices=4) # pre-filled?!
	timestamp = models.DateTimeField(auto_now_add=True)
	#Analysis_type = models.CharField(max_length=50,default=None , choices=ANALYSISTYPES)
	Sample_preparation = models.BooleanField()
	Data_analysis = models.BooleanField()#choices=DATAANALYSIS)

	#Data_analysis = models.BooleanField()
#class Profile_extra(models.Model):
	#def __unicode__(self):
	#	return self.Name
	def __unicode__(self):
		return self.Project_title


# shotgun Specimen
# class Specimen_SG(models.Model):
# 	Species = models.CharField(max_length=120)
# 	Taxon_id = models.CharField(max_length=120, null=True)
# 	Protein_sequence_database_publically_available = models.BooleanField(choices=DATAANALYSIS, null=False,
# 		default=True)
# 	Sequence_database_name = models.CharField(max_length=50)
# 	Sequence_database_file = models.FileField(blank=True, storage=FileSystemStorage(location=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'media')))
# 	##Other_Relevant_
# 	##Other_Sequence_Database_File = models.FileField(upload_to='seqdbs')
# 	#Sample_Type_Delivered 
# 	Sample_type_delivered = models.CharField(max_length=50, null=False)
# 	#Sample_type_delivered = models.CharField(max_length=50 ,choices=SAMPLETYPES, null=False, default='cell pellet')
# 	#Sample_vial = models.CharField(max_length=120)
# 	# if applicable exact
# 	Buffer_Composition = models.CharField(max_length=300)
# 	#volume or estimation in ul / ml
# 	Volume = models.DecimalField(decimal_places=2, max_digits=6)
# 	VUnit = models.BooleanField(choices=VUNITS, default='μl', null=False,)
# 	Protein_concentration = models.DecimalField(decimal_places=2, max_digits=6)
# 	CUnit = models.CharField(max_length=10 , choices=CUNITS,null=False,default='μg/μl', blank=False)
# 	def __unicode__(self):
# 		return self.Species 	
# 	def get_absolute_url(self):
# 		return reverse('pportal:home')

# # PTM Specimen
# class Specimen_PTM(models.Model):
# 	Modification_Under_Investigation = models.CharField(max_length=120)
# 	Species = models.CharField(max_length=120)
# 	Taxon_id = models.CharField(max_length=120)
# 	Sequence_Database_Public_Availability = models.BooleanField(choices=DATAANALYSIS, null=False,
# 		default=True)
# 	Sequence_Database_Source = models.BooleanField()
# 	Sequence_Database_File = models.FileField()
# 	#Sample_Type_Delivered 
# 	Sample_Type = models.CharField(max_length=50 ,choices=SAMPLETYPES)
# 	Sample_Vial = models.CharField(max_length=120)
# 	Buffer_Composition = models.CharField(max_length=300)
# 	#volume or estimation in ul / ml
# 	Volume = models.FloatField()
# 	VUnit = models.BooleanField(choices=VUNITS)
# 	Protein_Concentration = models.FloatField()
# 	CUnit = models.CharField(max_length=10 , choices=CUNITS)
# 	def __unicode__(self):
# 		return self.Species 	

# # AP-MS Specimen
# class Specimen_APMS(models.Model):
# 	Bait_Molecule = models.BooleanField(choices=BAITS)
# 	# if protein 
# 	# antibodies used for IP
# 	IPAntibodies_names = models.CharField(max_length=120)
# 	# if applicable
# 	IPAntibodies_Supplier = models.CharField(max_length=120) 
# 	IPAntibodies_CatalogNumber = models.CharField(max_length=120)
# 	# amount or estimate
# 	Species = models.CharField(max_length=120)
# 	Taxon_id = models.CharField(max_length=120)
# 	Sequence_Database_Public_Availability = models.BooleanField(choices=DATAANALYSIS, null=False,
# 		default=True)
# 	Sequence_Database_Source = models.BooleanField()
# 	Sequence_Database_File = models.FileField()
# 	#Sample_Type_Delivered 
# 	Sample_Type = models.BooleanField(max_length=50, choices=SAMPLETYPESAPMS)
# 	Sample_Vial = models.CharField(max_length=120)
# 	Buffer_Composition = models.CharField(max_length=300)
# 	#volume or estimation in ul / ml
# 	Volume = models.FloatField()
# 	VUnit = models.BooleanField(choices=VUNITS)
# 	Protein_Concentration = models.FloatField()
# 	CUnit = models.CharField(max_length=10 , choices=CUNITS)
# 	def __unicode__(self):
# 		return self.Species 	

# # Gelband Specimen
# class Specimen_GB(models.Model):
# 	Experimental_Setup_Sample_Preparation = models.TextField(max_length=300) 
# 	Gel_GelBand_Image = models.FileField()
# 	Species = models.CharField(max_length=120)
# 	Taxon_id = models.CharField(max_length=120)
# 	Sequence_Database_Public_Availability = models.BooleanField(choices=DATAANALYSIS, null=False,
# 		default=True)
# 	Sequence_Database_Source = models.BooleanField()
# 	Sequence_Database_File = models.FileField()
# 	#Sample_Type_Delivered 
# 	Gel_Type = models.TextField(max_length=300)
# 	Gel_Supplier = models.CharField(max_length=120) 
# 	Gel_CatalogNumber = models.CharField(max_length=120)
# 	Gel_Staining_Method = models.CharField(max_length=120)
# 	Electrophoresis_Type = models.BooleanField(choices=PAGETYPES)
# 	Sample_Vial = models.CharField(max_length=120)
# 	# or estimation of
# 	Amount_Of_Protein_Loaded = models.CharField(max_length=300)
# 	Amount_Of_Protein_Loaded_Type = models.BooleanField(choices=GBCHOICES)
# 	#volume or estimation in ul / ml
# 	CUnit = models.CharField(max_length=10, choices=VUNITS, null=False,
# 		default=True)
# 	def __unicode__(self):
# 		return self.Species 	

# # reference: Django documentation
# examples/one_to_one

# class Experiment(models.Model):
# 	#def __init__(self):
# 	Isotopic_labeling = models.BooleanField(choices=DATAANALYSIS, null=False,
# 		default=True)
# 	Isotopic_labeling_details = models.CharField(max_length=20, blank=True)
# 	Nb_factors = models.IntegerField(blank=False, default = 1)
# 	Nb_conditions = models.IntegerField(blank=False, default = 1)
# 	# maybe instantiate another model called efactor (experimental factor) n times, n (Nb_factors)
# 	Factor_name_lst = models.CharField(max_length=120, null=True)
# 	Conditions_list = models.CharField(max_length=120, null=True)
# 	Nb_samples = models.IntegerField(blank=False, default = 0)
# 	Generic_Sample_Name = models.CharField(max_length=120, null=False)
# 	Sample_Name = models.CharField(max_length=120, null=True)
# 	# getmehods



#class 2 - form 1
# class Sample(models.Model): # biological specimen
# 	#def __init__(self):
# 	#Experiment.__init__(self)
# 	#experiment = models.OneToOneField(Experimental_Design, 
# 	#	on_delete=models.CASCADE,
# 	#	primary_key=True)
# 	Generic_Sample_Name = models.CharField(max_length=120, null=False, default="Sample")
# 	#Generic_Sample_Name = models.CharField(max_length=120, null=True)
# 	#Name = models.CharField(max_length=120, null=True)
# 	#Species = experiment.Species()
# 	Species = models.CharField(max_length=120, blank=False, default = None)
# 	#Taxon_ID = experiment.Taxon_ID()
# 	#Sample_Type_Delivered = experiment.Sample_Type_Delivered()
# 	Sample_Type_Delivered = models.CharField(max_length=50, blank=True)
# 	Buffer_composition = models.CharField(max_length=50, blank=True)
# 	Volume = models.CharField(max_length=20, blank=True)
# 	Protein_conc = models.CharField(max_length = 10, default = None)
# 	#Isotopic_labeling = experiment.Isotopic_labeling()
# 	def __unicode__(self):
# 		return self.Name



# class Experimental_Design(models.Model):
# 	'''Defined as a collection of Samples
# 	'''
# 	#def __init__(self, no_samples, no_factors, Generic_Sample_Name, Custom_Sample_Name):
# 	def __init__(self, no_samples, no_factors, generic_sample_name):
# 		# once this is created create a table with prefilled fields
# 		samples = list()
# 		Nb_samples = no_samples
# 		Nb_factors = no_factors
# 		Generic_Sample_Name = generic_sample_name
# 		for i in range(1,no_samples+1):
# 			sample = Sample(Nb_factors = no_factors, Generic_Sample_Name = generic_sample_name + str(i))
# 			samples.append(sample)


# old sanple		
# class Sample(models.Model):
# 	def __init__(self):
# 		Species = models.CharField(max_length=120, null=True)
# 		Taxon_ID = models.CharField(max_length=120, null=True)
# 		Protein_sequence_availability = models.BooleanField()
# 		Protein_sequence_database_availability = models.BooleanField()
# 		Protein_sequence_database = models.CharField(max_length=50,blank=True)
# 		Protein_sequences_file = models.FileField(upload_to='uploads/%Y/%m/%d/',blank=True)
# 		Sample_Type_Delivered = models.CharField(max_length=100)
# 		Isotopic_labeling = models.CharField(max_length=20, blank=True)
# 		Nb_factors = models.IntegerField(default=0)
# 		maybe instantiate another model called efactor (experimental factor) n times, n (Nb_factors)
# 		Factor_name_lst = models.CommaSeparatedIntegerField(max_length=120, null=True)
# 		Nb_samples = models.IntegerField(default=1)
# 		Generic_Sample_Name = models.CharField(max_length=120, null=True)
# 		getmehods