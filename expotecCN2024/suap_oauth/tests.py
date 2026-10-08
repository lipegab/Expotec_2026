from types import SimpleNamespace
from unittest.mock import Mock, patch

from django.test import SimpleTestCase

from .adapter import SuapAdapter
from .provider import SuapProvider
from .views import SuapOAuth2Adapter


class SuapAdapterTests(SimpleTestCase):
    def test_authentication_errors_log_http_details_without_secrets(self):
        exception = ValueError("sensitive response data")
        exception.response = SimpleNamespace(
            status_code=401,
            url="https://suap.example/o/token/?secret=do-not-log",
        )

        with self.assertLogs("suap_oauth.adapter", level="ERROR") as captured:
            SuapAdapter().on_authentication_error(
                request=object(),
                provider=SimpleNamespace(id="suap"),
                exception=exception,
            )

        message = captured.output[0]
        self.assertIn("ValueError; HTTP 401 at /o/token/", message)
        self.assertNotIn("do-not-log", message)
        self.assertNotIn("sensitive response data", captured.output[0])


class SuapOAuth2AdapterTests(SimpleTestCase):
    @patch("suap_oauth.views.get_adapter")
    def test_complete_login_fetches_profile_with_bearer_token(self, get_adapter):
        response = Mock()
        response.json.return_value = {"cpf": "12345678901"}
        get_adapter.return_value.get_requests_session.return_value.get.return_value = (
            response
        )
        sociallogin = object()
        provider = Mock()
        provider.sociallogin_from_response.return_value = sociallogin
        adapter = SuapOAuth2Adapter(request=object())

        with patch.object(adapter, "get_provider", return_value=provider):
            result = adapter.complete_login(
                request=object(),
                app=object(),
                token=SimpleNamespace(token="access-token"),
            )

        get_adapter.return_value.get_requests_session.return_value.get.assert_called_once_with(
            "https://suap.ifrn.edu.br/api/rh/eu/",
            headers={"Authorization": "Bearer access-token"},
        )
        self.assertIs(result, sociallogin)


class SuapProviderTests(SimpleTestCase):
    def test_profile_mapping_uses_suap_api_fields(self):
        provider = SuapProvider(None, app=Mock())
        profile = {
            "nome_registro": "Maria da Silva",
            "primeiro_nome": "Maria",
            "ultimo_nome": "Silva",
            "email_preferencial": "maria@example.com",
            "cpf": None,
            "identificacao": "123",
            "tipo_usuario": "Aluno",
            "campus": "CN",
        }

        fields = provider.extract_common_fields(profile)

        self.assertEqual(provider.extract_uid(profile), "123")
        self.assertEqual(fields["cpf"], "")
        self.assertEqual(fields["email"], "maria@example.com")
        self.assertEqual(fields["first_name"], "Maria")
        self.assertEqual(fields["last_name"], "Silva")
