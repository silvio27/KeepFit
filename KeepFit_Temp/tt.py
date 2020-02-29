import csv

with open('FitnessRecord.data', 'r') as file:
    a = []
    f_csv = csv.reader(file)
    next(f_csv)
    for i in f_csv:
        a.append(i)

with open('Tempdata.data','a') as file:
    file.write(str(a))