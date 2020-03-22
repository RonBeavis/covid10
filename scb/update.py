import requests

url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv'
session = requests.session()
try:
	r = session.get(url,timeout=20)
	f = open('covid-19_confirmed.csv','w')
	print(len(r.text))
	f.write(r.text)
	f.close()
	lines = [l for l in open('covid-19_confirmed.csv') if len(l) > 10]
	f = open('covid-19_confirmed.csv','w')
	f.write(''.join(lines))
	f.close()
except requests.exceptions.RequestException as e:
	print(e)


url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv'
session = requests.session()
try:
	r = session.get(url,timeout=20)
	f = open('covid-19_deaths.csv','w')
	print(len(r.text))
	f.write(r.text)
	f.close()
	lines = [l for l in open('covid-19_deaths.csv') if len(l) > 10]
	f = open('covid-19_deaths.csv','w')
	f.write(''.join(lines))
	f.close()
except requests.exceptions.RequestException as e:
	print(e)


