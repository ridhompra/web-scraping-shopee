from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd
import time 

opsi = webdriver.ChromeOptions()
opsi.add_argument('--headless')
s = Service('chromedriver')

driver = webdriver.Chrome(service=s, options= opsi)
key = input('mau cari apa : ')
shopee_url = 'https://shopee.co.id/search?keyword={}'.format(key)
base_url = 'https://shopee.co.id'
driver.set_window_size(1300,800)

driver.get(shopee_url)

rentang = 500
for i in range(1,9):
    akhir = rentang * i
    perintah = "window.scrollTo(0,"+str(akhir)+")"
    driver.execute_script(perintah)
    print('loading ke - '+ str(i))
    time.sleep(10)

time.sleep(5)

# menyimpan tampilan ketika selenium melakukan akses pada URL
driver.save_screenshot('home.png')
# akan mengambil source tag di HTML
content = driver.page_source


data = BeautifulSoup(content,'html.parser')
# print(data.encode('utf-8'))

#find all akan mencari semua data dengan ciri khusu yg diberikan (div, a, body)
# tag div ini memiliki class apa (class yang ingin dicari)
list_nama,list_gambar,list_harga,list_terjual,list_loc,list_link = [],[],[],[],[],[]

no = 0
for area in data.find_all('div', class_='VTjd7p whIxGK'):
    nama = area.find('div', class_='ie3A+n bM+7UW Cve6sh').getText()
    gambar = area.find('img')['src']
    harga = area.find('div',class_='vioxXd rVLWG6').get_text()
    terjual = area.find('div',class_='r6HknA uEPGHT')
    if terjual != None:
        terjual = terjual.get_text()
    loc = area.find('div',class_='zGGwiV').get_text()
    # link = area.find('a')['href']
    no+=1
    # print('== '*25,'\n',no)
    # print(nama)
    # print(gambar)
    # print(harga)
    # print(terjual)
    # print(loc)
    # print(link)
    print(f'> processing data ke - {no}')
    list_nama.append(nama)
    list_gambar.append(gambar)
    list_harga.append(harga)
    list_terjual.append(terjual)
    list_loc.append(loc)
    # list_link.append(link)

df = pd.DataFrame({'nama':list_nama, 'gambar':list_gambar, 'harga': list_harga, 'terjual': list_terjual, 'location': list_loc})
writer = pd.ExcelWriter(f'{key}.xlsx')
df.to_excel(writer,'sheet1',index=False)
# writer.save()

driver.quit()
