from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random
import json
from zhdate import ZhDate as lunar_date


today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
bn_birthday = os.environ['bn_birthday']
zj_birthday = os.environ['zj_birthday']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

bn_user_id = os.environ["BN_USER_ID"]
zj_user_id = os.environ["ZJ_USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  url = "http://t.weather.sojson.com/api/weather/city/101130101"
  res = requests.get(url).json()
  return res["data"]["forecast"][0]["type"], res["data"]["forecast"][0]["high"]+res["data"]["forecast"][0]["low"]

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday(birthday):
  all_birthday= str(date.today().year)+','+birthday
  lunar_birthday = lunar_date(int(all_birthday.split(',',3)[0]),int(all_birthday.split(',',3)[1]),int(all_birthday.split(',',3)[2]))
  print(lunar_birthday.to_datetime())
  next = datetime.strptime(str(lunar_birthday.to_datetime()),"%Y-%m-%d %H:%M:%S")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)
wm = WeChatMessage(client)
wea, temperature = get_weather()
data = {"city":{"value":city},"weather":{"value":wea},"temperature":{"value":temperature},"love_days":{"value":get_count()},"bn_birthday":{"value":get_birthday(bn_birthday)},"zj_birthday":{"value":get_birthday(zj_birthday)},"words":{"value":get_words(), "color":get_random_color()}}
res = wm.send_template(bn_user_id, template_id, data)
res = wm.send_template(zj_user_id, template_id, data)
print(res)
