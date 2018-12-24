import bs4 as bs
import urllib.request
import csv
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome()
driver.get("https://www.imdb.com")
sauce = urllib.request.urlopen('https://www.imdb.com/title/tt0088930/?ref_=fn_al_tt_1').read()

name = []
character = []
name_str = ''
name_str_edited = 'Names:'
name_list = []
odd = []
even = []


td_count = 0
char_count = 0


html = driver.page_source
soup = bs.BeautifulSoup(sauce, 'lxml')
nav = soup.nav
title = 'Clue'
year = '1985'

try:
    inputElement = driver.find_element_by_id("navbar-query")
    inputElement.send_keys(title, ' ', year)
    inputElement.send_keys(Keys.ENTER)
    time.sleep(10)
    driver.find_element_by_link_text(title).click()
    for td_char in soup.find_all('td', class_='character'):
        # print(td_char.text)
        character.append(td_char.text + ', ')
        char_count += 1
        if char_count > 10:
            break

#try treating this like a string not a list to use regex to clean it up, slice the backend off first
    for td_char in soup.find_all('tr', class_='odd'):
        # print(td_char.text)
        odd.append(td_char.text + ', ')
        char_count += 1
        if char_count > 10:
            break

    for td_char in soup.find_all('tr', class_='even'):
        # print(td_char.text)
        even.append(td_char.text + ', ')
        char_count += 1
        if char_count > 10:
            break

    for i in name:
        name_str = ''.join(name)

    for i in name_str:
        name_list.append(i)

    for i in character:
        character_str = ''.join(character)
        character_str = character_str + ", "

    name_str = re.sub('\n', '', name_str)
    character_str = re.sub('\n', '', character_str)
    character_str = character_str[:-4]

except Exception as e:
    print('Exception found', format(e))
odd_str = ''
for i in odd:
    odd_str = ''.join(i)
# odd_str = odd_str[:20]
odd_str = re.sub(r'\n ...', '', odd_str)
odd = odd[:20]
print('odd: ', odd)
print('even: ', even)
#print('name string: ', name_str)
#print('name: ', name)
print('Characters: ', character_str)
