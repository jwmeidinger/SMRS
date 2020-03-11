import requests
import json

"""
*** Grap Team, Project, Review, Defect, ProductNumber, PhaseType, Users list
"""
item = 'Team'
r = requests.get('http://127.0.0.1:8000/restAPI/{}/'.format(item))
print(r.text)

"""
*** Grap your auth token
"""
#data = {'username':'admin@smrs.com','password':'pass'}
#r = requests.post('http://127.0.0.1:8000/restAPI/auth-token/',data = data )
#token = r.json()['token']
#print(token)

"""
*** This is setting the headers as the auth token so you don't have to type it every time
"""
myToken = '3e1fca608220a091aaf613e963ec3fc8a97573ca'
head = {'Authorization': 'Token {}'.format(myToken)}

"""
*** This is an example of creating a new Team
"""
#data = {"name": "D - Team"}
#r = requests.post('http://127.0.0.1:8000/restAPI/Team/', headers = head, data=data)
#print(r.text)

"""
*** This is an example of Deleting a Team
"""
#item = '6' ## remember to change the ID of team you want to change
#r = requests.delete('http://127.0.0.1:8000/restAPI/Team/{}'.format(item),headers = head)
#print(r.text)

