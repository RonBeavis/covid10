#!/bin/bash

#python3 update.py
#python3 add_us_states.py

mkdir confirmed
python3 country_info.py confirmed log confirmed/global.png
python3 country_info.py confirmed linear confirmed/global_linear.png
python3 country_info.py confirmed linear confirmed/global_delta.png delta
python3 country_info.py confirmed log confirmed/general.png
python3 country_info.py confirmed linear confirmed/global_delta.png delta
python3 country_info.py confirmed linear confirmed/general_delta.png delta
python3 country_info.py confirmed log confirmed/northern.png
python3 country_info.py confirmed linear confirmed/northern_linear.png
python3 us_info.py confirmed log confirmed/us.png
python3 us_info.py confirmed linear us_confirmed/linear.png
python3 ca_info.py confirmed log confirmed/confirmed/ca.png
python3 ca_info.py confirmed linear ca_linear.png
python3 asian_info.py confirmed log confirmed/asia.png
python3 asian_info.py confirmed linear confirmed/asia_linear.png
python3 country_info.py confirmed log confirmed/atin.png
python3 country_info.py confirmed linear confirmed/latin_linear.png
python3 country_info.py confirmed log confirmed/africa.png
python3 country_info.py confirmed linear confirmed/africa_linear.png
#python3 timestamp.py

mkdir deaths
python3 country_info.py deaths log deaths/global.png
python3 country_info.py deaths linear deaths/global_linear.png
python3 country_info.py deaths linear deaths/global_delta.png delta
python3 country_info.py deaths log deaths/northern.png
python3 country_info.py deaths linear deaths/northern_linear.png
python3 country_info.py deaths log deaths/general.png
python3 country_info.py deaths linear deaths/general_linear.png
python3 country_info.py deaths linear deaths/general_delta.png delta
python3 us_info.py deaths log deaths/us.png
python3 us_info.py deaths linear deaths/us_linear.png
python3 asian_info.py deaths log deaths/asia.png
python3 asian_info.py deaths linear deaths/asia_linear.png
python3 country_info.py deaths log deaths/latin.png
python3 country_info.py deaths linear deaths/latin_linear.png
python3 country_info.py deaths log deaths/africa.png
python3 country_info.py deaths linear deaths/africa_linear.png
#python3 timestamp.py
