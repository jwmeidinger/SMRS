# SMRS
## Standardized Metrics Reporting and Storage


#### Table of Contents

- [Overview](#overview)
- [What's in the API](#whats-in-the-api)
- [Requirements](#requirements)
- [API Key & Credentials](#api-key-and-credentials)
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Documentation & Resources](#documentation-and-resources)

---

## Overview

This project is part of the John Deere Standaridized Metrics Reporting and Storage project. This project allows a django rest API to obtain reports from variety of repositories ones such as github and Colaborative. Using the rest API to filter this information to a database and making a easy to use application to filter any and all information for John Deere engineers.

## What's in the API

The API conists of:

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
- Processors: Intel Atom® processor or Intel® Core™ i3 processor
- Disk space: 1 GB
- Operating systems: Windows* 7 or later, macOS, and Linux

## API Key and Credentials

The API uses a simple token-based HTTP Authentication scheme provided by [Django REST framework](https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication). When each user is created they are granted a token. The token can be removed from the Admin page. In order to use or view your token check out the [Usage](#usage) section.

*If you don't want every user to have a token check out SMRS/SMRS/Account/models.py at the bottom.

## Installation

How to set it up....

**Step 1 - Download from GitHub:**

    Navigate to the Github page that is holding the projects code and click the download button and to edit the codeopen it in         your chosen editor
    
**Step 2 - Start the Env:**

    

## Usage

This example demonstrates how to make requests to the running server

```python
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
data = {'username':'admin@smrs.com','password':'pass'}
r = requests.post('http://127.0.0.1:8000/restAPI/auth-token/',data = data )
token = r.json()['token']
print(token)

"""
*** This is setting the headers as the auth token so you don't have to type it every time
"""
myToken = '3e1fca608220a091aaf613e963ec3fc8a97573ca'
head = {'Authorization': 'Token {}'.format(myToken)}

"""
*** This is an example of creating a new Team
"""
data = {"name": "D - Team"}
r = requests.post('http://127.0.0.1:8000/restAPI/Team/', headers = head, data=data)
print(r.text)

"""
*** This is an example of Deleting a Team
"""
item = '6' ## remember to change the ID of team you want to change
r = requests.delete('http://127.0.0.1:8000/restAPI/Team/{}'.format(item),headers = head)
print(r.text)

```

## Features

### Item 1

example

### Item 2

example

### Item 3

example

## Documentation and Resources

### Official Rest API Documentation

- [Django Documentation](https://www.djangoproject.com/)
- [Django Rest Framework](https://www.django-rest-framework.org/)
- [item](put_link_here)
- [item](put_link_here)
- [item](put_link_here)



