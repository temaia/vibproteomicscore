#!/usr/bin/python
# -*- coding: utf-8 -*-
import io
import os
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
    worksheet_s.write(3, 1, ugettext("Description"), header) # from dropdown from parsed conditions Experimental_conditions
    #worksheet_s.write(3, 2, ugettext("Isotopic label"), header) # from dropdown from parsed conditions Isotopic_label
    worksheet_s.write(3, 2, ugettext("Replicate"), header) # pre filled 123 123 if total/3 = 0 else,jjjjj
    worksheet_s.write(3, 3, ugettext("Estimated MW"), header) #add Sample type value and leave free for editing
    worksheet_s.write(3, 4, ugettext("Buffer composition"), header) #add Buffer composition value and leave free for editing (space dows not matter)
    worksheet_s.write(3, 5, ugettext("Amount/Concentration of protein (μg or μg/μl)"), header) #format digits (2 decimals) leave for edit
    #worksheet_s.write(3, 5, ugettext("Sample amount (protein mass (or estimation of) (μg)"), header) #format digits (2 decimals) leave for edit
    worksheet_s.write(3, 6, ugettext("Volume (μl)"), header) #  #format digits (2 decimals) leave for edit
    worksheet_s.write(3, 7, ugettext("Other relevant information"), header) # leave free

    # generate values to prepopulate table
    #idx = 1
    # experimental conditions
    ec = arguments_dict["2-Experimental_conditions"][0].replace(' ','').split(',')
    print(ec)
    no_ec = len(ec)
    #parsimonious list for replicates
    no_replicates = int(arguments_dict["2-Nb_replicates_per_condition"][0].replace(' ',''))
    no_samples = int(arguments_dict["2-Nb_samples"][0].replace(' ',''))
    print('nosa'+str(no_samples))
    # predicted no_ec
    pno_ec = no_samples//no_replicates + no_samples%no_replicates
    plist = list(range(1,no_replicates+1,1))*pno_ec
    eclist = []
    for ec0 in ec:
        for rep in range(1,no_replicates+1,1):
            eclist.append(ec0)
    eclist =eclist + [""]*(no_samples-len(eclist))
    #for rep in range(1,no_replicates+1,1):
    #    eclist.append('')
    # buffer
    #print(eclist)
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
        worksheet_s.write_string(row, 2, "rep_" + str(plist[idx]), celledit)
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
    worksheet_s.set_column('B:B', 15.8)  # Experimental Condition
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
