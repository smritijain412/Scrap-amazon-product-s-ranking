# -*- coding: utf-8 -*-
"""
Created on Thu Sep 23 13:30:04 2021

@author: Smriti.Jain
"""

import requests
import re
import random
import pandas as pd
from selenium import webdriver



def scrapping(file_path,file):
        files=pd.read_excel(file_path)   #file_path 
        asin=files['ASIN'].to_list()
        
        n=random. randint(0,len(asin)-1)  #generate random number 
        
        
        # selenium for session id 
        driver = webdriver.Chrome (executable_path="chromedriver.exe")
        driver.maximize_window()
        url="https://www.amazon.com/dp/"+asin[n]
        driver.get(url)
        c = driver.session_id
       
        Header=({'user-agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
                'session_id': c})
        
        driver.close()
        
        clean = re.compile('<.*?>')
        
        
        res1={}  #store data in a dictionary
        print('Scrapping start')
        for i in asin:
            url="https://www.amazon.com/dp/"+i
            response = requests.get(url,headers=Header)
            try:
                idx=response.text.find('Best Sellers Rank')
                if idx!=-1: 
                    print('Scrapping Start',i)
                    ranks=response.text[idx:]
                    cl_1=re.sub(clean,'', ranks)
                    q=[re.split('# |\n',cl_1)[x] for x in range(10) if '#' in re.split('# |\n',cl_1)[x]]
                    q_=list(filter(None, q)) #remove None from list 
                    res1[i]=q_    
                    print('scrap done',i)
                else:
                    print('error')
                    break
                    #print('Error :',i)
            except Exception as e:
                print(e,i)
                
        #driver.close()
        print('Scrapping End')
          
        
        
        res2={}
        for k,v in res1.items():
            lis=[]
            for i in range(len(v)):
                lis.extend(v[i].split('(')[0].split(' in '))
            res2[k]=lis
        
        #save result in csv file  
        
        df=pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in res2.items()])).T # (Better)
        
        #create columns dynamically 
        c=[]
        l=df.shape[1]//2
        for i in range(1,l+1):
            c.extend(['Rank_level_'+str(i),'Category_'+str(i)])
            
            
        df.columns = c
        
        df.reset_index(inplace=True)
        df.rename(columns={'index':'Amazon ASIN'},inplace=True)
        
        
        for i in df.columns:
            df[i] = df[i].str.replace('#', ' ')
            
        print('scrap done!')
        
        df.to_csv(file,index=False)  #save csv
        return df
    
#call function 
file_path=input("enter file path")
scrapping(file_path,'scrap_products_BSR.csv')