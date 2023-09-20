from django.test import TestCase
from django.contrib.sessions.middleware import SessionMiddleware
from django.test.client import Client


class MyTestCase(TestCase):
    def test_session_value(self):
        client = Client()
        # 세션 데이터 설정
        session_middleware = SessionMiddleware()
        request = self.client.request()
        session_middleware.process_request(request)
        request.session["load_count"] = 5  # 예시 값

        response = client.post('/login/', data={'username': 'username', 'password': 'password'})

        # 세션 데이터 확인
        self.assertEqual(request.session["load_count"], 6)  # 예상 값