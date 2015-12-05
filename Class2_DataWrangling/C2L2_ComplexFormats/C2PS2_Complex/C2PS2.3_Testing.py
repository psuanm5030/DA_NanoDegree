__author__ = 'Miller'

from bs4 import BeautifulSoup

datadir = '/Users/Miller/GitHub/GhNanoDegree/Class_DataWrangling/Lesson2_ComplexFormats/PS2_Complex/data/FL-ATL.html'

data = []

with open(datadir) as html:
    soup = BeautifulSoup(html)
    for item in soup.find_all(class_='dataTDRight'):
        info = {}
        info["courier"], info["airport"] = ('FL','ATL')
        try:
            val = int(item.text[:8])
            cnt = 0
            print item.text
            for i in item.find_all('td'):
                print cnt, i.text
                if cnt == 0: info['year'] = i.text.strip()
                elif cnt == 1: info['month'] = i.text.strip()
                elif cnt == 2:
                    info['flights']={}
                    info['flights']['domestic'] = int(i.text.replace(',',''))
                elif cnt == 3: info['flights']['international'] = int(i.text.replace(',',''))
                cnt += 1
        except:
            continue
        print info
        p = info.copy()
        data.append(p)

print data
