import numpy as np  
import pandas as pd   
import random
import string
import requests


"""
*** Making tables to input data
"""
df = pd.DataFrame(columns=['Project','Team','Team members'])
df2 = pd.DataFrame(columns = ['DateOpened','DateClosed','ProjectID','WhereFound','Tag','Severity','Url',"Description"])

for x in range(5):
    df = df.append({'Project': random.randint(1,21), 'Team': random.choice(string.ascii_uppercase), 'Team members': 0}, ignore_index = True)
for x in range(20):
    df2 = df2.append({'DateOpened':"{}-{}-{}".format(random.randint(2000,2020),random.randint(0,11)+1,random.randint(0,29)+1),'DateClosed':"{}-{}-{}".format(random.randint(2000,2020),random.randint(0,11)+1,random.randint(0,29)+1),'ProjectID' : random.randint(1,5),'WhereFound': random.randint(1,8),'Tag': "tags {}".format(x),'Severity': "Minor",'Url':"https://www.github.com/2{}".format(x),'Description': "It is a problem"}, ignore_index = True)


"""
*** Input admin Token
"""
myToken = '9e29fa76fc3a824e0e02eb4abcf43bd8ee193c95'
head = {'Authorization': 'Token {}'.format(myToken)}  


"""
*** This is an example of creating a new Team
"""
for index, row in df.iterrows():
    string = "{}".format(row['Team'])
    data = {"name": string}
    r = requests.post('http://127.0.0.1:8000/restAPI/Team/', headers = head, data=data)
     

"""
*** Getting the team names so we can get the ID of them and save them to a dict
"""
response = requests.get('http://127.0.0.1:8000/restAPI/{}/'.format('Team'))
json_response = response.json()
dic = {}
for x in range(len(json_response)):
    dic[json_response[x]["name"]] = json_response[x]["id"]
print(dic)


"""
*** Creating a post request for every new project that is being put into the API
"""
for index, row in df.iterrows():
    teamName = "{}".format(row['Team'])
    projectName = "{}".format(row['Project'])
    if teamName in dic:
        teamID = dic[teamName]
        print(teamID)
        data = {"name": projectName, "teamID": teamID, "projectNumber": projectName}
        r1 = requests.post('http://127.0.0.1:8000/restAPI/Project/', headers = head, data=data)
        print(r1.text) 


"""
*** Creating a post request for random defects
    Side Note: You will have to do the same thing as the Project POST for the projectID and whereFound
    As you will have a Project name and will need a PK found in API
"""
for index, row in df2.iterrows():
    data = {'dateOpened': "{}".format(row['DateOpened']),'dateClosed':"{}".format(row['DateClosed']),'projectID': "{}".format(row['ProjectID']),'whereFound': "{}".format(row['WhereFound']),'tag':"{}".format(row['Tag']),'severity':"{}".format(row['Severity']),'url':"{}".format(row['Url']),'description':"{}".format(row['Description'])}
    r2 = requests.post('http://127.0.0.1:8000/restAPI/Defect/', headers = head, data=data)
    print(r2.text)

"""
*** Creating a post request for random reviews
"""
for index, row in df2.iterrows():
    data = {'dateOpened': "{}".format(row['DateOpened']),'dateClosed':"{}".format(row['DateClosed']),'projectID': "{}".format(row['ProjectID']),'whereFound': "{}".format(row['WhereFound']),'tag':"{}".format(row['Tag']),'severity':"{}".format(row['Severity']),'url':"{}".format(row['Url'])}
    r2 = requests.post('http://127.0.0.1:8000/restAPI/Review/', headers = head, data=data)
    print(r2.text)

