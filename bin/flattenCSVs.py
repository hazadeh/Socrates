
import csv
import os

counter = 0
dir = 'resources/excels'
rewrite=False
if rewrite: fout = open(dir + '\\' + 'all.csv', 'w', newline='')
if rewrite: writer = csv.writer(fout)

for filename in os.listdir(dir):
    if '.csv' not in filename or filename == 'all.csv':
        continue
    print (filename)

    with open(dir + '\\'+ filename) as csvfile:
        course_topic = None
        reader = csv.reader(csvfile)
        for row in reader:
            if row[-1] == '0': # no URL is available
                if row[0] in ['GAMES', 'DIGITAL', 'CREATIVITY', 'MEDIA, COMMUNICATIONS & NET NEUTRALITY', 'SURVEILLANCE & PRIVACY']:
                    course_topic = row[0].strip()
                else:
                    print ('\t\tERROR ', row, filename)
            else:
                counter += 1
                row[1] = row[-1]
                row = row[0:2] + [course_topic]
                if rewrite: writer.writerow(row)
print (counter)




