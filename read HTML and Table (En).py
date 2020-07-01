from selenium import webdriver                                                      #Driver to work with browser
from selenium.common.exceptions import ElementClickInterceptedException             #If you get error that you can't click on smth
from selenium.common.exceptions import StaleElementReferenceException               #If you get element check on page error
from selenium.webdriver.support import expected_conditions as EC                    #This for check enable of different elements on web page
from selenium.webdriver.support.ui import WebDriverWait                             #Help to insert time waiting in webdriver if smth loading 
from selenium.webdriver.common.by import By                                         #Search different tags from page
from selenium.webdriver.common.keys import Keys                                     #This import allow use keybord in browser
import time                                                                         #Help to insert time waiting in project if smt loading
import pandas as pd                                                                 #Work with tables and data 
import numpy as np                                                                  #Work with data

delay = 20                                                                          #Max timer if smth go wrong

driver = webdriver.Chrome()                                                                 #Start Chrome
filed = open('Средняя стоимость услуг по всем разделам.txt', 'w', encoding='utf-8')                 #Open file to write information from site
driver.get ("https://klinika.k31.ru/stoimost-uslug/")                                                       #Open website in diver
print("Средняя стоимость услуг по всем разделам")                                                                   #Message:program started
                                                                                                                       #Here I try to write only process
WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.CSS_SELECTOR , "[data-id='clinic']"))).click()        #Wait while button clinic will be allow, after driver do click

WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.CSS_SELECTOR , '[data-id="2893"]'))).click()          #Wait while button needest button clinic will be allow, after driver do click
first_procedure_number = 45752                                                                                          #Number of procedure in list "Выберите направление" 
last_procedure_number = 45806
for i in range (first_procedure_number,last_procedure_number+1,1):                                                      #Cycle to read all tables from list "направления" 
    try:                                                                                                                        #Try to click
        WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.CSS_SELECTOR , "[data-id='direction']"))).click()
    except ElementClickInterceptedException:                                                                                    #If program cannot click I use a home button to get to the top, this strange method,but this works
        page = driver.find_element_by_tag_name("html")                                                                          #First time I use "FOR" insted pandas and I tryed to read all lines. Pandas make this process faster. And I end this work before banner start(after 2.30 min)
        page.send_keys(Keys.HOME)                                                                                               #Program tested more then 10 times and I delete this block about close banner
        time.sleep(0.1)                                                                                                         #Waiting to go up
        WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH , "/html/body/div[3]/section/div/div[1]/div/div[3]/div[2]/div/span"))).click()
    
    number_procedure="[data-id='"+str(i)+"']"                                                                                        #Class of component
    name_procedure = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.CSS_SELECTOR , number_procedure))).text       #Try to get name of procedure, if don't get it = wait
    WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.CSS_SELECTOR , number_procedure))).click()                     #Wait while you can't push click
    
    WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH , '/html/body/div[3]/section/div/div[1]/div/div[4]/div[1]/div/table')))   #Wait while table load

    try:
        tbl = driver.find_element_by_xpath("/html/body/div[3]/section/div/div[1]/div/div[4]/div[1]/div/table").get_attribute('outerHTML') #Download  table
    except StaleElementReferenceException:
        time.sleep(5)                                                                                                                     # Except wait and try again
        tbl = driver.find_element_by_xpath("/html/body/div[3]/section/div/div[1]/div/div[4]/div[1]/div/table").get_attribute('outerHTML')

    df  = pd.read_html(tbl)                                                     #Work with table
    df  = df[0].loc[:,0:1]                                                         #Try to get needest columns
    df  = df.rename(columns={0: "Наименование услуги", 1: "Цена"})                      #Write name for this columns
    df["Цена"] = df["Цена"].astype(str).str[:-2].astype(np.int64)                           #Get second column in int

    print('{0} : {1:.2f} руб.'.format(name_procedure, df["Цена"].mean()))                   #Message to user about current process
    filed.write('{0} : {1:.2f} руб.'.format(name_procedure, df["Цена"].mean()))    #Write process in file
    filed.write('\n') 
driver.close()                                                                      #Close web browser and file manager
filed.close()
print ("Программа выполнена! Данные сохранены в папку местанахождения программы")   #Message to user: "Work done"