from lxml import html
import requests
from bs4 import BeautifulSoup
import json

def main():
  response=requests.get('http://www.goal.com/en/fixtures?ICID=FX_TN_81')
  page=response.text
  soup=BeautifulSoup(page,'html.parser')
  matchlinks=[]
  location=[]
  for link in soup.find_all('a'):
    if str(link.get('href')).startswith('/en/match/'):
      matchlinks.append('http://www.goal.com'+str(link.get('href')))
  for matchpage in matchlinks:
    response=requests.get(matchpage)
    page=response.text
    soup=BeautifulSoup(page,'html.parser')
    for link in soup.find_all('li'):
      if str(link.text).startswith(u'\u2022') and str(link.text).find(',') != -1:
        location.append(str(link.text).split(',')[1][1:])
  key=0
  for weather in location:
    key+=1
    response=requests.get('http://api.openweathermap.org/data/2.5/weather?q={%s}&APPID=fb241d59a66f7872fd5a36929bd3415e'%(weather))
    if key!=7 and response.json()['clouds']['all']<20:
      print (weather+'  SUN')
    else:
      print (weather+'  clouds')
if __name__ == '__main__':
  main()