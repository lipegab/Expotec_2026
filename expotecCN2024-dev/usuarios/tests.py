from types import SimpleNamespace
from unittest.mock import Mock

from django.test import RequestFactory, SimpleTestCase
from django.urls import reverse

from .views import IndexView, InscreverseView, MinhasInscricoesView


class UserIndexViewTests(SimpleTestCase):
    def test_redirects_to_profile_when_no_event_is_configured(self):
        request = RequestFactory().get("/users/")
        request.user = SimpleNamespace(is_authenticated=True)
        request.evento = None

        response = IndexView.as_view()(request)

        self.assertRedirects(
            response,
            reverse("user:meu_perfil"),
            fetch_redirect_response=False,
        )


class UserEventViewsTests(SimpleTestCase):
    def setUp(self):
        self.request = RequestFactory().get("/users/me/inscricoes/")
        self.request.user = SimpleNamespace(is_authenticated=True)
        self.request.evento = None

    def test_my_registrations_redirects_to_profile_when_no_event_exists(self):
        response = MinhasInscricoesView().get(self.request)

        self.assertRedirects(
            response,
            reverse("user:meu_perfil"),
            fetch_redirect_response=False,
        )

    def test_event_signup_redirects_to_profile_when_no_event_exists(self):
        response = InscreverseView().get(self.request)

        self.assertRedirects(
            response,
            reverse("user:meu_perfil"),
            fetch_redirect_response=False,
        )
