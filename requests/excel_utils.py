#!/usr/bin/python
# -*- coding: utf-8 -*-
import io
import xlsxwriter
from django.utils.translation import ugettext
from django.db.models import Avg, Sum, Max, Min

#from .models import Town, Weather


def WriteToExcel(arguments_dict):
    #output = io.BytesIO()
    output = "media/ED/Experimental_design_"+arguments_dict["PID"]+".xlsx"
    workbook = xlsxwriter.Workbook(output)
    worksheet_s = workbook.add_worksheet("main")
    # add more Sheets
    #worksheet_b = workbook.add_worksheet("opts sheet")
    
    # excel styles
    title = workbook.add_format({
        'bold': True,
        'font_size': 14,
        'align': 'center',
        'valign': 'vcenter'
    })
    header = workbook.add_format({
        'bg_color': '#F7F7F7',
        'color': 'black',
        'align': 'center',
        'valign': 'top',
        'border': 1
    })
    cell = workbook.add_format({
        'align': 'center',
        'valign': 'top',
        'text_wrap': True,
        'border': 1
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
    title_text = "Experimental Design"# "+arguments_dict["PID"]
    print(title_text)
    
    #title_text = u"{0} {1}".format(ugettext("Experiment_ID"), user.profile.issue)
    # merge cells
    worksheet_s.merge_range('D2:F2', title_text, title)
    print(type(arguments_dict["3-Isotopic_labeling"][0]))
    if arguments_dict["3-Isotopic_labeling"][0] == 'False':
    # write header
        worksheet_s.write(3, 0, ugettext("Sample Name"), header) # project-ID+counter
        worksheet_s.write(3, 1, ugettext("Experimental Condition"), header) # from dropdown from parsed conditions Experimental_conditions
        #worksheet_s.write(3, 2, ugettext("Isotopic label"), header) # from dropdown from parsed conditions Isotopic_label
        worksheet_s.write(3, 2, ugettext("Replicate"), header) # pre filled 123 123 if total/3 = 0 else,jjjjj
        worksheet_s.write(3, 3, ugettext("Sample type delivered"), header) #add Sample type value and leave free for editing
        worksheet_s.write(3, 4, ugettext("Buffer composition"), header) #add Buffer composition value and leave free for editing (space dows not matter)
        worksheet_s.write(3, 5, ugettext("Protein mass (or estimation of) (μg)"), header) #format digits (2 decimals) leave for edit
        worksheet_s.write(3, 6, ugettext("Volume (if applicable) (μl)"), header) #  #format digits (2 decimals) leave for edit
        #worksheet_s.write(3, 8, ugettext("Other relevant information"), header) # leave free

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
        #parsimonious list for replicates
        no_replicates = int(arguments_dict["3-Nb_replicates_per_condition"][0].replace(' ',''))
        no_samples = int(arguments_dict["3-Nb_samples"][0].replace(' ',''))
        print('nosa'+str(no_samples))
        # predicted no_ec
        pno_ec = no_samples//no_replicates + no_samples%no_replicates
        plist = list(range(1,no_replicates+1,1))*pno_ec
        eclist = []
        for ec0 in ec:
            for rep in range(1,no_replicates+1,1):
                eclist.append(ec0)
        for rep in range(1,no_replicates+1,1):
            eclist.append('')
        # buffer
        print(eclist)
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
            worksheet_s.write_string(row, 3, arguments_dict['2-Sample_Type'][0], celledit)
            # buffer composition
            worksheet_s.write_string(row, 4, arguments_dict['2-Buffer_composition'][0], celledit)

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
            #worksheet_s.write_string(row, 8, '', celledit)

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

        # change column widths
        worksheet_s.set_column('A:A', 14.3)  # Sample Name
        worksheet_s.set_column('B:B', 20.8)  # Experimental Condition
        #worksheet_s.set_column('C:C', 12.6)  # Isotopic label
        worksheet_s.set_column('C:C', 9.5)  # Replicate
        worksheet_s.set_column('D:D', 30.0)  # Sample type delivered
        worksheet_s.set_column('E:E', 16.0)  # Buffer composition
        worksheet_s.set_column('F:F', 30.0)  # Protein mass
        worksheet_s.set_column('G:G', 25.0)  # Volume
        #worksheet_s.set_column('I:I', 25.0)  # Other relevant info
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
        worksheet_s.write(3, 2, ugettext("Isotopic label"), header) # from dropdown from parsed conditions Isotopic_label
        worksheet_s.write(3, 3, ugettext("Replicate"), header) # pre filled 123 123 if total/3 = 0 else,jjjjj
        worksheet_s.write(3, 4, ugettext("Sample type delivered"), header) #add Sample type value and leave free for editing
        worksheet_s.write(3, 5, ugettext("Buffer composition"), header) #add Buffer composition value and leave free for editing (space dows not matter)
        worksheet_s.write(3, 6, ugettext("Protein mass (or estimation of) (μg)"), header) #format digits (2 decimals) leave for edit
        worksheet_s.write(3, 7, ugettext("Volume (if applicable) (μl)"), header) #  #format digits (2 decimals) leave for edit
        #worksheet_s.write(3, 8, ugettext("Other relevant information"), header) # leave free

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
        #parsimonious list for replicates
        no_replicates = int(arguments_dict["3-Nb_replicates_per_condition"][0].replace(' ',''))
        no_samples = int(arguments_dict["3-Nb_samples"][0].replace(' ',''))
        print('nosa'+str(no_samples))
        # predicted no_ec
        pno_ec = no_samples//no_replicates + no_samples%no_replicates
        plist = list(range(1,no_replicates+1,1))*pno_ec
        eclist = []
        for ec0 in ec:
            for rep in range(1,no_replicates+1,1):
                eclist.append(ec0)
        for rep in range(1,no_replicates+1,1):
            eclist.append('')
        # buffer
        print(eclist)
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
            worksheet_s.write_string(row, 2, "labels", celledit) # make remark at the end
            # replicate
            worksheet_s.write_string(row, 3, "rep_" + str(plist[idx]), celledit)
            # sample type delivered
            worksheet_s.write_string(row, 4, arguments_dict['2-Sample_Type'][0], celledit)
            # buffer composition
            worksheet_s.write_string(row, 5, arguments_dict['2-Buffer_composition'][0], celledit)

            # protein 
            worksheet_s.write_number(row, 6, 0.00, celledit)
            worksheet_s.data_validation(row, 6,row, 6, {'validate':'decimal',
                                                  'criteria': '>',
                                                  'value':'0.00'})
            # volume
            worksheet_s.write_number(row, 7, 0.00, celledit)

            worksheet_s.data_validation(row, 7, row, 7, {'validate':'decimal',
                                                  'criteria': '>',
                                                  'value':'0.00'})
            # Other relevant information
            #worksheet_s.write_string(row, 8, '', celledit)

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

        # change column widths
        worksheet_s.set_column('A:A', 14.3)  # Sample Name
        worksheet_s.set_column('B:B', 20.8)  # Experimental Condition
        worksheet_s.set_column('C:C', 12.6)  # Isotopic label
        worksheet_s.set_column('D:D', 9.5)  # Replicate
        worksheet_s.set_column('E:E', 30.0)  # Sample type delivered
        worksheet_s.set_column('F:F', 16.0)  # Buffer composition
        worksheet_s.set_column('G:G', 30.0)  # Protein mass
        worksheet_s.set_column('H:H', 25.0)  # Volume
    
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
