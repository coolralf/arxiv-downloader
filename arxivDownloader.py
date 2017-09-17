# Requirements: beautifulsoup4,requests, aria2 , lxml 
import os,requests,re,sys
from bs4 import BeautifulSoup

def downloadFile(url):
    os.system("aria2c %s"%url)
    return 0

def getPage(url):
    s = requests.Session()
    data = s.get(url).text

    soup = BeautifulSoup(data,"lxml")
    downloadUrls = soup.find_all('a',title="Download PDF")
    info = []
    for i in range(len(downloadUrls)):
        temp = "https://arxiv.org"+downloadUrls[i]['href'] +".pdf"
        info.append(temp)
    return info

def getInfo(url):
    s = requests.Session()
    
    flag = True
    info = []

    num = 1
    print("Start Searching!")
    while flag == True:
        data = s.get(url).text
        soup = BeautifulSoup(data,"lxml")
        endPage = soup.find('a',text="Next 25 results")
        if endPage == None:
            flag = False
        else:
            endPage = "https://arxiv.org"+endPage['href']
        info = info + getPage(url)
        url = endPage
        print("Page %i finished!"%num)
        num = num+1
    print("All pages finished!") 
    return info 

if __name__== "__main__":
    searchName = sys.argv[1]
    #print(searchName)
    #basicUrl = "https://arxiv.org/find/all/1/all:+%s/0/1/0/all/0/1"%searchName
    url = "https://arxiv.org/find/all/1/all:+"+ searchName +"/0/1/0/all/0/1"
    #url = searchName + basicUrl
    
    info = getInfo(url)

    print("Start Downloading!")
    
    for i in range(len(info)):
        downloadFile(info[i])
        print("File [%s/%s] finished!"%(i+1,len(info)))

    print("Dowloading Finished!")
            
    




    