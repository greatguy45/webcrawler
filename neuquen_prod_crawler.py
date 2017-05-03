from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
from time import gmtime, strftime, sleep
import re, csv, datetime

year_to_be_parsed = ['2016','2015','2014','2013','2012','2011','2010','2009','2008','2007','2006']
block_to_be_parsed = ['LOMA CAMPANA - LOMA CAMPANA-LLL']

writer=open('neuquen_prod.csv', 'w',encoding='utf-8')
#writer = csv.writer(csvfile, delimiter=',')
writer.writelines('well' + "," + 'date' + "," + 'data' + "," + 'fluid' + "," + 'well_id' + "\n")

driver = webdriver.Chrome()
#driver = webdriver.PhantomJS()
url= "https://www.se.gob.ar/datosupstream/graf_prod_x_pozo.php?gas=1&ejecutar=1&vienede=&idpozo="
#driver.maximize_window()
driver.implicitly_wait(20) # seconds
driver.get(url)

# ------ SET THE YEAR ------
try:
    for selected_year in year_to_be_parsed:
        year_select = Select(driver.find_element_by_xpath("//select[@name='anio']"))
        year_select.select_by_value(selected_year)

        sleep(3) #make sure the web is loaded

        # ------ SET THE PROVINCE ------
        province_select = Select(driver.find_element_by_xpath("//select[@name='provincia']"))
        province_select.select_by_visible_text('NEUQUéN')
        #province_list =[o.text for o in province_select.options]
        sleep(5) #make sure the web is loaded

        # ------ SET THE BLOCK ------
        for selected_block in block_to_be_parsed:
            block_select = Select(driver.find_element_by_xpath("//select[@name='yacimiento']"))
            block_select.select_by_visible_text(selected_block)
            #block_list =[o.text for o in block_select.options]
            sleep(5) #make sure the web is loaded

            # ------ GET THE WELL LIST ------
            well_select = Select(driver.find_element_by_xpath("//select[@name='pozo']"))
            #print ([o.text for o in well_select.options] ) #Prints "Option", followed by "Not Option"
            well_list_name =[o.text for o in well_select.options]
            well_list_value = [o.get_attribute("value") for o in well_select.options]
            well_list_name.pop(0) #remove first element which is not well name
            well_list_value.pop(0)  # remove first element which is not well name
            total_well_count = len(well_list_value)

            # ------ SELECT THE WELL ------
            well_counter = 0
            for well in well_list_value:
                well_counter = well_counter + 1
                progress_pct = round(well_counter/total_well_count*100,2)
                print("No: " + str(well_counter) + " , Well ID: " + well + " , Well Name: " + well_list_name[well_counter-1] + " , Pct progress: " + str(progress_pct) + " , current time: " + strftime("%Y-%m-%d %H:%M:%S", gmtime()))
                well_select = Select(driver.find_element_by_xpath("//select[@name='pozo']"))
                well_select.select_by_value(well)
                # ------ CLICK THE FLUID BUTTON ------
                for fluid_iter in [2,1,3]:

                    #if fluid_iter != 2:
                    driver.find_element_by_xpath("//html/body/div[2]/form/div[5]/input[" + str(fluid_iter) + "]").click()  # this worked

                    #sleep(5) #make sure the web is loaded

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
                        re_value = re.compile(r"value='\d*\.?\d*'")


                        label=re_label.findall(data_str)
                        value=re_value.findall(data_str)
                        for i in range(0,len(label)):
                            label[i]=re.sub(r"label='(\w+)'", r"\1", label[i])
                            value[i] = re.sub(r"value='(\d*\.?\d*)'", r"\1", value[i])
                            print (wellname + ",01-" + label[i] + "-" + year + ","+  value[i] + "," + fluid + "," + well + "\n")
                            writer.writelines(wellname + ",01-" + label[i] + "-" + year + ","+  value[i] + "," + fluid + "," + well + "\n")
finally:
    writer.close()
