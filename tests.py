from rest_framework.test import APITestCase
from rest_framework import status


class StatusResponseTest(APITestCase):
	"""
		GET request to /subscriptioninfo/ will fetch all customers info,
		this test will pass if a successful get request response return HTTP 200_OK
	"""	
	def test_get_customer_info_request(self):
		response = self.client.get('/subscriptioninfo/')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		print("\nTHis test will pass after successfully getting a HTTP_200_OK response")


class NotAllowedResponseTest(APITestCase):
	"""
		Put request to /subscriptioninfo/, this route only support GET & POST request,
		also no credential data is passed with the endpoint,
		this test will pass if a put request with provided data has return 403_FORBIDDEN
	"""
	def test_put_customer_info_request(self):
		customer_data = {"subscriber_name": "John", "plan_type": "Bronze", 
			"primary_phone_number": "01823459878"}
		response = self.client.put("/subscriptioninfo/", customer_data)
		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
		print("\nThis test will pass if put request return a response of HTTP_403_FORBIDDEN!\n")
