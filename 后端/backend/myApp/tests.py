from django.test import TestCase, Client
from myApp.models import *
import pandas as pd
import uuid

# Create your tests here.
class RegisterTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_task_submit(self):
        response1 = self.client.post('/api/submitPrint/', {'username': '12345678', 'dataStorage':[{'fileName':'报告', 'paper':'A4', 'color':'黑白', 'note':'无', 'doubleSided':True},
                                                                                           {'fileName':'论文', 'paper':'A3', 'color':'彩色', 'note':'打2份', 'doubleSided':False}]})
        self.assertEqual(response1.status_code, 200)
        print(list(Tasks.objects.all().values()))
        print(response1.content)
        # print(response2)
        # print(Tasks.objects.all().count())
        

