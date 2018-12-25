import bs4 as bs
import urllib.request
import pandas as pd

sauce = urllib.request.urlopen('http://www.omdbapi.com/?t=the+happening&y=2008&r=xml&apikey=49f91ae0').read()
soup = bs.BeautifulSoup(sauce, 'xml')
output = str(soup)
print(soup)
f = open('clue_1985.xml', 'w+')
f.write(output)
f.close()

key = '49f91ae0'



