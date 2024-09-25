import requests
from bs4 import BeautifulSoup

#r = requests.get(".KR.html")
html = open("KR.html", "r")

index = html.read()




soup = BeautifulSoup(index, 'lxml')

table = soup.find_all('table')[4]#, class_='ng-binding')
print(table)
if table:
    style = table.get('style')
    if style and 'background-color' in style:
        print(style)
        #background_color = style.split('background-color')
    else:
        print("No background color found in inline style.")
else:
    print("no table found on the page.")

#print(table)


"""
rows = table.find_all('tr')
print(rows)#print(content)
print(len(rows))
 
for i,row in enumerate(rows):
    content = row.find_all('div', class_="ng-binding")
    print(i)
    for j, div in enumerate(content):
        print(i,j)
        print(div.text.strip())
        print("\n")

"""