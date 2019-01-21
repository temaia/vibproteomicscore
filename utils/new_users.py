import csv
#from django.contrib.auth import get_user_model
#User = get_user_model()
#user=User.objects.create_user(username=, email, password=password)
filename = "/home/pportal/dev2Sep18/myenv3/pportal4/static-dev/new_users.csv"
with open(filename, 'r') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        print(f'\t{row["username"]} works in the {row["email"]} department, and was born in {row["password"]}, {row["analysistype"]}.')
        line_count += 1
    print(f'Processed {line_count} lines.')
