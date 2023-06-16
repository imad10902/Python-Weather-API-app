import datetime as dt
import requests
import sys
import csv

BASE_URL = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/forecast?unitGroup=metric'
ACCESS_KEY = open('key.txt', 'r').read()

#The location in this free API is according to timezone. So, only time zone locations work. 
#For example type: "Asia/Kolkata", "Asia/Tehran", "America/New_York"
CITY= input('Enter city name with continent: ')
filename= "forecast_" + CITY.replace('/', '') + ".txt"
url= BASE_URL + "&timezone=" + CITY + "&include=days%2Ccurrent" + "&key=" + ACCESS_KEY + '&contentType=json'


response = requests.get(url)
if response.status_code!=200:
  if(response.status_code == 400):
    print("Type correct city name in correct format" )
  else:
    print("Request could not fetch result and retuned with error code: ", response.status_code)
  sys.exit()  
#Error handling above


result= response.json()
#Printing the output in terminal
for day in result['days'][:9]:
  print('Date:', day['datetime'], end="   ")
  print('Temperature in celsius:', day['temp'], end="  ")
  print("Humidity:", day['humidity'])
  



#Creating file with tabular data
headers = list(result['days'][0].keys())
column_widths = [max(len(header), max(len(str(row.get(header, ""))) for row in result['days'])) for header in headers]
formatted_headers = [header.center(width) for header, width in zip(headers, column_widths)]
formatted_data = [
    [str(row.get(header, "")).ljust(width) for header, width in zip(headers, column_widths)]
    for row in result['days']
]
table = [' '.join(row) for row in formatted_data]
table_str = '\n'.join(table)
with open(filename, 'w') as file:
    file.write(table_str)