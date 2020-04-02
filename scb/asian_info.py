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
delta = params['delta']
type = params['type']
output = params['output']
# specify list of countries to track
clist = ['Indonesia','Thailand','Philippines','Taiwan*','China','Japan','Korea, South','Singapore','India','Pakistan','Iran','Malaysia']
clabels = {'Korea, South':'S. Korea','Taiwan*':'Taiwan'}

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
for l in lines:
	c = l[1]
	if c == 'China' and l[0] != 'Hong Kong':
		continue
	if c not in country:
		country[c] = [0]*len(xs)
	if c in country:
		ts = l[4:]
		for i,t in enumerate(ts):
			try:
				country[c][i] += int(t)
			except:
				pass
mpl.style.use('seaborn-notebook')
ax = plt.gca()
plt.yscale(type)
plt.ylabel('%s (%s)' % (ytitle,type))
#set titles based on the csv used
xtitle = 'days after 10th death'
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
	if c == 'China':
		px = [xv[-1],xv[-1]+1]
		dy = 1.0 + float(yv[-1]-yv[-2])/float(yv[-1])
		py = [yv[-1],yv[-1]*dy]
		plt.plot(xv,yv,marker='o',label='%s' % ('Hong Kong'))
		plt.text(px[-1]+.2,py[-1],'Hong Kong')
		plt.plot(px,py,marker='x',linestyle=':',alpha=1,color='#999999')


#		plt.text(len(xv)-1+.2,yv[-1],'Hong Kong')
#		plt.plot(xv,yv,marker='o',label='%s' % ('Hong Kong'))
	else:
		px = [xv[-1],xv[-1]+1]
		dy = 1.0 + float(yv[-1]-yv[-2])/float(yv[-1])
		py = [yv[-1],yv[-1]*dy]
		plt.plot(xv,yv,marker='o',label='%s' % (cl))
		plt.text(px[-1]+.2,py[-1],cl)
		plt.plot(px,py,marker='x',linestyle=':',alpha=1,color='#999999')
	
#show the graph

if not delta:
	plot_model(plt,max,10,'#55ff55')
	plot_model(plt,max,20,'#aaddaa')
	plot_model(plt,max,30,'#aaaaaa')
	plot_model(plt,max,50,'#ffaaaa')

plt.grid(True, lw = 1, ls = ':', c = '.8')
plt.legend(loc='best')
fig = matplotlib.pyplot.gcf()
fig.set_size_inches(10,5)
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.legend(loc='upper left', bbox_to_anchor=(1.1, 1))
fig.savefig('%s' % (output), dpi=100, bbox_inches='tight')

