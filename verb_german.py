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
    def get_text(self,verb_in_div):
        """
            Lấy các nội dung bên trong thẻ div (các danh từ đã được chia theo ngữ pháp)
        """
        tr=verb_in_div.find_all("tr")
        td=[]
        for t in tr:
            dir_={}
            td_=t.find_all("td")
            
            # print(f"len td: {len(td)}")
            if len(td_)>1:
                # dir_['conjugated_verbs']="None"
                dir_["type"]=td_[0].text
                dir_['conjugated_verbs']=td_[1].text
                td.append(dir_)
            else: 
                dir_['conjuge']=td_[0].text
                td.append(dir_)
        return td
    def main(self):
        # div_tag=self.soup.find_all()
        data_all=[]
        for v in range(10):
            print(f"verb{v}: {self.verb[v]}")
            if self.verb[v]=="": continue
            response=requests.get(self.url+str(self.verb[v]))
            soup=BeautifulSoup(response.content,"html.parser")
            section=soup.find_all("section", class_="rBox rBoxWht")
            print(len(section))
            if len(section)==0: 
                print("no identification")
                continue
            one_verb={} # Lưu trữ nội dung của từng trang
            one_verb['verb']=self.verb[v]
            p_tag=soup.find_all("a", class_="rKnpf rNoSelect rLinks")
            if len(p_tag)==0: verb_recommnend=self.verb[v]
            else:
                verb_recommnend=p_tag[len(p_tag)-1].find("b").text
            one_verb['verb_recommend']=verb_recommnend
            total_data=[]
            # total_data.append()
            se=len(section)
            if len(section)>6: se=6

            for s in range(1,se+1):
                # print(s)
                data_div=[] 
                data_section={} # lưu trữ nội dung của từng section trong một trang
                div=section[s].find_all("div", class_="vTbl")
                if s==1:
                    data_section['section']="simple"
                    data_div=[] # Lưu trữ nội dung của từng thẻ div
                    for d in div:
                        div_dic={} # Lưu trữ nội dung các động từ được chia
                        div_dic['tense']=d.find("h2").text
                        div_dic['content']=self.get_text(d) 
                        
                        data_div.append(div_dic) # Gộp các động từ đã được chia vào biến lưu trữ thẻ div
                    data_section['content_section']=data_div # Gán dữ liệu của thẻ div vào các section
                else:
                    data_section['section']=section[s].find("h2").text
                    data_div=[]
                    for d in div:
                        div_dic={}
                        div_dic['tense']=d.find("h3").text
                        div_dic['content']=self.get_text(d)
                        
                        data_div.append(div_dic) # Gộp các động từ đã được chia vào biến lưu trữ thẻ div
                    data_section['content_section']=data_div # Gán dữ liệu của thẻ div vào các section
                # print(f" data section: {data_section}")
                total_data.append(data_section) # Gộp dữu liệu các section vào biến lưu trữ trang request
                print(total_data)
            one_verb['results']=total_data # Gán dữ liệu của trang request vào biến lưu trữ theo động từ
            data_all.append(one_verb) # Gộp dữ liệu biến lưu trữ động từ vào dữ liệu tổng 
        with open("data_verb.json","w",encoding="utf-8") as f:
            json.dump(data_all,f,ensure_ascii=False)
                
                    



if __name__=="__main__":
    url="https://www.verbformen.com/conjugation/?w="
    v=Verb_noun(mydb,url)
    v.main()