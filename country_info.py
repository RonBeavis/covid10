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

args = sys.argv;
path = 'covid-19_confirmed.csv'
ytitle = 'confirmed cases'
clist = ['US','Korea, South','Canada','Italy','Spain','France','UK','Singapore','Japan','United Kingdom','Iran']
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
with open(path) as csvfile:
	readCSV = csv.reader(csvfile, delimiter=',')
	for r in readCSV:
		if len(r) > 0:
			lines.append(r)

titles = lines[0]
lines = lines[1:]
xs = [datetime.datetime.strptime(d,"%m/%d/%y").date() for d in titles[4:]]
country = {}
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
#	plt.yscale('log')
mpl.style.use('seaborn-notebook')
ax = plt.gca()
plt.yscale('log')
plt.ylabel(ytitle)
xtitle = 'days after 10th death'
if ytitle == 'confirmed cases':
	xtitle = 'days after 100th case'
plt.xlabel(xtitle)
plt.title('COVID-19 %s (Johns Hopkins CSSE data)' % (ytitle))
ax.legend(loc='upper left', bbox_to_anchor=(1, 1))

for c in country:
	if c not in clist:
		continue
	min = 10
	if ytitle == 'confirmed cases':
		min = 100
	xv = []
	yv = []
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
	plt.text(len(xv)-1+.2,yv[-1],c)
	plt.plot(xv,yv,marker='o',label='%s' % (c))
plt.legend(loc='best')
plt.grid(True, lw = 1, ls = '--', c = '.8')

plt.show()

