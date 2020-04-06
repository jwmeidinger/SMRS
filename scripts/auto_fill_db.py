import numpy as np  
import pandas as pd   
import names 
import random
import string
import requests


df = pd.DataFrame(columns=['Project','Team','Team members'])
df2 = pd.DataFrame(columns = ['DateOpened','DateClosed','ProjectID','WhereFound','Tag','Severity','Url',"Description"])

for x in range(20):
    
    df = df.append({'Project': random.randint(1,21), 'Team': random.choice(string.ascii_uppercase), 'Team members': 0, 'Review': random.randint(1000,2000), 'Defect': random.randint(500,1000)}, ignore_index = True)
    df2 = df2.append({'DateOpened':"{}-{}-{}".format(random.randint(2000,2020),random.randint(0,11)+1,random.randint(0,29)+1),'DateClosed':"{}-{}-{}".format(random.randint(2000,2020),random.randint(0,11)+1,random.randint(0,29)+1),'ProjectID' : random.randint(15,40),'WhereFound': 1,'Tag': "tag {}".format(x),'Severity': "Minor",'Url':"https://www.github.com/{}".format(x),'Description': "It is a problem"}, ignore_index = True)

myToken = '73c4114212d8918012b10f33e8b0a2afdb0b4b30'
head = {'Authorization': 'Token {}'.format(myToken)}  


"""
*** This is an example of creating a new Team
"""
for index, row in df.iterrows():
    string = "{}".format(row['Team'])
    data = {"name": string}
    r = requests.post('http://127.0.0.1:8000/restAPI/Team/', headers = head, data=data)
     


response = requests.get('http://127.0.0.1:8000/restAPI/{}/'.format('Team'))
json_response = response.json()
dic = {}
for x in range(len(json_response)):
    
    dic[json_response[x]["name"]] = json_response[x]["id"]
print(dic)

for index, row in df.iterrows():
    teamName = "{}".format(row['Team'])
    projectName = "{}".format(row['Project'])
    if(dic[teamName]!= ""):
        teamID = dic[teamName]

    data = {"name": projectName , "teamID" :teamID}
    r1 = requests.post('http://127.0.0.1:8000/restAPI/Project/', headers = head, data=data)
    print(r1.text)  


for index, row in df2.iterrows():
    
    data = {'dateOpened': "{}".format(row['DateOpened']),'dateClosed':"{}".format(row['DateClosed']),'projectID': "{}".format(row['ProjectID']),'whereFound': "{}".format(row['WhereFound']),'tag':"{}".format(row['Tag']),'severity':"{}".format(row['Severity']),'url':"{}".format(row['Url']),'description':"{}".format(row['Description'])}
    r2 = requests.post('http://127.0.0.1:8000/restAPI/Defect/', headers = head, data=data)
    print(r2.text)

for index, row in df2.iterrows():
    
    data = {'dateOpened': "{}".format(row['DateOpened']),'dateClosed':"{}".format(row['DateClosed']),'projectID': "{}".format(row['ProjectID']),'whereFound': "{}".format(row['WhereFound']),'tag':"{}".format(row['Tag']),'severity':"{}".format(row['Severity']),'url':"{}".format(row['Url'])}
    r2 = requests.post('http://127.0.0.1:8000/restAPI/Review/', headers = head, data=data)
    print(r2.text)

