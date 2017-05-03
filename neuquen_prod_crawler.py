from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import re
import csv

csvfile=open('neuquen_prod.csv', 'w')
writer = csv.writer(csvfile, delimiter=',')
writer.writerow('well' + "," + 'date' + "," + 'data' + "," + 'fluid')

driver = webdriver.Chrome()
url= "https://www.se.gob.ar/datosupstream/graf_prod_x_pozo.php?gas=1&ejecutar=1&vienede=&idpozo="
#driver.maximize_window()
driver.implicitly_wait(20) # seconds
driver.get(url)

# ------ SET THE YEAR ------
year_select = Select(driver.find_element_by_xpath("//select[@name='anio']"))
for selected_year in ['2016','2015','2014','2013','2012','2011','2010']:
    year_select.select_by_value(selected_year)

    time.sleep(3) #make sure the web is loaded

    # ------ SET THE PROVINCE ------
    province_select = Select(driver.find_element_by_xpath("//select[@name='provincia']"))
    province_select.select_by_visible_text('NEUQUéN')
    #province_list =[o.text for o in province_select.options]
    time.sleep(5) #make sure the web is loaded

    # ------ SET THE BLOCK ------
    block_select = Select(driver.find_element_by_xpath("//select[@name='yacimiento']"))
    block_select.select_by_visible_text('LOMA CAMPANA - LOMA CAMPANA-LLL')
    #block_list =[o.text for o in block_select.options]
    time.sleep(5) #make sure the web is loaded

    # ------ GET THE WELL LIST ------
    well_select = Select(driver.find_element_by_xpath("//select[@name='pozo']"))
    #print ([o.text for o in well_select.options] ) #Prints "Option", followed by "Not Option"
    well_list =[o.text for o in well_select.options]
    well_list.pop(0) #remove first element which is not well name

    # ------ SELECT THE WELL ------
    for well in well_list:

        well_select.select_by_visible_text(well) #'YPF.NQ.LLL-1305(H)'
        # ------ CLICK THE FLUID BUTTON ------
        for fluid_iter in [2,1,3]:

            if fluid_iter != 2:
                driver.find_element_by_xpath("//html/body/div[2]/form/div[5]/input[" + str(fluid_iter) + "]").click()  # this worked

            #time.sleep(5) #make sure the web is loaded

            # ------ GET THE DATA ------
            html = driver.page_source
            soup = BeautifulSoup(html,"html.parser")
            #print (soup.prettify())
            param_found = soup.find_all("param")
            if len(param_found)>1:
                data_str=param_found[2].get("value")

                fluid = re.search(r"caption='(\w+)'",data_str).group(1)
                wellname = re.search(r"subcaption='Pozo\s(.+)'.xAxis.+Año.(\d+)",data_str).group(1)
                year = re.search(r"subcaption='Pozo\s(.+)'.xAxis.+Año.(\d+)",data_str).group(2)

                re_label = re.compile(r"label='\w+'")
                re_value = re.compile(r"value='\w+.\w+'")


                label=re_label.findall(data_str)
                value=re_value.findall(data_str)
                for i in range(0,len(label)):
                    label[i]=re.sub(r"label='(\w+)'", r"\1", label[i])
                    value[i] = re.sub(r"value='(\w+.\w+)'", r"\1", value[i])
                    print (wellname + ",01-" + label[i] + "-" + year + ","+  value[i] + "," + fluid)
                    writer.writerow(wellname + ",01-" + label[i] + "-" + year + ","+  value[i] + "," + fluid )

csvfile.close()
