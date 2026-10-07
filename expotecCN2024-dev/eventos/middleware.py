from django.utils.deprecation import MiddlewareMixin

from atividades.models import InscricaoAtividade

from .models import Avaliador, Evento, Monitor


class EventoSelecionadoMiddleware(MiddlewareMixin):

    def process_request(self, request):
        request.evento = Evento.objects.all().first()
        if not request.user.is_authenticated:
            request.user.is_evaluator = False
            return

        request.user.is_evaluator = False
        request.user.is_monitor = False
        request.user.avaliador = None
        request.user.monitor = None
        request.user.atividades = None

        if request.evento is None:
            return

        request.user.is_evaluator = request.evento.avaliadores.filter(
            usuario=request.user
        ).exists()
        request.user.is_monitor = request.evento.monitores.filter(
            usuario=request.user
        ).exists()
        request.user.avaliador = Avaliador.objects.filter(
            usuario=request.user, evento=request.evento
        ).first()
        request.user.monitor = Monitor.objects.filter(
            usuario=request.user, evento=request.evento
        ).first()
        request.user.atividades = InscricaoAtividade.objects.filter(
            usuario=request.user, atividade__tipo__evento=request.evento
        ).first()