import datetime
import re

lines = [l for l in open('Ω_master.html','r')]
now = datetime.datetime.now()
tm = '(%s UTC)' % (now.strftime("%Y-%m-%d %H:%M:%S"))
f = open('Ω.html','w')
for l in lines:
	o = l
	if o.find('<h3') != -1:
		o = re.sub('\(.?\)',tm,l)
		print(o,tm)
	f.write(o)
f.close()
