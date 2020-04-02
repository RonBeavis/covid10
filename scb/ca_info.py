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

ca_states = {
    'British Columbia': 'BC',
    'Alberta': 'AB',
    'Saskatchewan': 'SK',
    'Manitoba': 'MB',
    'Ontario': 'ON',
    'Quebec': 'QC',
    'New Brunswick': 'NB',
    'Nova Scotia': 'NS',
    'Newfoundland and Labrador': 'NL',
	'Prince Edward Island': 'PE',
	'Yukon': 'YT',
	'Nunavut': 'NU',
	'Northwest Territories': 'NT'
}

params = {'delta': False}

def plot_model(_plt,_max,_per,_color):
	xv = []
	yv = []
	y = params['limit']
	for x in range(0,max):
		xv.append(x)
		yv.append(y)
		y = y * (1.0 + _per/100.0)
		if y > ymax:
			break
	_plt.plot(xv,yv,marker='x',linestyle='--',alpha=0.8,color=_color,label='+%i%% /day' % (_per))
	_plt.text(len(xv)-1+.2,yv[-1],'%i%%' % (_per),color=_color)

#process input parameters
if len(sys.argv) < 3:
	print('usage: python country_info.py -l(min value) -o(out file) -t(linear/log) -d(delta) -c(deaths/confirmed)')
	exit()
for l in sys.argv[1:]:
	if l.find('-o') == 0:
		params['output'] = l[2:]
	elif l.find('-t') == 0:
		params['type'] = l[2:]
	elif l.find('-l') == 0:
		params['limit'] = int(l[2:])
	elif l.find('-d') == 0:
		params['delta'] = True
	elif l.find('-c') == 0:
		params['consequences'] = l[2:]
	else:
		print('Unknown parameter %s' % (l))
		exit()
print(params)

if params['consequences'] == 'deaths':
		path = 'covid-19_deaths.csv'
		ytitle = 'fatalities'
else:
		path = 'covid-19_confirmed.csv'
		ytitle = 'confirmed cases'

type = params['type']
output = params['output']

# specify list of countries to track
# if the 2nd command line argument is 'linear' or 'log', use that to set y-axis type
delta = params['delta']

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
	if l[1] != 'Canada':
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
if params['consequences'] == 'deaths':
	xtitle = 'days after %ith death' % (params['limit'])
else:
	xtitle = 'days after %ith case' % (params['limit'])
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
	min = params['limit']
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
	if s in ca_states:
		sl = ca_states[s]
	else:
		continue
	px = [xv[-1],xv[-1]+1]
	dy = 1.0 + float(yv[-1]-yv[-2])/float(yv[-1])
	py = [yv[-1],yv[-1]*dy]
	plt.plot(xv,yv,marker='o',label='%s' % (sl))
	plt.text(px[-1]+.2,py[-1],sl)
	plt.plot(px,py,marker='x',linestyle=':',alpha=1,color='#999999')
#show the graph

if not delta:
	plot_model(plt,max,10,'#55ff55')
	plot_model(plt,max,20,'#aaddaa')
	plot_model(plt,max,30,'#aaaaaa')
	plot_model(plt,max,50,'#ffaaaa')

plt.grid(True, lw = 1, ls = ':', c = '.8')
fig = matplotlib.pyplot.gcf()
fig.set_size_inches(10,5)
plt.legend(loc='best')
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.legend(loc='upper left', bbox_to_anchor=(1.1, 1))
fig.savefig('%s' % (output), dpi=100, bbox_inches='tight')

