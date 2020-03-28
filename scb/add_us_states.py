import re
import datetime
import requests
import shutil

def get_csv():
	yday = datetime.datetime.now()-datetime.timedelta(days=1)
	url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/%s.csv' % (yday.strftime("%m-%d-%Y"))
	session = requests.session()
	try:
		r = session.get(url,timeout=20)
		f = open('cvdaily.csv','w')
		print(len(r.text))
		f.write(r.text)
		f.close()
		lines = [l for l in open('cvdaily.csv') if len(l) > 10]
		f = open('cvdaily.csv','w')
		f.write(''.join(lines))
		f.close()
	except requests.exceptions.RequestException as e:
		print(e)

def rename_files():
	yday = datetime.datetime.now()-datetime.timedelta(days=1)
	dest = 'archive/covid-19_confirmed_us_base_%s.csv' % (yday.strftime("%m-%d-%Y"))
	shutil.move('covid-19_confirmed_us_base.csv',dest)
	dest = 'archive/covid-19_deaths_us_base_%s.csv' % (yday.strftime("%m-%d-%Y"))
	shutil.move('covid-19_deaths_us_base.csv',dest)
	shutil.move('covid-19_confirmed_us.csv','covid-19_confirmed_us_base.csv')
	shutil.move('covid-19_deaths_us.csv','covid-19_deaths_us_base.csv')

get_csv()
rename_files()
lines = [l.rstrip() for l in open('cvdaily.csv','r')]
deaths = {}
confirmed = {}
lines = lines[1:]
for l in lines:
	vs = l.split(',')
	if len(vs) < 4:
		continue
	if vs[3] == 'US':
		if vs[2] in confirmed:
			confirmed[vs[2]] += int(vs[7])
		else:
			confirmed[vs[2]] = int(vs[7])
		if vs[2] in deaths:
			deaths[vs[2]] += int(vs[8])
		else:
			deaths[vs[2]] = int(vs[8])
lines = [l.rstrip() for l in open('covid-19_confirmed_us_base.csv','r')]
titles = lines[0]
ts = titles.split(',')
lines = lines[1:]
xs = [datetime.datetime.strptime(d,"%m/%d/%y").date() for d in ts[4:]]
nday = (xs[-1]+datetime.timedelta(days=1)).strftime("%m/%d/%y")
titles += ',%s' % (nday)
out = open('covid-19_confirmed_us.csv','w')
out.write('%s\n' % (titles))
for l in lines:
	vs = l.split(',')
	if len(vs) < 4:
		continue
	if vs[0] in confirmed:
		l += ',%i' % (int(confirmed[vs[0]]))
	out.write('%s\n' % (l))
out.close()

lines = [l.rstrip() for l in open('covid-19_deaths_us_base.csv','r')]
titles = lines[0]
ts = titles.split(',')
lines = lines[1:]
xs = [datetime.datetime.strptime(d,"%m/%d/%y").date() for d in ts[4:]]
nday = (xs[-1]+datetime.timedelta(days=1)).strftime("%m/%d/%y")
titles += ',%s' % (nday)
out = open('covid-19_deaths_us.csv','w')
out.write('%s\n' % (titles))
for l in lines:
	vs = l.split(',')
	if len(vs) < 4:
		continue
	if vs[0] in confirmed:
		l += ',%i' % (int(deaths[vs[0]]))
	out.write('%s\n' % (l))
out.close()

