"""
Author: Joseph Rios
Webpage scraper for wordbrain.info

Creates puzzle files from the website
Creates a solution file for all of them

Uses BeautifulSoup4 and Requests
"""
import requests
from bs4 import BeautifulSoup

puzzles = []
solutions = []

def scrape(url):
    global puzzles,solutions
    soup = BeautifulSoup(requests.get(url).content,"html.parser")
    lbs = soup.find_all("span","letterblock")
    sbs = soup.find_all("span","solution")
    for each in lbs:
        temp = []
        for i in each.find_all("span"):
            temp.append(i.contents[0])
        n = int(len(temp)/len(each.find_all("br"))) 
        temp = ["".join(temp[i:i+n]) for i in range(0, len(temp), n)]
        puzzles.append(temp)
    for each in sbs:
        while(each.br!=None):
            each.br.decompose()
        for i in range(len(each.contents)):
            each.contents[i] = each.contents[i].strip()
            if(each.contents[i][-1]==","):
                #Strip away the comma
                each.contents[i]=each.contents[i][:-1]
        solutions.append(each.contents)

def make_files():
    #Make Puzzle Files
    for i in range(len(puzzles)):
        with open(str(i)+".txt",'w') as f:
            for soln in solutions[i]:
                f.write(str(len(soln))+" ")
            f.write("\n")
            for line in puzzles[i]:
                line = line.upper()
                f.write(line+"\n")
    #Make Solution File
    with open("solutions.txt",'w') as f:
        for soln in solutions:
            for i in range(len(soln)):
                soln[i] = soln[i].upper()
            f.write(" ".join(soln)+"\n")

def main():
    base_url = "http://wordbrain.info/en/"
    urls = []
    with open("cat1.txt","r") as f:
        data = f.readlines()
    data = list(map(lambda x: x.strip(),data))
    for cat in data:
        urls.append(base_url+cat+"/")
    with open("cat2.txt","r") as f:
        data = f.readlines()
    data = list(map(lambda x: x.strip(),data))
    for cat in data:
        urls.append(base_url+"themes/"+cat+"/")
    for url in urls:
        scrape(url)
    make_files()

if(__name__=="__main__"):
    main()
