from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
#from tqdm import notebook
import pandas as pd
import re

def string_to_time(time_str):
	""" Ф-ия преобразования полученой строки со временем в количество минут 
	"""
    hhmm = re.findall('[0-9]*[0-9]', time_str)
    if len(hhmm) > 1:
        ovr_time = int(hhmm[0])*60 + int(hhmm[1])
    else:
        ovr_time = int(hhmm[0]) #время не может быть 1 минута от станции до станции, значит там время равно 1 час => 60 минут
    return ovr_time if ovr_time > 1 else 60 


data = pd.read_csv("data/data_full.csv", sep = ";") #Данные с индексами всех станций Яндекс.Метро
data.columns = ['id','station'] 

train = pd.read_csv("data/data.csv", sep = ",", header = None)
train.columns = ['station','drink']

train = train.merge(data, on = 'station')
train = train[(train['id'] != 'st52567621')] #Оставляем только зеленую белорусскую 

options = Options()
options.add_argument("start-maximized")
driver = webdriver.Chrome(chrome_options=options, executable_path='/home/huvi2/Documents/chromedriver') #ЗАМЕНИТЬ ПУТЬ ДО ДРАЙВЕРА

times_df = []
names = []

for k, m in train.drop_duplicates().iterrows():
    from_id = m[2]
    from_station = m[0]
    names.append(from_station)
    times = []
    for i, j in data.iterrows():
        to_id = j[0]
        to_station = j[1]
        if to_id == from_id:
            times.append(0)
        else:
            url = f"https://yandex.ru/metro/moscow?route_from_id={from_id}&route_to_id={to_id}&scheme_id=sc34974011"
            driver.get(url)
            time.sleep(2.5)
            elem = driver.find_elements_by_class_name("masstransit-route-snippet-view__route-duration")
            text = elem[0].get_attribute('innerHTML')
            ovr_time = string_to_time(text)
            times.append(ovr_time)
    times_df.append(times)
    
results = pd.DataFrame(data = np.array(times_df).T, index = data['station'])
results.columns = ['Сокол', 'Маяковская', 'Речной вокзал',
       'Белорусская', 'Беломорская', 'Сходненская', 'Пражская',
       'Юго-Западная', 'Калужская']
results.T.to_csv('data/metroMatrix.csv')
print("Done")
