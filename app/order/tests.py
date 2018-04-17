from django.urls import reverse, resolve
from rest_framework.test import APITestCase

from order import apis


class Order(APITestCase):
    VIEW = apis.OrderView
    URL_PATH = '/api/order/payment/'
    URL_NAME = 'order:payment'

    def test1_url(self):
        """
        주문 신청 URL이 제대로 할당되었는지 체크
        :return:
        """
        reverse_url = reverse(self.URL_NAME)
        self.assertEqual(self.URL_PATH, reverse_url, 'Order API: URL_NAME')

        resolve_view = resolve(self.URL_PATH)
        self.assertEqual(self.URL_NAME, resolve_view.view_name, 'Order API: URL_PATH')
        self.assertEqual(self.VIEW.as_view().__name__, resolve_view.func.__name__, 'Order API: View Class')
