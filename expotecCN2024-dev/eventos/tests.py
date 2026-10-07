from types import SimpleNamespace
from unittest.mock import Mock, patch

from django.test import RequestFactory, SimpleTestCase

from .middleware import EventoSelecionadoMiddleware


class EventoSelecionadoMiddlewareTests(SimpleTestCase):
    @patch("eventos.middleware.Evento.objects")
    def test_authenticated_user_without_event_gets_default_event_flags(
        self, evento_manager
    ):
        evento_manager.all.return_value.first.return_value = None
        request = RequestFactory().get("/users/")
        request.user = SimpleNamespace(is_authenticated=True)

        EventoSelecionadoMiddleware(get_response=Mock()).process_request(request)

        self.assertIsNone(request.evento)
        self.assertFalse(request.user.is_evaluator)
        self.assertFalse(request.user.is_monitor)
        self.assertIsNone(request.user.avaliador)
        self.assertIsNone(request.user.monitor)
        self.assertIsNone(request.user.atividades)
