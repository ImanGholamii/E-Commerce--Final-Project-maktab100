from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


# Create your tests here.
class EmailSendingAPITest(TestCase):
    def setUp(self):
        pass

    def test_email_sending_endpoint(self):
        url = reverse('email_sender:mock-send-email-api')
        client = APIClient()

        data = {
            # 'to': 'imangholamiimi@gmail.com',
            # 'from': 'sharlotimi@gmail.com',
            'subject': 'test automatic',
            'body': 'Hello',
            'recipient': '',
        }
        response = client.post(url, data, format='json')
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edge_cases(self):
        pass

    def test_authentication(self):
        pass

    def test_email_content(self):
        pass

    def test_performance(self):
        pass

    def test_input_validation(self):
        pass
