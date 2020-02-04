import requests

#Get information from Team
r = requests.get('http://127.0.0.1:8000/restAPI/Team/')
print(r.text)

#Create Team
#r = requests.post('http://127.0.0.1:8000/restAPI/Team/',data = {'name':'D-Team'})
#print(r.text)

#Delete Team
#item = '4' ## remember to change the ID of team you want to change
#r = requests.delete('http://127.0.0.1:8000/restAPI/Team/{}'.format(item))
#print(r.text)