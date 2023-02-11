#!/usr/bin/env python
# coding: utf-8

# In[147]:


import csv
from datetime import datetime
import requests
from bs4 import BeautifulSoup


# In[148]:


template='https://in.indeed.com/jobs?q={}&l={}'
#https://in.indeed.com/jobs?q=computer%20science&l=india&start=


# In[149]:


def  get_url(position,location):
    template='https://in.indeed.com/jobs?q={}&l={}'
    url= template.format(position,location)
    return url


# In[150]:


url=get_url('Computer science','india')


# # extract raw html

# In[152]:


response=requests.get(url)


# In[153]:


response


# In[154]:


response.reason


# In[155]:


soup=BeautifulSoup(response.text,'html.parser')


# In[156]:


cards=soup.find_all('div','cardOutline')


# In[157]:


len(cards)


# In[158]:


print(cards)


# In[159]:


card=cards[0]


# In[160]:


#name
atag =card.h2.a


# In[161]:


job_title=card.find('h2','jobTitle').text.strip()


# In[162]:


job_title


# In[163]:


job_url='https://in.indeed.com'+atag.get('href')


# In[164]:


company=card.find('span','companyName').text.strip()


# In[165]:


company


# In[166]:


job_location=card.find('div','companyLocation').text.strip()


# In[167]:


job_location


# In[168]:


job_summary=card.find('div','job-snippet').text.strip().replace('\n',',')


# In[169]:


job_summary


# In[170]:


post_date=card.find('span','date').text.strip()


# In[171]:


post_date


# In[172]:


today=datetime.today().strftime('%Y-%m-%d')


# In[173]:


today


# In[174]:


try:
    
    job_salary=card.find('div','metadata salary-snippet-container').text.strip()
except:
    job_salary= ''


# In[175]:


job_salary


# # generalize the model with a function

# In[181]:


def get_record(card):
    atag =card.h2.a
    job_title=card.find('h2','jobTitle').text.strip()
    job_url='https://in.indeed.com'+atag.get('href')
    company=card.find('span','companyName').text.strip()
    job_location=card.find('div','companyLocation').text.strip()
    job_summary=card.find('div','job-snippet').text.strip().replace('\n',',')
    post_date=card.find('span','date').text.strip()
    today=datetime.today().strftime('%Y-%m-%d')
    
    try:
        job_salary=card.find('div','metadata salary-snippet-container').text.strip()
    except:
        job_salary= ''
        
    record =(job_title,company,job_location,job_summary,post_date,today,job_salary,job_url)   
    
    return record


# In[182]:


Records=[]
    
for card in cards:
    record =get_record(card)
    
    Records.append(record)


# In[183]:


Records[0]


# # get next page

# In[184]:


#soup.find('a',{'aria-label':'Next'}).get('href')


# In[185]:


while True:
    try:
        url='https://in.indeed.com'+ soup.find('a',{'aria-label':'Next'}).get('href')
    except AttributeError:  
        break
        
    response = requests.get(url)
    soup=BeautifulSoup(response.text,'html.parser')
    cards=soup.find_all('div','cardOutline')
    
    for card in cards:
        record =get_record(card)

        Records.append(record)
    
    


# In[186]:


len(Records)


# # putting all together

# In[202]:


import csv
from datetime import datetime
import requests
from bs4 import BeautifulSoup

def  get_url(position,location):
    template='https://in.indeed.com/jobs?q={}&l={}'
    url= template.format(position,location)
    return url

def get_record(card):
    atag =card.h2.a
    job_title=card.find('h2','jobTitle').text.strip()
    job_url='https://in.indeed.com'+atag.get('href')
    company=card.find('span','companyName').text.strip()
    job_location=card.find('div','companyLocation').text.strip()
    job_summary=card.find('div','job-snippet').text.strip().replace('\n',',')
    post_date=card.find('span','date').text.strip()
    today=datetime.today().strftime('%Y-%m-%d')
    
    try:
        job_salary=card.find('div','metadata salary-snippet-container').text.strip()
    except:
        job_salary= ''
        
    record =(job_title,company,job_location,job_summary,post_date,today,job_salary,job_url)   
    
    return record

def main(position,location):
    Records=[]
    url=get_url(position,location)
    
    #extracct the job data
    
    while True:
        response = requests.get(url)
        soup=BeautifulSoup(response.text,'html.parser')
        cards=soup.find_all('div','cardOutline')
        
        for card in cards:
            record =get_record(card)

            Records.append(record)
        try:
            url='https://in.indeed.com'+ soup.find('a',{'aria-label':'Next'}).get('href')
        except AttributeError:  
            break
        

    #save the job data
    
    with open('Computer_vision.csv','w',newline='', encoding='utf-8') as f:
        writer =csv.writer(f)
        writer.writerow(['job_title','company','job_location','job_summary','post_date','today','job_salary','job_url'])
        
        writer.writerows(Records)
    
    

    


# In[203]:


main('Computer Vision','india')


# In[ ]:




