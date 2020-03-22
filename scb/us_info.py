import sys
import requests
import re
import json
import os
import matplotlib.pyplot as plt
import matplotlib.style
import matplotlib as mpl
import datetime
import csv

us_states = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands':'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Palau': 'PW',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY',
}

def plot_model(_plt,_max,_per,_color):
	xv = []
	yv = []
	y = 100
	for x in range(0,max):
		xv.append(x)
		yv.append(y)
		y = y * (1.0 + _per/100.0)
		if y > ymax:
			break
	_plt.plot(xv,yv,marker='x',linestyle='--',color=_color,label='+%i%% /day' % (_per))
	_plt.text(len(xv)-1+.2,yv[-1],'%i%%' % (_per),color=_color)

args = sys.argv;
path = 'covid-19_confirmed.csv'
ytitle = 'confirmed cases'
type = 'log'
output = args[3]
# specify list of countries to track
# if the 2nd command line argument is 'linear' or 'log', use that to set y-axis type
try:
	type = args[2]
except:
	type = 'log'
# select either confirmed cases or deaths for graph, from the 1st command line argument
try:
	if args[1] == 'deaths':
		path = 'covid-19_deaths.csv'
		ytitle = 'fatalities'
		args.pop(1)
	elif args[1] == 'confirmed':
		path = 'covid-19_confirmed.csv'
		ytitle = 'confirmed cases'
		args.pop(1)
except:
	path = 'covid-19_confirmed.csv'
	ytitle = 'confirmed cases'

lines = []
# read the csv file into a list of lists
with open(path) as csvfile:
	readCSV = csv.reader(csvfile, delimiter=',')
	for r in readCSV:
		if len(r) > 0:
			lines.append(r)

titles = lines[0]
lines = lines[1:]
#create an x-axis list, converting the dates in the first line into datetime objects
xs = [datetime.datetime.strptime(d,"%m/%d/%y").date() for d in titles[4:]]

state = {}
#parse lines into a dict of country totals
for l in lines:
	if l[1] != 'US':
		continue
	s = l[0]
	if s not in state:
		state[s] = [0]*len(xs)
	if s in state:
		ts = l[4:]
		for i,t in enumerate(ts):
			try:
				state[s][i] += int(t)
			except:
				pass
mpl.style.use('seaborn-notebook')
ax = plt.gca()
plt.yscale(type)
plt.ylabel('%s (%s)' % (ytitle,type))
#set titles based on the csv used
xtitle = 'days after 10th death'
if ytitle == 'confirmed cases':
	xtitle = 'days after 100th case'
plt.xlabel(xtitle)
now = datetime.datetime.now()
tm = '%s UTC' % (xs[-1].strftime("%Y-%m-%d"))
plt.title('COVID-19 %s (JHU CSSE data) %s' % (ytitle,tm))
#go through the selected country data and organize into plotted graphs
limit = 14
i = 0
max = 0
ymax = 0
for s,v in sorted(state.items(),key=lambda value: value[1][-1],reverse = True):
	min = 10
	if ytitle == 'confirmed cases':
		min = 100
	if i > limit:
		continue
	i += 1
	xv = []
	yv = []
	dyv = []
	x = 0
	ok = False
	for y in state[s]:
		if not ok and y >= min:
			ok = True
		if ok:
			xv.append(x)
			x += 1
			yv.append(y)
	if len(xv) < 2:
		continue
	if yv[-1] > ymax:
		ymax = yv[-1]
	if len(xv) > max:
		max = len(xv)
	if s in us_states:
		sl = us_states[s]
	else:
		sl = s
	plt.text(len(xv)-1+.2,yv[-1],sl)
	plt.plot(xv,yv,marker='o',label='%s' % (sl))
#show the graph

plot_model(plt,max,10,'#55ff55')
plot_model(plt,max,30,'#aaaaaa')
plot_model(plt,max,50,'#ffaaaa')


plt.grid(True, lw = 1, ls = ':', c = '.8')
fig = matplotlib.pyplot.gcf()
fig.set_size_inches(10,5)
plt.legend(loc='best')
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.legend(loc='upper left', bbox_to_anchor=(1.1, 1))
fig.savefig('D:\somecrazyblogger-org/covid19/%s' % (output), dpi=100, bbox_inches='tight')

