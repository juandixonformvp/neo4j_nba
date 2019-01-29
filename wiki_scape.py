from bs4 import BeautifulSoup
import urllib.request
import re
import numpy as np
wiki = "https://en.wikipedia.org/wiki/List_of_2015%E2%80%9316_NBA_season_transactions"
hdr = {'User-Agent': 'Mozilla/5.0'}
req = urllib.request.Request(wiki,headers=hdr)
page = urllib.request.urlopen(req)
soup = BeautifulSoup(page)


tables = soup.findAll("table")
myTable = tables[5]
rows = myTable.findAll('tr')

data = [[td.findChildren(text=True) for td in tr.findAll("td")] for tr in rows]
myList = ['June','July','August','September','October','November','December','January','February','Hawks','Celtics','Nets','Hornets','Bulls','Cavaliers','Mavericks','Nuggets','Pistons','Warriors','Rockets','Pacers','Clippers','Lakers','Grizzlies','Heat','Bucks','Timberwolves','Pelicans','Knicks','Thunder','Magic','76ers','Suns','Blazers','Kings','Spurs','Raptors','Jazz','Wizards']
pickList = ['first','second','Hawks','Celtics','Nets','Hornets','Bulls','Cavaliers','Mavericks','Nuggets','Pistons','Warriors','Rockets','Pacers','Clippers','Lakers','Grizzlies','Heat','Bucks','Timberwolves','Pelicans','Knicks','Thunder','Magic','76ers','Suns','Blazers','Kings','Spurs','Raptors','Jazz','Wizards']
#myre = re.compile('|'.join(myList))
myre = re.compile(r'\b(?:%s)\b' % '|'.join(myList))
pickre = re.compile(r'\b(?:%s)\b' % '|'.join(pickList))
result = []
#for i in range(len(data)): print(myre.findall(str(data[i])))
for i in range(len(data)): result.append(myre.findall(str(data[i])))
#result = myre.findall(str(data))
result = list(filter(None, result))

pickResult = []
#for i in range(len(data)): print(myre.findall(str(data[i])))
for i in range(len(data)): pickResult.append(pickre.findall(str(data[i])))
#result = myre.findall(str(data))
pickResult = list(filter(None, pickResult))

#print(pickResult)

#adds the missing month
for i in range(len(result)):
    if len(result[i]) == 2:
        if len(result[i-1]) != 1:
            result[i].insert(0,result[i-1][0])
        else:
            result[i].insert(0, result[i-2][0])

#print(result)

#accounts for three way trades
for i in range(len(result)):
    if len(result[i]) == 1:
        result[i].insert(0, result[i - 1][0])
        result[i].append(result[i - 1][2])

#print(result)


for i in range(len(pickResult)):
    for j in pickResult[i]:
        #print(j)
        if j == "first":
            #print(j)
            result[i].insert(pickResult[i].index(j),"first")
        if j == "second":
            #print(j)
            result[i].insert(pickResult[i].index(j), "second")


def uniq(input):
    output = []
    for x in input:
        if x not in output:
            output.append(x)
    return output

resultNew =[]
for r in result:
    resultNew.append(uniq(r))

#print(resultNew)
#print(result)
#print(len(result))
#print(len(pickResult))


