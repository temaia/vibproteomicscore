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


def WriteToExcel(arguments_dict):
    #WriteToExceloutput = io.BytesIO()
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
    title_text = "Experimental design and sample details"# "+arguments_dict["PID"]
    #print(title_text)
    
    #title_text = u"{0} {1}".format(ugettext("Experiment_ID"), user.profile.issue)
    # merge cells
    worksheet_s.merge_range('D2:F2', title_text, title)
    #print(type(arguments_dict["3-Isotopic_labeling"][0]))
    if arguments_dict["3-Isotopic_labeling"][0] == 'False':
    # write header
        worksheet_s.write(3, 0, ugettext("Sample Name"), header) # project-ID+counter
        # remove?workshe
        worksheet_s.write(3, 1, ugettext("Experimental Condition"), header) # from dropdown from parsed conditions Experimental_conditions
        #worksheet_s.write(3, 2, ugettext("Isotopic label"), header) # from dropdown from parsed conditions Isotopic_label
        worksheet_s.write(3, 2, ugettext("Replicate"), header) # pre filled 123 123 if total/3 = 0 else,jjjjj
        worksheet_s.write(3, 3, ugettext("Sample type delivered"), header) #add Sample type value and leave free for editing
        worksheet_s.write(3, 4, ugettext("Buffer composition"), header) #add Buffer composition value and leave free for editing (space dows not matter)
        worksheet_s.write(3, 5, ugettext("Sample amount"), header) #format digits (2 decimals) leave for edit
        worksheet_s.write(3, 6, ugettext("Unit (μg of protein / # of cells *)"), header) #format digits (2 decimals) leave for edit
        #worksheet_s.write(3, 5, ugettext("Sample amount (protein mass (or estimation of) (μg)"), header) #format digits (2 decimals) leave for edit
        worksheet_s.write(3, 7, ugettext("Volume (if applicable) (μl)"), header) #  #format digits (2 decimals) leave for edit
        worksheet_s.write(3, 8, ugettext("Other relevant information"), header) # leave free

        #print(arguments_dict.keys())

        # # column widths
        # town_col_width = 10
        # description_col_width = 10
        # observations_col_width = 25
     #    dict_keys(['csrfmiddlewaretoken', 'contact_wizard_sg-current_step', '2-Species', '2-Sequence_Database_Public_Availability',
     # '2-Sequence_database_name', '2-Sequence_database_file', '2-Sample_Type', '2-Buffer_composition', 
     # '3-Experimental_conditions', '3-Conditions_to_compare', '3-Nb_replicates_per_condition', 
     # '3-Nb_samples', '3-Isotopic_labeling', '3-Isotopic_labeling_details', 'PID'])

        # generate values to prepopulate table
        #idx = 1
        # experimental conditions into list
        ec = arguments_dict["3-Experimental_conditions"][0].replace(' ','').split(',')
        print(ec)
        no_ec = len(ec)
        
        no_samples = int(arguments_dict["3-Nb_samples"][0].replace(' ',''))
        print('nosa'+str(no_samples))
        #parsimonious list for replicates
        no_replicates = arguments_dict["3-Nb_replicates_per_condition"][0].replace(' ','').split(',')
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
            #print('samplestemp')
            #print(samplestemp)
            samples_dict[ec[i]] = samplestemp
        eclist = list()
        replicatelist = list()
        maxno_replicates = max(no_replicates)
        #lentemp = no_replicates
        for j in range(maxno_replicates):
            #for i in range(no_replicates*len(ec)):
            # nb samples left per condition
            nbsamplesperectemp = [len(s) for s in samples_dict.values()]
            #print('nbsamples')
            #print(nbsamplesperectemp)
            # condition indexes with samples left
            c2samplefrom = [i for i, x in enumerate(nbsamplesperectemp) if x!=0]
            # order of experimental conditions to sample from which still have samples left
            ectempindexes = random.sample(range(len(ec)), len(ec))
            ectemp = [ec[ix] for ix in ectempindexes]
            #print("ectemp")
            #print(ectemp)
            #ectemp2 = [ectemp[i] for i in c2samplefrom]
            for i in range(len(ec)):
                if len(samples_dict[ectemp[i]])>0:
                    # index defining which sample from each condition ec[i] will be chosen
                    try:
                        samplelistindexestemp = random.sample(range(nbsamplesperectemp[ectempindexes[i]]),1)
                        sampletemp = samples_dict[ectemp[i]].pop(samplelistindexestemp[0]).split("_")
                        eclist.append(sampletemp[0])
                        replicatelist.append(sampletemp[1])
                    except IndexError:
                        replicatelist.append("")
        no_samplesleft = no_samples-len(eclist)
        eclist = eclist + ['']*no_samplesleft
        replicatelist = replicatelist + ['']*no_samplesleft
        # NEW
        saunit = ['μg of protein','# of cells']
        #for rep in range(1,no_replicates+1,1):
        #    eclist.append('')
        # buffer
        #print(eclist)
        #print(replicatelist)
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
            worksheet_s.write_string(row, 3, arguments_dict['2-Sample_Type'][0], celledit)
            # buffer composition
            worksheet_s.write_string(row, 4, arguments_dict['2-Buffer_composition'][0], celledit)

            # sample amount
            worksheet_s.write_number(row, 5, 0.00, celledit)
            worksheet_s.data_validation(row, 5,row, 5, {'validate':'decimal',
                                                  'criteria': '>',
                                                  'value':'0.00'})
            # sample amount unit
            worksheet_s.write_string(row, 6, "", celledit)
            worksheet_s.data_validation(row, 6,row, 6, {'validate':'list',
                                                  'source': saunit})
            # volume
            worksheet_s.write_number(row, 7, 0.00, celledit)

            worksheet_s.data_validation(row, 7, row, 7, {'validate':'decimal',
                                                  'criteria': '>',
                                                  'value':'0.00'})
            # Other relevant information
            worksheet_s.write_string(row, 8, '', celledit)

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
        worksheet_s.merge_range(span2,"- * according to if the sample is protein extract or cell pellet, respectively", cellneditleft)
         
        # change column widths
        worksheet_s.set_column('A:A', 14.3)  # Sample Name
        worksheet_s.set_column('B:B', 20.8)  # Experimental Condition
        #worksheet_s.set_column('C:C', 12.6)  # Isotopic label
        worksheet_s.set_column('C:C', 9.5)  # Replicate
        worksheet_s.set_column('D:D', 22.0)  # Sample type delivered
        worksheet_s.set_column('E:E', 16.0)  # Buffer composition
        worksheet_s.set_column('F:F', 18.0)  # Protein mass
        worksheet_s.set_column('G:G', 28.0)  # Protein mass unit
        worksheet_s.set_column('H:H', 23.0)  # Volume
        worksheet_s.set_column('I:I', 28.0)  # Other relevant info
        #worksheet_s.set_column('J:J', 25.0)  # Observations column


        # row = row + 1
        # # Adding some functions for the data
        # max_temp_avg = Weather.objects.all().aggregate(Avg('max_temperature'))
        # worksheet_s.write_formula(row, 4,
        #                           '=average({0}{1}:{0}{2})'.format('E', 6, row),
        #                           cell_center,
        #                           max_temp_avg['max_temperature__avg'])
        # min_temp_avg = Weather.objects.all().aggregate(Avg('min_temperature'))
        # worksheet_s.write_formula(row, 5,
        #                           '=average({0}{1}:{0}{2})'.format('F', 6, row),
        #                           cell_center,
        #                           min_temp_avg['min_temperature__avg'])
        # wind_avg = Weather.objects.all().aggregate(Avg('wind_speed'))
        # worksheet_s.write_formula(row, 6,
        #                           '=average({0}{1}:{0}{2})'.format('G', 6, row),
        #                           cell_center,
        #                           wind_avg['wind_speed__avg'])
        # precip_sum = Weather.objects.all().aggregate(Sum('precipitation'))
        # worksheet_s.write_formula(row, 7,
        #                           '=sum({0}{1}:{0}{2})'.format('H', 6, row),
        #                           cell_center,
        #                           precip_sum['precipitation__sum'])
        # precip_prob_avg = Weather.objects.all() \
        #     .aggregate(Avg('precipitation_probability'))
        # worksheet_s.write_formula(row, 8,
        #                           '=average({0}{1}:{0}{2})'.format('I', 6, row),
        #                           cell_center,
        #                           precip_prob_avg['precipitation_probability__avg'])

        # worksheet_d = workbook.add_worksheet("Chart Data")

        # if town:
        #     towns = [town]
        # else:
        #     towns = Town.objects.all()

        # # Creating the Line Chart
        # line_chart = workbook.add_chart({'type': 'line'})
        # # adding dates for the values
        # dates = Weather.objects.order_by('date').filter(
        #     town=Town.objects.first()).values_list('date', flat=True)
        # str_dates = []
        # for d in dates:
        #     str_dates.append(d.strftime('%d/%m/%Y'))
        # worksheet_d.write_column('A1', str_dates)
        # worksheet_d.set_column('A:A', 10)

        # # add data for the line chart
        # for idx, t in enumerate(towns):
        #     data = Weather.objects.order_by('date').filter(town=t)
        #     letter_max_t = chr(ord('B') + idx)
        #     letter_min_t = chr(ord('B') + idx + len(towns))
        #     worksheet_d.write_column(
        #         "{0}1".format(letter_max_t),
        #         data.values_list('max_temperature', flat=True))
        #     worksheet_d.write_column(
        #         "{0}1".format(letter_min_t),
        #         data.values_list('min_temperature', flat=True))

        #     # add data to line chart series
        #     line_chart.add_series({
        #         'categories': '=Chart Data!$A1:$A${0}'.format(len(dates)),
        #         'values': '=Chart Data!${0}${1}:${0}${2}'
        #         .format(letter_max_t, 1, len(data)),
        #         'marker': {'type': 'square'},
        #         'name': u"{0} {1}".format(ugettext("Max T."), t.name)
        #     })
        #     line_chart.add_series({
        #         'categories': '=Chart Data!$A1:$A${0}'.format(len(dates)),
        #         'values': '=Chart Data!${0}${1}:${0}${2}'
        #         .format(letter_min_t, 1, len(data)),
        #         'marker': {'type': 'circle'},
        #         'name': u"{0} {1}".format(ugettext("Min T."), t.name)
        #     })
        # # adding other options
        # line_chart.set_title({'name': ugettext("Maximum and Minimum Temperatures")})
        # line_chart.set_x_axis({
        #     'text_axis': True,
        #     'date_axis': False
        # })
        # line_chart.set_y_axis({
        #     'num_format': u'## ℃'
        # })
        # # Insert Chart to "Charts" Sheet
        # worksheet_c.insert_chart('B2', line_chart, {'x_scale': 2, 'y_scale': 1})

        # # Creating the column chart
        # bar_chart = workbook.add_chart({'type': 'column'})

        # # creating data for column chart
        # cell_index = len(towns) * 2 + 2
        # for idx, t in enumerate(towns):
        #     max_wind = Weather.objects.filter(town=t).aggregate(Max('wind_speed'))
        #     min_wind = Weather.objects.filter(town=t).aggregate(Min('wind_speed'))
        #     worksheet_d.write_string(idx, cell_index, t.name)
        #     worksheet_d.write_number(
        #         idx, cell_index + 1, max_wind['wind_speed__max'])
        #     worksheet_d.write_number(
        #         idx, cell_index + 2, min_wind['wind_speed__min'])

        # # add series
        # bar_chart.add_series({
        #     'name': 'Max Speed',
        #     'values': '=Chart Data!${0}${1}:${0}${2}'
        #     .format(chr(ord('A') + cell_index + 1), 1, len(towns)),
        #     'categories': '=Chart Data!${0}${1}:${0}${2}'
        #     .format(chr(ord('A') + cell_index), 1, len(towns)),
        #     'data_labels': {'value': True, 'num_format': u'#0 "km/h"'}
        # })
        # bar_chart.add_series({
        #     'name': 'Min Speed',
        #     'values': '=Chart Data!${0}${1}:${0}${2}'
        #     .format(chr(ord('A') + cell_index + 2), 1, len(towns)),
        #     'categories': '=Chart Data!${0}${1}:${0}${2}'
        #     .format(chr(ord('A') + cell_index), 1, len(towns)),
        #     'data_labels': {'value': True, 'num_format': u'#0 "km/h"'}
        # })
        # # adding other options
        # bar_chart.set_title({'name': ugettext("Maximum and minimum wind speeds")})

        # worksheet_c.insert_chart('B20', bar_chart, {'x_scale': 1, 'y_scale': 1})

        # # Creating the pie chart
        # pie_chart = workbook.add_chart({'type': 'pie'})

        # # creating data for pie chart
        # pie_values = []
        # pie_values.append(Weather.objects.filter(max_temperature__gt=20).count())
        # pie_values.append(Weather.objects.filter(max_temperature__lte=20,
        #                                          max_temperature__gte=10).count())
        # pie_values.append(Weather.objects.filter(max_temperature__lt=10).count())
        # pie_categories = ["T >18", "10 < T < 18", "T < 10"]

        # # adding the data to "Chart Data" Sheet
        # cell_index = cell_index + 4
        # worksheet_d.write_column("{0}1".format(chr(ord('A') + cell_index)),
        #                          pie_values)
        # worksheet_d.write_column("{0}1".format(chr(ord('A') + cell_index + 1)),
        #                          pie_categories)

        # # adding the data to the chart
        # pie_chart.add_series({
        #     'name': ugettext('Temperature statistics'),
        #     'values': '=Chart Data!${0}${1}:${0}${2}'
        #     .format(chr(ord('A') + cell_index), 1, 3),
        #     'categories': '=Chart Data!${0}${1}:${0}${2}'
        #     .format(chr(ord('A') + cell_index + 1), 1, 3),
        #     'data_labels': {'percentage': True}
        # })

        # # insert the chart on "Charts" Sheet
        # worksheet_c.insert_chart('J20', pie_chart)
    else:
