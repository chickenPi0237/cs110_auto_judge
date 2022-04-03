import csv

time_stamp = []
name = []
id = []
url = []

csv_path = '.\\cs101_lab0.csv'

with open(csv_path, newline='', encoding='utf-8') as csv_file:
    table = csv.reader(csv_file, delimiter=',')
    header = next(table)
    for row in table:
        time_stamp.append(row[0])
        name.append(row[1])
        id.append(row[2])
        url.append(row[3])
        
