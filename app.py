from flask import Flask, render_template

app = Flask(__name__)

import datetime
import csv
with open('blinkdata.csv','r') as csv_file:
    lines = csv_file.readlines()

labels = []
values = []

for line in lines[1:]:
    print(line)
    data = line.split(';')
    print(data)
    labels.append(data[0])
    values.append(data[1])

for j in range(len(labels)):
    date_time_str=labels[j]
    date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
    labels[j]=date_time_obj

for m in range(len(values)):
    newstring=values[m].replace("\n",'')
    values[m]=newstring

print(labels)
print("whoa")
print(values)

colors = [
    "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
    "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
    "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]

@app.route('/')
def index():
    return render_template('graphtest.html', title='Today', max=2, labels=labels, values=values,legend="Strain Level")


@app.route('/datatesting')
def datapage():
    return render_template('bar_chart.html', title='Today', max=2, labels=labels, values=values)


@app.route('/graphtest')
def graphtest():
    return render_template('graphtest.html', title='Today', max=2, labels=labels, values=values,legend="Strain Level")

@app.route('/index')
def graphtest():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
