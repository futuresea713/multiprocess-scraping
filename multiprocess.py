import requests
from bs4 import BeautifulSoup
import csv
from multiprocessing import Pool, freeze_support



def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def scraping(var1):
   allresults = []
   headers = {
       "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
       "Accept-Encoding": "*",
       "Connection": "keep-alive"
   }
   OldURL = "https://www.healthcare6.com/search/?svc=&state=&city=&count=25709&keywords=Dermatology&button=&page={}".format(var1)
   r = requests.get(OldURL, headers=headers)
   soup = BeautifulSoup(r.content, 'html.parser')
   tablecontent = soup.find('table', attrs={'class': 'table table-condensed'})
   for idx,table in enumerate(tablecontent.findAll('tr')):
       if idx != 0:
           result = []
           try:
               # tdlocation = table.find("td", attrs={'class': 'pt18'})
               name = table.find("h2").text
               result.append(name)
           except:
               result.append(" ")
               pass
           try:
               # tdlocation = table.find("td", attrs = {'class': 'pt18'})
               location = table.find("div", attrs = {'class' : 'hidden-xs'}).text
               result.append(location)
           except:
               result.append(" ")
               pass
           allresults.append(result)


   return allresults





if __name__ == '__main__':

    freeze_support()

    result = list(chunks(range(1, 1430), 5))

    for res in result:
        lis = list(res)
        with Pool(processes=5) as pool:
          allresults1 = pool.map(scraping, lis)
          for all in allresults1:
              with open("scraping-name-location2.csv", "a", newline="", encoding="utf-8") as fe:
                  writer = csv.writer(fe)
                  writer.writerows(all)

    print("done~~")

















