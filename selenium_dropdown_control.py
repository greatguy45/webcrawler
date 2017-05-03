from selenium import webdriver
import requests
from bs4 import BeautifulSoup

page = requests.get("https://www.se.gob.ar/datosupstream/graf_prod_x_pozo.php?gas=1&ejecutar=1&vienede=&idpozo=")
soup = BeautifulSoup(page.content, 'html.parser')

#get all the year options
year=soup.find("select",{"name":"anio"})
year_options = year.find_all("option")
options1=[y.text for y in year_options]
year_values = [o.get("value") for o in year_options]

print ("list of all year available\n")
for x in range(1,len(options1)):
    print (options1[x], year_values[x])

#get all the province options
province=soup.find("select",{"name":"provincia"})
province_options = province.find_all("option")
options2=[y.text for y in province_options]
province_values = [o.get("value") for o in province_options]

print ("list of all province available\n")
for x in range(1,len(options2)):
    print (options2[x], province_values[x])

#get all the yacimiento options
yacimiento=soup.find("select",{"name":"yacimiento"})
yacimiento_options = yacimiento.find_all("option")
options3=[y.text for y in yacimiento_options]
yacimiento_values = [o.get("value") for o in yacimiento_options]

print ("list of all formation available\n")
for x in range(1,len(options3)):
    print (options3[x], yacimiento_values[x])

#get all the pozo options
pozo=soup.find("select",{"name":"pozo"})
pozo_options = pozo.find_all("option")
options4=[y.text for y in pozo_options]
pozo_values = [o.get("value") for o in pozo_options]

print ("list of all pozo available\n")
for x in range(1,len(options4)):
    print (options4[x], pozo_values[x])
