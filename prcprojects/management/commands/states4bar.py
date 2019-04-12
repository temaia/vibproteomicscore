# coding=UTF-8
import csv
import os
import json
from prcprojects.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings
import random
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
        #outputfile ="/home/pportal/dev2Sep18/prcsite/vibproteomicscore/static/PRC_issues_dailyreport2.csv"
        #outputfileall ="/home/pportal/dev2Sep18/prcsite/vibproteomicscore/static/static/PRC_issues_dailyreport2all.csv"
        statesoutfile =os.path.join(settings.BASE_DIR, "static/PRCCMBPSB_States.json" )


        with open(inputfile, 'r', encoding='utf-8') as csvfile:
            csvfile_reader = csv.DictReader(csvfile)
            line_count = 0
            Nb_Projects_SP_S=0
            Nb_Projects_SP_NS=0
            Nb_Projects_MS_S=0
            Nb_Projects_MS_NS=0
            Nb_Projects_DA_S=0
            Nb_Projects_DA_NS=0
            # 2d SP + 2d DA (per issue)
            #Nb_Projects = list()
            i=0
            for row in csvfile_reader:
                #print(row['total_running_time'])
                if row['Scheduling_State']=='Scheduled' and row["State"]=="Data_Analysis":# ["Arrived","Sample_Prep","MS_Run", "Data_Analysis"]:
                    Nb_Projects_DA_S +=1
                if row['Scheduling_State']=='NotScheduled' and row["State"]=="Data_Analysis":# ["Arrived","Sample_Prep","MS_Run", "Data_Analysis"]:
                    Nb_Projects_DA_NS +=1
                if row['Scheduling_State']=='Scheduled' and row["State"]=="Sample_Prep":# ["Arrived","Sample_Prep","MS_Run", "Data_Analysis"]:
                    Nb_Projects_SP_S +=1
                if row['Scheduling_State']=='NotScheduled' and row["State"]=="Sample_Prep":# ["Arrived","Sample_Prep","MS_Run", "Data_Analysis"]:
                    Nb_Projects_SP_NS +=1
                if row['Scheduling_State']=='Scheduled' and row["State"]=="MS_Run":# ["Arrived","Sample_Prep","MS_Run", "Data_Analysis"]:
                    Nb_Projects_MS_S +=1
                if row['Scheduling_State']=='NotScheduled' and row["State"]=="MS_Run":# ["Arrived","Sample_Prep","MS_Run", "Data_Analysis"]:
                    Nb_Projects_MS_NS +=1 
                else:
                    pass

        # write file with busyness per instrument
        with open(statesoutfile, 'w') as csvfile:
            #csvfile.write('Running start date\tLab PI\tType\tUser Name\tYouTrack\tProject Name (YouTrack)\t# samples\tMS_Injections_Per_Sample\trun length (hours)\ttotal running time (hours)\tMass_Spectrometer\tCreated_DateH\tArrival_DateH\tMS_RunStateH\tMS_RunStatesH\tMS_RunStatesnrH\tre-runs/problems\tMS_RunStartH\tMS_RunStartsH\tMS_RunStartsnrH\tresolvedH\tResolvedDateH\tCleatedDate\n')
            json.dump({'Waiting':[Nb_Projects_SP_NS, Nb_Projects_MS_NS, Nb_Projects_DA_NS],
                       'Processed':[Nb_Projects_SP_S, Nb_Projects_MS_S, Nb_Projects_DA_S]},csvfile)
            #json.dump({'Processed':[Nb_Projects_SP_S, Nb_Projects_MS_S, Nb_Projects_DA_S]},csvfile)
            #csvfile.write('Scheduled,'+str(Nb_Projects_SP_S'\n')
            #csvfile.write('NotScheduled,' + '\n')
            #csvfile.close() 
                
        ##print(i)
        ##
        ##with open(inputfile, 'r') as in_f, open(statesoutfile, 'w', newline='') as out_f:
        ##    data = [item for item in csv.reader(in_f)]
        ##    # to be revised
        ##    MedianWTime = 34
        ##    MedianWTime_col = ["Median_wTime"]+[MedianWTime]*len(MinWaitingTimes)
        ##    MinWaitingTimes = ["Min_wTime"]+MinWaitingTimes
        ##    new_data = []
        ##    for i, item in enumerate(data):
        ##        try:
        ##            item.append(MedianWTime_col[i])
        ##            item.append(MinWaitingTimes[i])
        ##        except IndexError as e:
        ##            item.append("placeholder")
        ##            item.append("placeholder")
        ##        new_data.append(item)
        ##    csv.writer(out_f).writerows(new_data)



