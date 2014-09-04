import mock

from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.models import AnonymousUser

from django.test import TestCase
from django.test import RequestFactory

from lizard_fancylayers import views


class TestHomepageView(TestCase):
    def setUp(self):
        self.view_function = views.HomepageView.as_view()

    def test_has_response(self):
        request = RequestFactory().get('/')
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.user = AnonymousUser()

        response = self.view_function(request, '')

        self.assertContains(response, 'Apps overview', status_code=200)
