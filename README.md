# SMRS
## Standardized Metrics Reporting and Storage
###### Read the whole thing if you want to save a lot of time.

#### Table of Contents

- [Overview](#overview)
- [What's in the API](#whats-in-the-api)
- [Requirements](#requirements)
- [API Key & Credentials](#api-key-and-credentials)
- [Installation & Run](#installation-and-run)
- [API Usage](#api-usage)
- [FAQ](#frequently-asked-questions)
- [Documentation & Resources](#documentation-and-resources)

---

## Overview

This project is part of the John Deere Standardized Metrics Reporting and Storage project. This project allows a django rest API to obtain reports from variety of repositories ones such as GitHub and Collaborative. Using the rest API to filter this information to a database and making a easy to use application to filter any and all information for John Deere engineers.

## What's in the API

The API consists of:

- Get request to obtain data from Team, Project, Review, Defects, ProductNumber, PhaseType and Account list.
- Ability to grant or delete Tokens as admins privileges.
- Ability for POST requests for authenticated users can create new objects such as Defects or Projects.
- Ability for DELETE requests for authenticated users can remove objects such as Defects or Projects.
- Ability for PATCH requests for authenticated users can modify objects such as Defects or Projects.
- Views allow for the showing of the objects but also allows to do all of the items listed above (Except grant tokens).


## Requirements

The following requirements must be met to use this API:

- Admin / super user to allow changes to overall database and to run server
- Python 3.5 or later
- All required installs from requirement.txt
- Operating systems: Windows* 7 or later, macOS, and Linux

## API Key and Credentials

The API uses a simple token-based HTTP Authentication scheme provided by [Django REST framework](https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication). When each user is created they are granted a token. The token can be removed from the Admin page. In order to use or view your token check out the [Usage](#usage) section.

*If you don't want every user to have a token check out [FAQ](#frequently-asked-questions) at the bottom.

## Installation and Run

(Local) How to set it up....

**Step 1 - Download from GitHub:**

Navigate to the GitHub page that is holding the projects code and click the download button, save to desktop.
    
**Step 2 - Start the Env:**

The environment is used to mitigate cross contamination for the server as we want to make sure we don't use items on your PC. This is how you start the Env.

    \Desktop\SMRS\DeereEnv\Scripts>activate
    
**Step 3 - Install requirements:**

If modules are missing from the environment this is how you can install the missing items. We recommend doing this anyways.

    \Desktop\SMRS>pip install -r requirements.txt
    
**Step 4 - Lastly run:**

    \Desktop\SMRS\SMRS>python manage.py runserver

## API Usage

This example demonstrates how to make requests to the running server

```python
import requests
import json

"""
*** Grab Team, Project, Review, Defect, Product, PhaseType, Users list
"""
item = 'Team'
r = requests.get('http://127.0.0.1:8000/restAPI/{}/'.format(item))
print(r.text)

"""
*** Grab your auth token.
"""
data = {'username':'admin@smrs.com','password':'pass'}
r = requests.post('http://127.0.0.1:8000/restAPI/auth-token/', data = data )
token = r.json()['token']
print(token)

"""
*** This is setting the headers as the auth token so you don't have to type it every time
    Reminder: change token below to the new token or simply use the token request above.
"""
myToken = '3e1fca608220a091aaf613e963ec3fc8a97573ca'
head = {'Authorization': 'Token {}'.format(myToken)}

"""
*** This is an example of creating a new Team.
"""
data = {"name": "D - Team"}
r = requests.post('http://127.0.0.1:8000/restAPI/Team/', headers = head, data=data)
print(r.text)

"""
*** This is an example of Deleting a Team.
"""
item = '6' ## remember to change the ID of team you want to change
r = requests.delete('http://127.0.0.1:8000/restAPI/Team/{}'.format(item), headers = head)
print(r.text)

```
Let's just say you just got this project. This is how you would set this up for easy uses.

1. ) Create a python script that gets all the infromation from all the repos. Gather all the info into a pandas table. lastly, For loop the requests into the server. A example file is in the scripts called dumdata.py

2. ) linux servers can run python scripts everyday or week to update the server.

## Frequently Asked Questions

### How do you create a new Admin / Super user?

    \Desktop\SMRS\SMRS>python manage.py createsuperuser

### How do you wipe the database?

1. ) You need delete the db.sqlite3 file.

2. ) Once the file is deleted you need to migrate which creates the database with the requirements of all the models.py files.

        \Desktop\SMRS\SMRS>python migrate

3. ) Lastly, create a new super user. (Q above)

### How do you make changes to the database?

If you make changes in any of models.py files I would advise to do this.

1. ) Once the file is modified you need to make migrations which creates a new file in the migrations folder for the app. 

        \Desktop\SMRS\SMRS>python makemigrations

2. ) Lastly, you need to migrate to the database.

        \Desktop\SMRS\SMRS>python migrate
   
3. ) Bonus: If the item is required it might ask you to create a default for the other items in the DB already.

### How do you add data to the database?

There are three ways to add data to the database.

1. ) First way of adding items is through the admin portal which can be done at doman.com/admin/

2. ) The second way and the fastest way is through the REST API which more info can be found [Above](#usage). We found the best way to do this is to put info into a pandas table and using a for loop going through each row with a request at the bottom. A mock data example can be found \Desktop\SMRS\scripts\dumdata.py . This can not be done with users unless you add it to the REST API.

3. ) The last way to create new entries is through the [Shell](https://docs.djangoproject.com/en/3.0/ref/django-admin/#shell).

### How do you add and remove tokens?

Every user should have a token when there account is created. If you do not want this look at the next question below.
To remove a token from someone you can do that from the admin portal which is doman.com/admin/ .

### I don't want everyone to have a token. How do I change that?

To simply put you can remove or comment out the last function on the SMRS/SMRS/Account/models.py and save.

If the users are already created you can still keep all the users and remove the tokens by simply doing the question above.

### How do you add a new item to the rest API?

I find it easier to watch then read so here is a good video that I used on [YouTube](https://youtu.be/263xt_4mBNc?t=226) but to make it short and sweet. The Rest-framework uses four main items. More info can be found in the resources below.

1. ) Models are used to create the tables used for the Database. Start here when making a new table or just adding a new item.

2. ) [Serializers](https://www.django-rest-framework.org/tutorial/1-serialization/) is used to change your models into a json format that you can view.

3. ) [Views](https://www.django-rest-framework.org/api-guide/viewsets/) is bringing everything together such as the data and template to display the info.

4. ) [Router](https://www.django-rest-framework.org/api-guide/routers/) is used to support for automatic URL routing to Django.

### How do you add a new App?

Below is the command to create the app but you also need to include it into the SMRS/SMRS/SMRS/settings.py under INSTALLED_APPS.

    \Desktop\SMRS\SMRS>python manage.py startapp {name of project}

### I changed the static files but it's not changing.

There is two reason this happens. One, you need to run this command when you change any static file.

    \Desktop\SMRS\SMRS>python manage.py collectstatic

Two, sometimes when using chrome it holds onto the css to load the pages faster and this can be fixed by using incognito or removing them in the chrome settings.

## Documentation and Resources

### Official Rest API Documentation

- [Django Documentation](https://www.djangoproject.com/)
- [Django Rest Framework](https://www.django-rest-framework.org/)
- [Django Models](https://docs.djangoproject.com/en/3.0/topics/db/models/)
- [Django Views](https://docs.djangoproject.com/en/3.0/topics/http/views/)
- [Django Urls](https://docs.djangoproject.com/en/3.0/topics/http/urls/)




