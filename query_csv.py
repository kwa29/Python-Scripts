import csv
import requests
import sys
import xlsxwriter

wb = xlsxwriter.Workbook(sys.argv[1].replace(".csv",".xlsx"))
ws = wb.add_worksheet("stats")    # your worksheet title here

"""
A simple program to print the result of a Prometheus query as CSV.
"""

if len(sys.argv) != 3:
    print('Usage: {0} http://prometheus:9090 a_query'.format(sys.argv[0]))
    sys.exit(1)

response = requests.get('{0}/api/v1/query'.format(sys.argv[1]),
        params={'query': sys.argv[2]})
results = response.json()['data']['result']

# Build a list of all labelnames used.
labelnames = set()
for result in results:
      labelnames.update(result['metric'].keys())

# Canonicalize
labelnames.discard('__name__')
labelnames = sorted(labelnames)

writer = csv.writer(sys.stdout)
# Write the header,
writer.writerow(['name', 'timestamp', 'value'] + labelnames)

# Write the sanples.
for result in results:
    l = [result['metric'].get('__name__', '')] + result['value']
    for label in labelnames:
        l.append(result['metric'].get(label, ''))
    writer.writerow(l)

with open(sys.argv[1],'r') as csvfile:
    table = csv.reader(csvfile)
    i = 0
    # write each row from the csv file as text into the excel file
    # this may be adjusted to use 'excel types' explicitly (see xlsxwriter doc)
    for row in table:
        ws.write_row(i, 0, row)
        i += 1
wb.close()