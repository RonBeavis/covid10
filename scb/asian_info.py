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

def plot_model(_plt,_max,_per,_color,_yt):
	xv = []
	yv = []
	y = 100
	if _yt == 'fatalities':
		y = 10
	for x in range(0,max):
		xv.append(x)
		yv.append(y)
		y = y * (1.0 + _per/100.0)
		if y > ymax:
			break
	_plt.plot(xv,yv,marker='x',linestyle='--',alpha=0.8,color=_color,label='+%i%% /day' % (_per))
	_plt.text(len(xv)-1+.2,yv[-1],'%i%%' % (_per),color=_color)

args = sys.argv;
path = 'covid-19_confirmed.csv'
ytitle = 'confirmed cases'
type = 'log'
output = args[3]
# specify list of countries to track
clist = ['Indonesia','Thailand','Philippines','Taiwan*','China','Japan','Korea, South','Singapore','India','Pakistan','Iran','Malaysia']
clabels = {'Korea, South':'S. Korea','Taiwan*':'Taiwan'}
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
if ytitle == 'confirmed cases':
	xtitle = 'days after 100th case'
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
	min = 10
	if ytitle == 'confirmed cases':
		min = 100
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

plot_model(plt,max,10,'#55ff55',ytitle)
plot_model(plt,max,20,'#aaddaa',ytitle)
plot_model(plt,max,30,'#aaaaaa',ytitle)
plot_model(plt,max,50,'#ffaaaa',ytitle)

plt.grid(True, lw = 1, ls = ':', c = '.8')
plt.legend(loc='best')
fig = matplotlib.pyplot.gcf()
fig.set_size_inches(10,5)
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.legend(loc='upper left', bbox_to_anchor=(1.1, 1))
fig.savefig('%s' % (output), dpi=100, bbox_inches='tight')

