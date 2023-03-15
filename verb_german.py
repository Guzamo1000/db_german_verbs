import requests
from bs4 import  BeautifulSoup
import pandas as pd 
import mysql.connector
import json

mydb = mysql.connector.connect(
  host="localhost",
  user="user1",
  password="password1",
  database="german"
)
class Verb_noun:
    def __init__(self, mydb,url):
        self.url=url
        df=pd.read_sql("Select * from verben", mydb)
        self.verb=list(set(df['form']))
    def get_text(self,section):
        tr=section.find_all("tr")
        td=[]
        for t in tr:
            dir_={}
            td_=t.find_all("td")
            dir_["type"]=td_[0].text
            if len(td_)>1:
                # dir_['conjugated_verbs']="None"
                dir_['conjugated_verbs']=td_[1].text
                td.append(dir_)
            
        return td
    def main(self):
        # div_tag=self.soup.find_all()
        for v in range(len(self.verb)):
            print(f"verb{v}: {self.verb[v]}")
            if self.verb[v]=="": continue
            response=requests.get(self.url+str(self.verb[v]))
            soup=BeautifulSoup(response.content,"html.parser")
            section=soup.find_all("section", class_="rBox rBoxWht")
            if len(section)==0: 
                print("no identification")
                continue
            total_data=[]
            se=len(section)
            if len(section)>6: se=6
            
            for s in range(1,se+1):
                data_section={}
                div=section[s].find_all("div", class_="vTbl")
                if s==1:
                    data_section['section']="simple"
                    for d in div:
                        div_data={}
                        div_data['tense']=d.find("h2").text
                        div_data['content']=self.get_text(d)
                        data_section['content_section']=div_data
                else:
                    data_section['section']=section[s].find("h2").text
                    for d in div:
                        div_data={}
                        div_data['tense']=d.find("h3").text
                        div_data['content']=self.get_text(d)
                        data_section['content_section']=div_data
                total_data.append(data_section)
            print(total_data)

                
                    



if __name__=="__main__":
    url="https://www.verbformen.com/conjugation/?w="
    v=Verb_noun(mydb,url)
    v.main()