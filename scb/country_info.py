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
	if len(yv) > 1:
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
delta = params['delta']

# specify list of countries to track
eulist = ['Sweden','Switzerland','Italy','Spain','France','United Kingdom',
		'Germany','Belgium','Austria','Poland','Netherlands','Portugal','Norway',
		'Cyprus','Croatia','Bulgaria','Ireland','Greece','Denmark','Hungary',
		'Latvia', 'Lithuania', 'Luxembourg', 'Malta','Romania', 'Slovakia', 'Slovenia']
nalist = ['US','EU','Canada','Mexico']
melist = ['Kuwait','Qatar','Saudi Arabia','Egypt','Israel','Bahrain','United Arab Emirates','Morocco','Jordan','Lebanon','Iran','Afganistan','Turkey','Syria','Iraq']
clist = ['Sweden','Switzerland','US','Korea, South','Italy','Spain','France','United Kingdom','Germany','Belgium','Austria']
if output.find('northern') == 0:
	clist = ['Sweden','Denmark','Canada','Norway','Russia','Finland','Netherlands','Australia','Iceland','New Zealand']
elif output.find('latin') == 0:
	clist = ['Mexico','Brazil','Chile','Argentina','Columbia','Peru','Bolivia','Ecuador','Cuba','Panama','Nicaragua','Uruguay','Guatemala','Belize','Jamaica']
elif output.find('africa') == 0:
	clist = ['Kuwait','Qatar','Saudi Arabia','Egypt','South Africa','Israel','Bahrain','Algeria','United Arab Emirates','Morocco','Jordan','Lebanon','Kenya','Ethiopia']
elif output.find('global') == 0:
	clist = ['Earth','EU','China','N. America','Middle East','ROE']

# if the 2nd command line argument is 'linear' or 'log', use that to set y-axis type
clabels = {'Korea, South':'S. Korea','Taiwan*':'Taiwan','Netherlands':'Holland','United Kingdom':'UK','United Arab Emirates':'UAE'}

# select either confirmed cases or deaths for graph, from the 1st command line argument

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
country = {}
#parse lines into a dict of country totals
if 'EU' in clist:
	country['EU'] = [0]*len(xs)
else:
	eulist = []
if 'N. America' in clist:
	country['N. America'] = [0]*len(xs)
else:
	nalist = []
if 'Earth' in clist:
	country['Earth'] = [0]*len(xs)
	country['ROE'] = [0]*len(xs)
if 'Middle East' in clist:
	country['Middle East'] = [0]*len(xs)
else:
	melist = []

for l in lines:
	c = l[1]
	if c not in country:
		country[c] = [0]*len(xs)
	if c in country:
		ts = l[4:]
		for i,t in enumerate(ts):
			try:
				country[c][i] += int(t)
			except:
				pass
	if 'Earth' not in clist:
		continue
	if c in eulist:
		ts = l[4:]
		for i,t in enumerate(ts):
			try:
				country['EU'][i] += int(t)
			except:
				pass
	elif c in nalist:
		ts = l[4:]
		for i,t in enumerate(ts):
			try:
				country['N. America'][i] += int(t)
			except:
				pass
	elif c in melist:
		ts = l[4:]
		for i,t in enumerate(ts):
			try:
				country['Middle East'][i] += int(t)
			except:
				pass
	elif c != 'China':
		ts = l[4:]
		for i,t in enumerate(ts):
			try:
				country['ROE'][i] += int(t)
			except:
				pass
	ts = l[4:]
	for i,t in enumerate(ts):
		try:
			country['Earth'][i] += int(t)
		except:
			pass
dtitle = ytitle
if delta:
	dtitle = 'new ' + ytitle + '/day'

mpl.style.use('seaborn-notebook')
ax = plt.gca()
plt.yscale(type)
plt.ylabel('%s (%s)' % (dtitle,type))
#set titles based on the csv used

if params['consequences'] == 'deaths':
	xtitle = 'days after %ith death' % (params['limit'])
else:
	xtitle = 'days after %ith case' % (params['limit'])

plt.xlabel(xtitle)
now = datetime.datetime.now()
tm = '%s UTC' % (xs[-1].strftime("%Y-%m-%d"))
plt.title('COVID-19 %s (JHU CSSE data) %s' % (ytitle,tm))
ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
#go through the selected country data and organize into plotted graphs
max = 0
ymax = 0
for c,v in sorted(country.items(),key=lambda value: value[1][-1],reverse = True):
	if c not in clist:
		continue
	min = params['limit']
	xv = []
	yv = []
	dyv = []
	x = 0
	ok = False
	for y in country[c]:
		if not ok and y >= min:
			ok = True
		if ok:
			xv.append(x)
			x += 1
			yv.append(y)
	if len(xv) < 2:
		continue
	if len(xv) > max:
		max = len(xv)
	if yv[-1] > ymax:
		ymax = yv[-1]
	if c in clabels:
		cl = clabels[c]
	else:
		cl = c
	px = [xv[-1],xv[-1]+1]
	dy = 1.0 + float(yv[-1]-yv[-2])/float(yv[-1])
	py = [yv[-1],yv[-1]*dy]
	if delta:
		dv = []
		for i,y in enumerate(yv):
			if i == 0:
				dv.append(0)
			else:
				dv.append(yv[i]-yv[i-1])
		av = []
		if len(dv) < 4:
			continue
		for i,y in enumerate(dv):
			if i < 2:
				av.append((dv[i]+dv[i+1]+dv[i+2])/3.0)
			else:
				av.append((dv[i]+dv[i-1]+dv[i-2])/3.0)
			
		yv = av
	if output.find('global') == 0:
		if delta:
			plt.text(xv[-1]+.2,yv[-1],cl)
			plt.plot(xv,yv,marker='.',label='%s' % (cl))
		else:
			plt.text(px[-1]+.2,py[-1],cl)
			plt.plot(xv,yv,marker='.',label='%s' % (cl))
			plt.plot(px,py,marker='x',linestyle=':',alpha=1,color='#999999')
	
	else:
		if delta:
			plt.text(xv[-1]+.2,yv[-1],cl)
			plt.plot(xv,yv,marker='o',label='%s' % (cl))
		else:
			plt.text(px[-1]+.2,py[-1],cl)
			plt.plot(xv,yv,marker='o',label='%s' % (cl))
			plt.plot(px,py,marker='x',linestyle=':',alpha=1,color='#999999')

	#show the graph
if not delta:
	plot_model(plt,max,10,'#55ff55')
	plot_model(plt,max,20,'#aaddaa')
	plot_model(plt,max,30,'#aaaaaa')
	plot_model(plt,max,50,'#ffaaaa')

plt.legend(loc='best')
plt.grid(True, lw = 1, ls = ':', c = '.8')
fig = matplotlib.pyplot.gcf()
fig.set_size_inches(10,5)
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.legend(loc='upper left', bbox_to_anchor=(1.1, 1))
fig.savefig('%s' % (output), dpi=100, bbox_inches='tight')

