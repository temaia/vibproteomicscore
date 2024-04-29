#!/usr/bin/python
# -*- coding: utf-8 -*-
import io
import os
import re
import random
from django.conf import settings
import xlsxwriter
from django.utils.translation import ugettext
from django.db.models import Avg, Sum, Max, Min

#from .models import Town, Weather


def WriteToExcel4(arguments_dict):
    #output = io.BytesIO()
    output = os.path.join(settings.MEDIA_ROOT, os.path.join("ED","Experimental_design_"+arguments_dict["PID"]+".xlsx"))
    #output = "media/ED/Experimental_design_"+arguments_dict["PID"]+".xlsx"
    workbook = xlsxwriter.Workbook(output)
    worksheet_s = workbook.add_worksheet("main")
    # add more Sheets
    #worksheet_b = workbook.add_worksheet("opts sheet")
    
    # excel styles
    title = workbook.add_format({
        'bold': True,
        'font_size': 12,
        'align': 'center',
        'valign': 'vcenter'
    })
    header = workbook.add_format({
        'bg_color': '#F7F7F7',
        'color': 'black',
        'align': 'center',
        'valign': 'top',
        'border': 1,
    })
    cell = workbook.add_format({
        'align': 'center',
        'valign': 'top',
        'text_wrap': True,
        'border': 1,
    })
    cellneditleft = workbook.add_format({
        'align': 'left',
        'valign': 'top',
        'text_wrap': True,
        'border': 1,
        #'italic':True,
        #'font_color':"FF6600"
        #'bg_color':"cee7f4"
    })
    cellnedit = workbook.add_format({
        'align': 'center',
        'valign': 'top',
        'text_wrap': True,
        'border': 1,
        #'italic':True,
        #'font_color':"FF6600"
        #'bg_color':"cee7f4"
    })
    celledit = workbook.add_format({
        'align': 'center',
        'valign': 'top',
        'text_wrap': True,
        'border': 1,
        #'italic':True,
        'font_color':"FF6600"
        #'bg_color':"cee7f4"
    })
    cell_center = workbook.add_format({
        'align': 'center',
        'valign': 'top',
        'border': 1
    })

    # write title
    title_text = "Sample details"# "+arguments_dict["PID"]
    #print(title_text)
    
    #title_text = u"{0} {1}".format(ugettext("Experiment_ID"), user.profile.issue)
    # merge cells
    worksheet_s.merge_range('D2:F2', title_text, title)
    #print(type(arguments_dict["3-Isotopic_labeling"][0]))
    # write header
    worksheet_s.write(3, 0, ugettext("Sample Name"), header) # project-ID+counter
    worksheet_s.write(3, 1, ugettext("Experimental_condition"), header) # from dropdown from parsed conditions Experimental_conditions
    #worksheet_s.write(3, 2, ugettext("Isotopic label"), header) # from dropdown from parsed conditions Isotopic_label
    worksheet_s.write(3, 2, ugettext("Replicate"), header) # pre filled 123 123 if total/3 = 0 else,jjjjj
    worksheet_s.write(3, 3, ugettext("Estimated MW"), header) #add Sample type value and leave free for editing
    worksheet_s.write(3, 4, ugettext("Buffer composition"), header) #add Buffer composition value and leave free for editing (space dows not matter)
    worksheet_s.write(3, 5, ugettext("Concentration of protein (μg/μl)"), header) #format digits (2 decimals) leave for edit
    #worksheet_s.write(3, 5, ugettext("Sample amount (protein mass (or estimation of) (μg)"), header) #format digits (2 decimals) leave for edit
    worksheet_s.write(3, 6, ugettext("Volume (μl)"), header) #  #format digits (2 decimals) leave for edit
    worksheet_s.write(3, 7, ugettext("Other relevant information"), header) # leave free

    ec = arguments_dict["2-Experimental_conditions"][0].replace(' ','').split(',')
    print(ec)
    no_ec = len(ec)
    
    no_samples = int(arguments_dict["2-Nb_samples"][0].replace(' ',''))
    print('nosa'+str(no_samples))
    #parsimonious list for replicates
    no_replicates = arguments_dict["2-Nb_replicates_per_condition"][0].replace(' ','').split(',')
    print(no_replicates)
    # fill in no_replicates list in case it does not match the number of ec
    # remove?
    if len(no_replicates)<no_ec:
        no_replicates = no_replicates+no_replicates*(no_ec-len(no_replicates))
    print(no_replicates)
    # convert to list
    def getrepnos(no_replicates_lst, no_samples,no_ecf):
        no_replicates_lstnew = list()
        #no_replicates_lst=no_replicates.replace(' ','').split(',')
        
        for i in range(len(no_replicates_lst)):
            # print(no_replicates_lst[i])
            try:
                no_replicates_lstnew.append(int(no_replicates_lst[i]))
            except ValueError:
                try:
                    no_replicates_lstnew.append(int(re.findall(r'\d+',no_replicates_lst[i])[0]))
                except IndexError:
                    no_replicate_i = no_samples//no_ecf
                    if i==(len(no_replicates_lst)-1):
                        no_replicate_i+=no_samples%no_ecf
                    print("norepi"+str(no_replicate_i))
                    no_replicates_lstnew.append(no_replicate_i)
        return no_replicates_lstnew
    no_replicates = getrepnos(no_replicates, no_samples, no_ec)
    #no_replicates = [int(x) for x in no_replicates]    
    # convert to list
    print(no_replicates)
    # predicted no_ec
    #pno_ec = no_samples//no_replicates + no_samples%no_replicates
    #replicates = list(range(1,no_replicates+1))
    # dictionary with ecs as keys and as values the sample names
    samples_dict = dict()
    #counter = 1
    for i in range(len(ec)):
        #replicates_temp = random.sample(replicates, len(replicates))
        #expcond_temp = random.sample(expcond, len(expcond))
        #for j in range(nb_replicates):
            #ec_order.append(expcond[i] + str(replicates_temp[j]))
            #sn_order.append(("_").join([project, str(counter)]))
            #counter+=1
        #ec=random.sample(ec, len(ec))
        samplestemp = list()
        #for j in no_replicates
        for j in range(1,no_replicates[i]+1):
            samplestemp.append(ec[i]+"_"+str(j))
            #samplestemp.append(ec[i]+str(replicates[j]))
        samples_dict[ec[i]] = samplestemp
    eclist = list()
    replicatelist = list()
    maxno_replicates = max(no_replicates)
    #lentemp = no_replicates
    for j in range(maxno_replicates):
        #for i in range(no_replicates*len(ec)):
        # nb samples left per condition
        nbsamplesperectemp = [len(s) for s in samples_dict.values()]
        # condition indexes with samples left
        c2samplefrom = [i for i, x in enumerate(nbsamplesperectemp) if x!=0]
        # order of experimental conditions to sample from which still have samples left
        ectempindexes = random.sample(range(len(ec)), len(ec))
        ectemp = [ec[ix] for ix in ectempindexes]
        #ectemp2 = [ectemp[i] for i in c2samplefrom]
        for i in range(len(ec)):
            if len(samples_dict[ectemp[i]])>0:
                # index defining which sample from each condition ec[i] will be chosen
                samplelistindexestemp = random.sample(range(nbsamplesperectemp[ectempindexes[i]]),1)
                sampletemp = samples_dict[ectemp[i]].pop(samplelistindexestemp[0]).split("_")
                eclist.append(sampletemp[0])
                replicatelist.append(sampletemp[1])
    no_samplesleft = no_samples-len(eclist)
    eclist = eclist + ['']*no_samplesleft
    replicatelist = replicatelist + ['']*no_samplesleft
    # NEW
    saunit = ['μg of protein','# of cells']
    # add data to the table
    for idx in range(0,no_samples,1):
        row = idx+5
        print(idx)
        # sample name
        worksheet_s.write_string(row, 0, arguments_dict["PID"] + "_" + str(idx+1), cell_center)
        # experimental conditions
        worksheet_s.write_string(row, 1, eclist[idx], celledit)
        worksheet_s.data_validation(row, 1,row, 1, { 'validate' :'list',
                                            'source' : ec})
        # isotopic labels
        #worksheet_s.write_string(row, 2, "labels", celledit) # make remark at the end
        # replicate
        if str(replicatelist[idx])!="":
            worksheet_s.write_string(row, 2, str(replicatelist[idx]), celledit)
        else:
            worksheet_s.write_string(row, 2, "", celledit)
        # sample type delivered
        worksheet_s.write_string(row, 3, '', celledit)
        # buffer composition
        worksheet_s.write_string(row, 4, '', celledit)

        # protein 
        worksheet_s.write_number(row, 5, 0.00, celledit)
        worksheet_s.data_validation(row, 5,row, 5, {'validate':'decimal',
                                              'criteria': '>',
                                              'value':'0.00'})
        # volume
        worksheet_s.write_number(row, 6, 0.00, celledit)

        worksheet_s.data_validation(row, 6, row, 6, {'validate':'decimal',
                                              'criteria': '>',
                                              'value':'0.00'})
        # Other relevant information
        worksheet_s.write_string(row, 7, '', celledit)

        # if len(data.town.name) > town_col_width:
        #     town_col_width = len(data.town.name)

        # worksheet_s.write(row, 2, data.date.strftime('%d/%m/%Y'), cell_center)
        # worksheet_s.write_string(row, 3, data.description, cell)
        # if len(data.description) > description_col_width:
        #     description_col_width = len(data.description)

        # worksheet_s.write_number(row, 4, data.max_temperature, cell_center)
        # worksheet_s.write_number(row, 5, data.min_temperature, cell_center)
        # worksheet_s.write_number(row, 6, data.wind_speed, cell_center)
        # worksheet_s.write_number(row, 7, data.precipitation, cell_center)
        # worksheet_s.write_number(row, 8,
        #                          data.precipitation_probability, cell_center)

        # observations = data.observations.replace('\r', '')
        # worksheet_s.write_string(row, 9, observations, cell)
        # observations_rows = compute_rows(observations, observations_col_width)
        # worksheet_s.set_row(row, 15 * observations_rows)
        #idx+=1
    idx += 7
    span = 'B'+str(idx)+':D'+str(idx)
    span2 = 'B'+str(idx+1)+':D'+str(idx+1)
    worksheet_s.merge_range(span,"- please edit and review the fields in orange", cellneditleft)
    #worksheet_s.merge_range(span2,"- * according to if the sample is protein extract or cell pellet, respectively", cellneditleft)
     
    # change column widths
    worksheet_s.set_column('A:A', 14.3)  # Sample Name



    worksheet_s.set_column('B:B', 20.8)  # Experimental Condition

    #worksheet_s.set_column('C:C', 12.6)  # Isotopic label
    worksheet_s.set_column('C:C', 9.5)  # Replicate
    worksheet_s.set_column('D:D', 15.8)  # Molecular weight
    worksheet_s.set_column('E:E', 25.0)  # Buffer composition
    worksheet_s.set_column('F:F', 40.0)  # Protein mass
    worksheet_s.set_column('G:G', 15.0)  # Volume
    worksheet_s.set_column('H:H', 30.0)  # Other relevant info
    #worksheet_s.set_column('J:J', 25.0)  # Observations column
   
    # close workbook
    workbook.close()
    #xlsx_data = output
    #xlsx_data = output.getvalue()
    #return xlsx_data


def compute_rows(text, width):
    if len(text) < width:
        return 1
    phrases = text.replace('\r', '').split('\n')

    rows = 0
    for phrase in phrases:
        if len(phrase) < width:
            rows = rows + 1
        else:
            words = phrase.split(' ')
            temp = ''
            for idx, word in enumerate(words):
                temp = temp + word + ' '
                # check if column width exceeded
                if len(temp) > width:
                    rows = rows + 1
                    temp = '' + word + ' '
                # check if it is not the last word
                if idx == len(words) - 1 and len(temp) > 0:
                    rows = rows + 1
    return rows
