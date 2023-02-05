import requests
import csv
from bs4 import BeautifulSoup
from itertools import zip_longest

class JobScrape:


    def __init__(self):


        self.result=None
        self.job_title = []
        self.company_name = []
        self.links=[]
        self.description=[]

    def saveandpasre(self):
        # fetch the url using request
        self.result = requests.get(
            "https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=Data+Analysis&txtLocation=")

        src=self.result.content

        # find the elements containing data that we need
        soup = BeautifulSoup(src, 'html.parser')
        job_titles=soup.find_all("h2")
        company_names = soup.find_all("h3", {"class": "joblist-comp-name"})
        for i in range(len(company_names)):
                self.job_title.append(job_titles[i].text.strip())
                self.links.append(job_titles[i].find('a').attrs['href'])
                self.company_name.append(company_names[i].text.replace("\n",""))

        for link in self.links:
               res=requests.get(link)
               src=res.content
               soup=BeautifulSoup(src,'html.parser')
               descriptions=soup.find('div',{"class":"jd-desc job-description-main"})
               self.description.append(descriptions.text.strip())
        return self.job_title,self.company_name,self.links,self.description




    def create_csv(self):
        # create csv file to save data

        file_list=[self.job_title,self.company_name,self.links,self.description]
        exported=zip_longest(*file_list)
        with open("JobsDetails.csv","w") as csvfile:
               write=csv.writer(csvfile)
               write.writerow(["Job Title","Company Name","links",'description'])
               write.writerows(exported)

        return "Done"


if __name__ == '__main__':
    Job=JobScrape()
    print(Job.saveandpasre())
    print(Job.create_csv())

