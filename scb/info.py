import sys
import requests
import re
import json
import os
import matplotlib.pyplot as plt
import matplotlib.style
import matplotlib as mpl
import datetime

args = sys.argv;
path = 'covid-19_deaths.csv'
ytitle = 'fatalities'
if args[1] == 'deaths':
	path = 'covid-19_deaths.csv'
	ytitle = 'fatalities'
	args.pop(1)
elif args[1] == 'confirmed':
	path = 'covid-19_confirmed.csv'
	ytitle = 'confirmed cases'
	args.pop(1)
lines = [l.rstrip().split(',') for l in open(path)]
titles = lines[0]
lines = lines[1:]
xs = [datetime.datetime.strptime(d,"%m/%d/%y").date() for d in titles[4:]]
for l in lines:
	if l[0].find(args[1]) == -1 or l[1].find(args[2]) == -1:
		continue;
	ts = l[4:]
	ys = []
	for t in ts:
		ys.append(int(t))
	print(ys)
	mpl.style.use('seaborn-notebook')
	plt.yscale('log')
	ax = plt.gca()
	formatter = matplotlib.dates.DateFormatter("%m-%d")
	ax.xaxis.set_major_formatter(formatter)
	locator = matplotlib.dates.DayLocator([7,14,21,28])
	ax.xaxis.set_major_locator(locator)
	plt.ylabel(ytitle)
	plt.xlabel('date')
	if len(l[0]) > 0:
		plt.title('%s, %s (%s,%s)' % (l[0],l[1],float(l[2]),float(l[3])))
	else:
		plt.title('%s (%.3f,%.3f)' % (l[1],float(l[2]),float(l[3])))
	plt.plot(xs,ys)
	plt.show()

