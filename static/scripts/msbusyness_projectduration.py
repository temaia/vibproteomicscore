# coding=UTF-8
import os
import json
from prcprojects.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings

import random
import csv
import re
import time
import math

class Command(BaseCommand):
    help='Gets # projects and scheduling state for states Sample_Prep, MS_Run, Data_Analysis'

    #def add_arguments(self, parser):
    #   parser.add_argument('usersfile', type=str, help='Indicates the number os users to be created')
        #User.objects.create_user(email=usor[0], password = usor[1],Main_analysis_type  = usor[2])

    def handle(self, *args, **kwargs):   
        inputfile =os.path.join(settings.BASE_DIR, "static/PRCCMBPSB_issues_dailyreport.csv")
        #outputfile ="/usr/local/www/apache24/data/PRCsite/vibproteomicscore/static/PRC_issues_dailyreport2.csv"
        # check session user status
        outputfileall =os.path.join(settings.BASE_DIR, "static/PRC_issues_dailyreport2all.csv")
        msoutfile =os.path.join(settings.BASE_DIR, "static/PRC_MassSpecs.csv")
        with open(inputfile, 'r', encoding='utf-8') as csvfile:
            csvfile_reader = csv.DictReader(csvfile)
            line_count = 0
            MS1Busyness=int()
            MS2Busyness=int()
            MS3Busyness=int()
            MS4Busyness=int()
            MS5Busyness=int()
            # 2d SP + 2d DA (per issue)
            MinWaitingTimes = list()
            i=0
            for row in csvfile_reader:
                MinWaitingTime = int(4) # weeks
                #print(row['total_running_time'])
                if row["Mass_Spectrometer"]=='Orbitrap Fusion Lumos' and row["State"] in ["Arrived","Sample_Prep","MS_Run"]:
                    if row['total_running_time']!='None':
                        if row['total_running_time']!=0:
                            #print(int(math.ceil(row['total_running_time']/24)))
                            MS1Busyness += int(row['total_running_time'])
                            #MinWaitingTime += math.ceil(int(row['total_running_time'])/24)
                        else:
                            MS1Busyness += int(row['total_running_time'])
                            #MinWaitingTime += int(row['total_running_time'])
                elif row["Mass_Spectrometer"]=='Q-Exactive HF' and row["State"] in ["Arrived","Sample_Prep","MS_Run"]:
                    if row['total_running_time']!='None':
                        if row['total_running_time']!=0:
                            MS2Busyness += int(row['total_running_time'])
                            #MinWaitingTime += math.ceil(int(row['total_running_time'])/24)
                        else:
                            MS2Busyness += int(row['total_running_time'])
                            #MinWaitingTime += int(row['total_running_time'])
                elif row["Mass_Spectrometer"]=='Q-Exactive HF Biopharma' and row["State"] in ["Arrived","Sample_Prep","MS_Run"]:
                    if row['total_running_time']!='None':
                        if row['total_running_time']!=0:
                            MS3Busyness += int(row['total_running_time'])
                            #MinWaitingTime += math.ceil(int(row['total_running_time'])/24)
                        else:
                            MS3Busyness += int(row['total_running_time'])
                            #MinWaitingTime += int(row['total_running_time'])
                elif row["Mass_Spectrometer"]=='Q-Exactive' and row["State"] in ["Arrived","Sample_Prep","MS_Run"]:
                    if row['total_running_time']!='None':
                        if row['total_running_time']!=0:
                            MS4Busyness += int(row['total_running_time'])
                            #MinWaitingTime += math.ceil(int(row['total_running_time'])/24)
                        else:
                            MS4Busyness += int(row['total_running_time'])
                            #MinWaitingTime += int(row['total_running_time'])
                elif row["Mass_Spectrometer"]=='LTQ Orbitrap Elite' and row["State"] in ["Arrived","Sample_Prep","MS_Run"]:
                    if row['total_running_time']!='None':
                        if row['total_running_time']!=0:
                            MS5Busyness += int(row['total_running_time'])
                            #MinWaitingTime += math.ceil(int(row['total_running_time'])/24)
                        else:
                            MS5Busyness += int(row['total_running_time'])
                            #MinWaitingTime += int(row['total_running_time'])
                else:
                    pass
                i+=1
                #print(str(i)+"_"+str(MinWaitingTime))
                MinWaitingTimes.append(i)
                    
        # write file with busyness per instrument
        with open(msoutfile, 'w', encoding='utf-8') as csvfile:
            #csvfile.write('Running start date\tLab PI\tType\tUser Name\tYouTrack\tProject Name (YouTrack)\t# samples\tMS_Injections_Per_Sample\trun length (hours)\ttotal running time (hours)\tMass_Spectrometer\tCreated_DateH\tArrival_DateH\tMS_RunStateH\tMS_RunStatesH\tMS_RunStatesnrH\tre-runs/problems\tMS_RunStartH\tMS_RunStartsH\tMS_RunStartsnrH\tresolvedH\tResolvedDateH\tCleatedDate\n')
            csvfile.write('Mass_Spectrometer,total_running_time_days\n')
            csvfile.write('Orbitrap Fusion Lumos,' + str(round(MS1Busyness/(24*5)))+'\n')
            csvfile.write('Q-Exactive HF,' + str(round(MS2Busyness/(24*5)))+'\n')
            csvfile.write('Q-Exactive HF Biopharma,' + str(round(MS3Busyness/(24*5)))+'\n')
            csvfile.write('Q-Exactive,' + str(round(MS4Busyness/(24*5)))+'\n')
            csvfile.write('LTQ Orbitrap Elite,' + str(round(MS5Busyness/(24*5)))+'\n')
            csvfile.close() 

        with open(inputfile, 'r', encoding='utf-8') as csvfile:
            csvfile_reader = csv.DictReader(csvfile)
            line_count = 0
            MS1Busyness=int()
            MS2Busyness=int()
            MS3Busyness=int()
            MS4Busyness=int()
            MS5Busyness=int()
            # 2d SP + 2d DA (per issue)
            MinWaitingTimes = list()
            i=0
            for row in csvfile_reader:
                #MinWaitingTime = int(4) # weeks
                #print(row['total_running_time'])
                #print(row["Mass_Spectrometer"])
                if row["Mass_Spectrometer"]=='Orbitrap Fusion Lumos' and row["State"] in ["Created","Arrived","Sample_Prep","MS_Run", "Data_Analysis", "Closed"]:
                    if row['total_running_time']!='None':
                        if row['total_running_time']!=0:
                            #print(int(math.ceil(row['total_running_time']/24)))
                            MS1Busyness += int(row['total_running_time'])
                            #MinWaitingTime += math.ceil(int(row['total_running_time'])/24)
                        else:
                            MS1Busyness += int(row['total_running_time'])
                            #MinWaitingTime += int(row['total_running_time'])
                elif row["Mass_Spectrometer"]=='Q-Exactive HF' and row["State"] in ["Created","Arrived","Sample_Prep","MS_Run", "Data_Analysis", "Closed"]:
                    if row['total_running_time']!='None':
                        if row['total_running_time']!=0:
                            MS2Busyness += int(row['total_running_time'])
                            #MinWaitingTime += math.ceil(int(row['total_running_time'])/24)
                        else:
                            MS2Busyness += int(row['total_running_time'])
                            #MinWaitingTime += int(row['total_running_time'])
                elif row["Mass_Spectrometer"]=='Q-Exactive HF Biopharma' and row["State"] in ["Created","Arrived","Sample_Prep","MS_Run", "Data_Analysis", "Closed"]:
                    if row['total_running_time']!='None':
                        if row['total_running_time']!=0:
                            MS3Busyness += int(row['total_running_time'])
                            #MinWaitingTime += math.ceil(int(row['total_running_time'])/24)
                        else:
                            MS3Busyness += int(row['total_running_time'])
                            #MinWaitingTime += int(row['total_running_time'])
                elif row["Mass_Spectrometer"]=='Q-Exactive' and row["State"] in ["Created","Arrived","Sample_Prep","MS_Run", "Data_Analysis", "Closed"]:
                    if row['total_running_time']!='None':
                        if row['total_running_time']!=0:
                            MS4Busyness += int(row['total_running_time'])
                            #MinWaitingTime += math.ceil(int(row['total_running_time'])/24)
                        else:
                            MS4Busyness += int(row['total_running_time'])
                            #MinWaitingTime += int(row['total_running_time'])
                elif row["Mass_Spectrometer"]=='LTQ Orbitrap Elite' and row["State"] in ["Created","Arrived","Sample_Prep","MS_Run", "Data_Analysis", "Closed"]:
                    if row['total_running_time']!='None':
                        if row['total_running_time']!=0:
                            MS5Busyness += int(row['total_running_time'])
                            #MinWaitingTime += math.ceil(int(row['total_running_time'])/24)
                        else:
                            MS5Busyness += int(row['total_running_time'])
                            #MinWaitingTime += int(row['total_running_time'])
                else:
                    pass
                i+=1
                #print(str(i)+"_"+str(MinWaitingTime))
                MinWaitingTimes.append(i)
        # add expected duration to issue (to be refined)
        with open(inputfile, 'r', encoding='utf-8') as in_f, open(outputfileall, 'w', newline='', encoding='utf-8') as out_f:
            data = [item for item in csv.reader(in_f)]
            # to be revised
            MedianWTime = 34
            MedianWTime_col = ["Median_wTime"]+[MedianWTime]*len(MinWaitingTimes)
            #MinWaitingTimes = ["Min_wTime"]+MinWaitingTimes
            new_data = []
            for i, item in enumerate(data):
                try:
                    item.append(MedianWTime_col[i])
                    #item.append(MinWaitingTimes[i])
                except IndexError as e:
                    item.append("placeholder")
                    #item.append("placeholder")
                new_data.append(item)
            csv.writer(out_f).writerows(new_data)
