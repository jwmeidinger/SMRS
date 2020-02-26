import requests
import coreapi

from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase
from .models import Defect
from .views import DefectView

class DefectModelTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username="admin@smrs.com", password="pass")

    def test_string_representation_defect(self):
        defect = Defect(tag="12345")
        self.assertEqual(str(defect), "12345")

    def test_post(self):

        data = {'username':'admin@smrs.com',
        'password':'pass'}
                
        token = requests.post('http://127.0.0.1:8000/restAPI/auth-token/',data = data )
        my_token = token.json()["token"]
        #print(my_token)

        #auth = coreapi.auth.TokenAuthentication(scheme="Token", token=my_token)
        #print(auth)
        #client = coreapi.Client(auth=auth)
        #response = client.get('http://127.0.0.1:8000/restAPI/Team/')
        #print(response)
        update_data = {'name':'D-Team'}
        response = requests.post('http://127.0.0.1:8000/restAPI/Team/',data = update_data, headers={'Authorization': 'Token {}'.format(my_token)})
        self.assertEqual(response.status_code, 200)

    def test_factory_post(self):
        request = self.factory.get('http://127.0.0.1:8000/restAPI/Team/')
        request.user = self.user

        response = DefectView(request)
        self.assertEqual(response.status_code, 200)