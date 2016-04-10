# -*- coding: utf-8 -*-
import html5lib
import pandas as pd
import urllib
import json
import numpy as np

url='http://api.openweathermap.org/data/2.5/forecast?q=Tokyo,jp&units=metric'
APPID='318341b80f0bc1437aaf73e5201928ff'


def get_icon_on_chatwork():
    ids=np.arange(18) + 77650039
    indexs=['01d', '01d', '02d', '02n', '03d', '03n', '04d', '04n', '09d', '09n' ,'10d', '10n', '11d', '11n', '13d', '13n' ,'50d', '50n']
    master_list=pd.Series(ids,index=indexs)
    return master_list


def get_json_data_from_api():
    url_wp=url+'&APPID='+APPID
    socket = urllib.request.urlopen(url_wp)
    jsondata=json.loads(result)

    city_json=jsondata['city']
    tenki_list=jsondata['list']

    rain_volumes=[row['rain']['3h'] if 'rain'  in row.keys() and '3h' in row['rain'] else 0 for row in tenki_list] 

list = get_icon_on_chatwork()
print(list.values)
#print str(get_icon_on_chatwork() ).decode("string-escape")