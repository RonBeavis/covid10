cd D:\somecrazyblogger-org\covid19
python update.py
python add_us_states.py
python country_info.py confirmed log global.png
python country_info.py confirmed linear global_linear.png
python country_info.py confirmed linear global_delta.png delta
python country_info.py confirmed log general.png
python country_info.py confirmed linear global_delta.png delta
python country_info.py confirmed linear general_delta.png delta
python country_info.py confirmed log northern.png
python country_info.py confirmed linear northern_linear.png
python us_info.py confirmed log us.png
python us_info.py confirmed linear us_linear.png
python ca_info.py confirmed log ca.png
python ca_info.py confirmed linear ca_linear.png
python asian_info.py confirmed log asia.png
python asian_info.py confirmed linear asia_linear.png
python country_info.py confirmed log latin.png
python country_info.py confirmed linear latin_linear.png
python country_info.py confirmed log africa.png
python country_info.py confirmed linear africa_linear.png
python timestamp.py

cd D:\somecrazyblogger-org\covid19d
copy ..\covid19\covid-19_confirmed.csv .\covid-19_confirmed.csv /Y
copy ..\covid19\covid-19_deaths.csv .\covid-19_deaths.csv /Y
copy ..\covid19\covid-19_confirmed_us.csv .\covid-19_confirmed_us.csv /Y
copy ..\covid19\covid-19_deaths_us.csv .\covid-19_deaths_us.csv /Y
python country_info.py deaths log global.png
python country_info.py deaths linear global_linear.png
python country_info.py deaths linear global_delta.png delta
python country_info.py deaths log northern.png
python country_info.py deaths linear northern_linear.png
python country_info.py deaths log general.png
python country_info.py deaths linear general_linear.png
python country_info.py deaths linear general_delta.png delta
python us_info.py deaths log us.png
python us_info.py deaths linear us_linear.png
python asian_info.py deaths log asia.png
python asian_info.py deaths linear asia_linear.png
python country_info.py deaths log latin.png
python country_info.py deaths linear latin_linear.png
python country_info.py deaths log africa.png
python country_info.py deaths linear africa_linear.png
python timestamp.py
