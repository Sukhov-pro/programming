from selenium import webdriver                                                      #Драйвер для работы с браузером, предварительно стоит установить данные пакеты
from selenium.common.exceptions import ElementClickInterceptedException             #Продолжение работы в случае выявления ошибки "неполучается нажать"
from selenium.common.exceptions import StaleElementReferenceException               #Драйвер для работы в случае выявления ошибки проверки элемента
from selenium.webdriver.support import expected_conditions as EC                    #Проверка доступности элемента
from selenium.webdriver.support.ui import WebDriverWait                             #Элемент добавления ожидания для драйвера
from selenium.webdriver.common.by import By                                         #Поиск по сайту через различные якори HTML
from selenium.webdriver.common.keys import Keys                                     #Исполнение горячих клавиш в браузере
import time                                                                         #Элемент добавления ожидания
import pandas as pd                                                                 #Работа с таблицами и данными
import numpy as np                                                                  #Работа с данными

delay = 20                                                                          #Таймер Максимального ожидания, в случае ошибок

driver = webdriver.Chrome()                                                                 #Запускаем хром
filed = open('Средняя стоимость услуг по всем разделам.txt', 'w', encoding='utf-8')                 #Открываем файл для записи результатов
driver.get ("https://klinika.k31.ru/stoimost-uslug/")                                                       #Открываем сайт в Хроме
print("Средняя стоимость услуг по всем разделам")                                                                   #Сообщение о начале работы программы
                                                                                                                       #Далее дословный перевод
WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.CSS_SELECTOR , "[data-id='clinic']"))).click()        #Ожидай пока не появится возможность кликнуть на кнопку выбора клиники, потом нажимай

WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.CSS_SELECTOR , '[data-id="2893"]'))).click()          #Ожидай пока не появится возможность кликнуть на нужную клинику, потом нажимай
first_procedure_number = 45752                                                                                          #Это номера процедур, находящиеся в списке "Выберите направление" 
last_procedure_number = 45806
for i in range (first_procedure_number,last_procedure_number+1,1):                                                      #Запускаем цикл по открытию всех направлений 
    try:                                                                                                                        #Пробуем нажать на выбор направления
        WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.CSS_SELECTOR , "[data-id='direction']"))).click()
    except ElementClickInterceptedException:                                                                                    #Если не получается, листаем страницу вверх и снова нажимаем, единственное здесь замечание, используя цикл for для считывания таблиц
        page = driver.find_element_by_tag_name("html")                                                                          #Программа не укладывалась во время 2.30 мин. после чего вылазит баннер на сайте. В случае использования пандас, время работы значительно сокращается
        page.send_keys(Keys.HOME)                                                                                               #Так как данная программа прошла 10 и более тестов убрал данный кусок программы, по закрытию баннера.
        time.sleep(0.1)                                                                                                         #Ожиданиe перелистывания в вверх страницы
        WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH , "/html/body/div[3]/section/div/div[1]/div/div[3]/div[2]/div/span"))).click()
    
    number_procedure="[data-id='"+str(i)+"']"                                                                                        #Выявление класса направления 
    name_procedure = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.CSS_SELECTOR , number_procedure))).text       #Выявление названия направления в случае его доступности, недоступен = ожидание
    WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.CSS_SELECTOR , number_procedure))).click()                     #Ожидай пока не появится возможность кликнуть на нужное направление, потом нажимай
    
    WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH , '/html/body/div[3]/section/div/div[1]/div/div[4]/div[1]/div/table')))   #ожидаем загрузку таблицы услуг с направления

    try:
        tbl = driver.find_element_by_xpath("/html/body/div[3]/section/div/div[1]/div/div[4]/div[1]/div/table").get_attribute('outerHTML') #скачиваем данные с таблицы услуг по направлению
    except StaleElementReferenceException:
        time.sleep(5)                                                                                                                     # иначе, ждем полной загрузки и снова скачиваем данные с таблицы услуг по направлению
        tbl = driver.find_element_by_xpath("/html/body/div[3]/section/div/div[1]/div/div[4]/div[1]/div/table").get_attribute('outerHTML')

    df  = pd.read_html(tbl)                                                     #Работа с таблицей, выборка нужных данных, во
    df  = df[0].loc[:,0:1]                                                         #выборка нужных столбцов
    df  = df.rename(columns={0: "Наименование услуги", 1: "Цена"})                      #Работа с таблицей, создаем название колонок
    df["Цена"] = df["Цена"].astype(str).str[:-2].astype(np.int64)                           #переводим в Int второй столбец цен

    print('{0} : {1:.2f} руб.'.format(name_procedure, df["Цена"].mean()))                   #Сообщение пользователю о работе программы и данном этапе
    filed.write('{0} : {1:.2f} руб.'.format(name_procedure, df["Цена"].mean()))    #Запись этапа в файл
    filed.write('\n') 
driver.close()                                                                      #Закрываем наш драйвер хрома и файл
filed.close()
print ("Программа выполнена! Данные сохранены в папку местанахождения программы")   #Сообщение пользователю выполнении программы