# write header
        worksheet_s.write(3, 0, ugettext("Sample Name"), header) # project-ID+counter
        worksheet_s.write(3, 1, ugettext("Experimental Condition"), header) # from dropdown from parsed conditions Experimental_conditions
        worksheet_s.write(3, 2, ugettext("Isotopic label *"), header) # from dropdown from parsed conditions Isotopic_label
        worksheet_s.write(3, 3, ugettext("Replicate"), header) # pre filled 123 123 if total/3 = 0 else,jjjjj
        worksheet_s.write(3, 4, ugettext("Sample type delivered"), header) #add Sample type value and leave free for editing
        worksheet_s.write(3, 5, ugettext("Buffer composition"), header) #add Buffer composition value and leave free for editing (space dows not matter)
        worksheet_s.write(3, 6, ugettext("Sample amount"), header) #format digits (2 decimals) leave for edit
        worksheet_s.write(3, 7, ugettext("Unit (μg of protein / # of cells **)"), header) #format digits (2 decimals) leave for edit
        worksheet_s.write(3, 8, ugettext("Volume (if applicable) (μl)"), header) #  #format digits (2 decimals) leave for edit
        worksheet_s.write(3, 9, ugettext("Other relevant information"), header) # leave free

        #print(arguments_dict.keys())

        # # column widths
        # town_col_width = 10
        # description_col_width = 10
        # observations_col_width = 25
     #    dict_keys(['csrfmiddlewaretoken', 'contact_wizard_sg-current_step', '2-Species', '2-Sequence_Database_Public_Availability',
     # '2-Sequence_database_name', '2-Sequence_database_file', '2-Sample_Type', '2-Buffer_composition', 
     # '3-Experimental_conditions', '3-Conditions_to_compare', '3-Nb_replicates_per_condition', 
     # '3-Nb_samples', '3-Isotopic_labeling', '3-Isotopic_labeling_details', 'PID'])

        # generate values to prepopulate table
        #idx = 1
        # experimental conditions
        ec = arguments_dict["3-Experimental_conditions"][0].replace(' ','').split(',')
        print(ec)
        no_ec = len(ec)
        no_samples = int(arguments_dict["3-Nb_samples"][0].replace(' ',''))
        print('nosa'+str(no_samples))
        #parsimonious list for replicates
        no_replicates = arguments_dict["3-Nb_replicates_per_condition"][0].replace(' ','').split(',')
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
            # index defining which sample from each condition ec[i] will be chosen
            for i in range(len(ec)):
                if len(samples_dict[ectemp[i]])>0:
                    try:
                        samplelistindexestemp = random.sample(range(nbsamplesperectemp[ectempindexes[i]]),1)
                        sampletemp = samples_dict[ectemp[i]].pop(samplelistindexestemp[0]).split("_")
                        eclist.append(sampletemp[0])
                        replicatelist.append(sampletemp[1])
                    except IndexError:
                        replicatelist.append("")

                    # samplelistindexestemp = random.sample(range(nbsamplesperectemp[ectempindexes[i]]),1)
                    # sampletemp = samples_dict[ectemp[i]].pop(samplelistindexestemp[0]).split("_")
                    # eclist.append(sampletemp[0])
                    # replicatelist.append(sampletemp[1])
        no_samplesleft = no_samples-len(eclist)
        eclist = eclist + ['']*no_samplesleft
        replicatelist = replicatelist + ['']*no_samplesleft
        # NEW
        saunit = ['μg of protein','# of cells']
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
            worksheet_s.write_string(row, 2, "label", celledit) # make remark at the end
            ## replicate
            #worksheet_s.write_string(row, 3, str(plist[idx]), celledit)
            # replicate
            if str(replicatelist[idx])!="":
                worksheet_s.write_string(row, 3, str(replicatelist[idx]), celledit)
            else:
                worksheet_s.write_string(row, 3, "", celledit)
            # sample type delivered
            worksheet_s.write_string(row, 4, arguments_dict['2-Sample_Type'][0], celledit)
            # buffer composition
            worksheet_s.write_string(row, 5, arguments_dict['2-Buffer_composition'][0], celledit)

            # protein 
            worksheet_s.write_number(row, 6, 0.00, celledit)
            worksheet_s.data_validation(row, 6,row, 6, {'validate':'decimal',
                                                  'criteria': '>',
                                                  'value':'0.00'})
            # sample amount unit
            worksheet_s.write_string(row, 7, "", celledit)
            worksheet_s.data_validation(row, 7,row, 7, {'validate':'list',
                                                  'source': saunit})
            # volume
            worksheet_s.write_number(row, 8, 0.00, celledit)

            worksheet_s.data_validation(row, 8, row, 8, {'validate':'decimal',
                                                  'criteria': '>',
                                                  'value':'0.00'})
            # Other relevant information
            worksheet_s.write_string(row, 9, '', celledit)

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
        span = 'B'+str(idx)+':E'+str(idx)
        span2 = 'B'+str(idx+1)+':E'+str(idx+1)
        span3 = 'B'+str(idx+2)+':E'+str(idx+2)
        worksheet_s.merge_range(span,"- please edit and review the fields in orange", cellneditleft)
        worksheet_s.merge_range(span2,"- * if you are unsure about the labeling schema to use please leave this column empty", cellneditleft)
        worksheet_s.merge_range(span3,"- ** according to if the sample is protein extract or cell pellet, respectively", cellneditleft)

        # change column widths
        worksheet_s.set_column('A:A', 14.3)  # Sample Name
        worksheet_s.set_column('B:B', 20.8)  # Experimental Condition
        worksheet_s.set_column('C:C', 15.0)  # Isotopic label
        worksheet_s.set_column('D:D', 9.5)  # Replicate
        worksheet_s.set_column('E:E', 22.0)  # Sample type delivered
        worksheet_s.set_column('F:F', 16.0)  # Buffer composition
        worksheet_s.set_column('G:G', 18.0)  # Protein mass
        worksheet_s.set_column('H:H', 28.0)  # Protein mass unit
        worksheet_s.set_column('I:I', 23.0)  # Volume
        worksheet_s.set_column('J:J', 28.0)  # Other relevant info
   
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
