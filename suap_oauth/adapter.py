import logging
import traceback
from urllib.parse import urlsplit

from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.utils import user_email, user_field


logger = logging.getLogger(__name__)


class SuapAdapter(DefaultSocialAccountAdapter):
    def on_authentication_error(
        self,
        request,
        provider,
        error=None,
        exception=None,
        extra_context=None,
    ):
        if provider.id == "suap" and exception is not None:
            response = getattr(exception, "response", None)
            status_code = getattr(response, "status_code", "unknown")
            endpoint = getattr(response, "url", None) or getattr(
                getattr(response, "request", None), "url", ""
            )
            endpoint_path = urlsplit(endpoint).path or "unknown endpoint"
            logger.error(
                "SUAP OAuth callback failed (%s; HTTP %s at %s)\n%s",
                type(exception).__name__,
                status_code,
                endpoint_path,
                "".join(traceback.format_tb(exception.__traceback__)),
            )
        return super().on_authentication_error(
            request,
            provider,
            error=error,
            exception=exception,
            extra_context=extra_context,
        )

    def populate_user(self, request, sociallogin, data):
        """
        Hook that can be used to further populate the user instance.

        For convenience, we populate several common fields.

        Note that the user instance being populated represents a
        suggested User instance that represents the social user that is
        in the process of being logged in.

        The User instance need not be completely valid and conflict
        free. For example, verifying whether or not the username
        already exists, is not a responsibility.
        """
        user = sociallogin.user
        user_email(user, data.get("email") or "")
        user_field(user, "username", data.get("username"))
        user_field(user, "nome_completo", data.get("nome_completo"))
        user_field(user, "first_name", data.get("first_name"))
        user_field(user, "last_name", data.get("last_name"))
        user_field(user, "cpf", data.get("cpf"))
        user_field(user, "instituicao", data.get("instituicao"))
        user_field(user, "vinculo", data.get("vinculo"))
        user_field(user, "matricula", data.get("matricula"))
        user_field(user, "campus", data.get("campus"))
        user_field(user, "curso", data.get("curso"))
        return user
