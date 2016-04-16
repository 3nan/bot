# -*- coding: utf-8 -*-
import html5lib
import pandas as pd
import urllib
import json
import numpy as np
import pycurl
import certifi


url='http://api.openweathermap.org/data/2.5/forecast?q=Tokyo,jp&units=metric'
APPID='318341b80f0bc1437aaf73e5201928ff'

chatwork_api='https://api.chatwork.com/v1/'
CHATWORKAPPID='4783740b3afe192e77a3e34e7d9bb3a8'
ROOMID='48434402'

def get_icon_on_chatwork():
    ids=np.arange(18) + 77650039
    indexs=['01d', '01n', '02d', '02n', '03d', '03n', '04d', '04n', '09d',
            '09n' ,'10d', '10n', '11d', '11n', '13d', '13n' ,'50d', '50n']
    master_list=pd.Series(ids,index=indexs)
    return master_list


def get_json_data_from_api():
    url_wp=url+'&APPID='+APPID
    socket = urllib.request.urlopen(url_wp)
    jsondata=json.loads(socket.read().decode('UTF-8'))

    city_json=jsondata['city']
    tenki_list=jsondata['list']

    rain_volumes=[row['rain']['3h']
                  if 'rain'  in row.keys() and '3h' in row['rain'] else 0
                  for row in tenki_list]
    date_list   = [[pd.to_datetime(data['dt_txt']).tz_localize('UTC').tz_convert('Asia/Tokyo').strftime('%Y-%m-%d %H:%M:00') ,
                  data['weather']] for data in tenki_list]
    weather_list = [ row['weather'] for row in tenki_list]
    df=pd.DataFrame([date_list, rain_volumes, weather_list]
                    ,index=['date' , 'rain' ,'weather'])
    return df.T



def  api (path, data=None):
    print( "Content-Type: application/json");

    # 送信データがある場合にはURLエンコードする
    if data != None:
        data = urllib.parse.urlencode(data)
        data = data.encode('utf-8')
    # APIキーをヘッダーに付与する
    headers = {"X-ChatWorkToken": CHATWORKAPPID}


    c = pycurl.Curl()
    c.setopt(pycurl.CAINFO, certifi.where())
    c.setopt(pycurl.URL, chatwork_api+path)
    c.setopt(pycurl.HTTPHEADER, ["X-ChatWorkToken:" +CHATWORKAPPID])
    c.setopt(pycurl.POST, 1)
    c.setopt(pycurl.POSTFIELDS, data)
    c.perform()

    
def weather_report():

    list = get_icon_on_chatwork()
    df=get_json_data_from_api()
    #return df
    df4=df[:4]

    strings=""
    for idx in df4.index:

        row = df4.ix[idx]
        weather= row.weather
        icon = weather[0].get('icon')
        
        strings+='[info][title]天気予報:'+row.date[0]+'[/title]'
        strings+='[preview id='+str(list[icon]) +' ht=50]'
        strings+=' 降水量：'+str(row.rain)+'mm[/info]'


    api( "rooms/"+ROOMID+"/messages",{"body":strings})



weather_report()
#pri


#print(list.values)
#print str(get_icon_on_chatwork() ).decode("string-escape")
