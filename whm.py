# from selenium import webdriver
# title = 'Number One With a Bullet'
# driver = webdriver.Chrome()
# # driver.get("https://www.google.com")
# # driver.get("https://www.imdb.com/find?ref_=nv_sr_fn&q=number+one+with+a+bullet+1987&s=all")
# driver.get("https://www.imdb.com")
# # submit_button - driver.find_elements_by_
# try:
#     # eleml = driver.find_element_by_link_text("Gmail")
#     eleml = driver.find_element_by_link_text("Movies")
#     print('Test Pass: Element found by link text')
#     eleml.click()
#
# except Exception as e:
#     print('Exception found', format(e))
#
# driver.close()


# eleml = driver.find_element_by_link_text("/title/tt0093658/?ref =fn al tt 1")
# print(eleml)
# eleml.click()
# element = driver.find_element_by_id("primary photo")
#
import re

l = '\n\n \n\n Eileen Brennan\n \n\n              ...\n          \n\nMrs. Peacock\n\n, '
print(l)
l = re.sub('\n, ', '', l)
print(l)
# for i in l:
#     print(i)
#     if "Mrs. Peacock" in i:
#         print('yay')
input('press enter to quit')