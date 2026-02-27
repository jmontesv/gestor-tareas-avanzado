from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from core.models import TaskList, Board
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.db import transaction
import json
from django.contrib.auth.decorators import login_required


# Vista para crear una nueva columna dentro de un tablero específico
class TaskListCreateView(LoginRequiredMixin, CreateView):
    model = TaskList
    fields = ["title"]
    template_name = "tasklists/create.html"

    def dispatch(self, request, *args, **kwargs):
        self.board = get_object_or_404(Board, pk=self.kwargs["board_id"])

        if request.user not in self.board.members.all() and request.user != self.board.created_by:
            return HttpResponseForbidden("No tienes acceso a este board")

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.board = self.board

        last_column = self.board.tasklists.order_by("-position").first()
        form.instance.position = (last_column.position + 1) if last_column else 0

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["board"] = self.board
        return context

    def get_success_url(self):
        return reverse_lazy("board_detail", kwargs={"pk": self.board.pk})

# Vista para reordenar columnas dentro de un tablero
@require_POST
@login_required
def reorder_tasklists(request):
    try:
        data = json.loads(request.body)

        if not data:
            return JsonResponse(
                {"success": False, "error": "Datos vacíos"},
                status=400
            )

        # Obtener todas las columnas enviadas
        tasklist_ids = [item["id"] for item in data]
        tasklists = TaskList.objects.select_related("board").filter(
            id__in=tasklist_ids
        )

        if not tasklists.exists():
            return JsonResponse(
                {"success": False, "error": "Columnas inválidas"},
                status=400
            )

        # Validar que todas pertenecen al mismo board
        board = tasklists.first().board
        if not all(t.board == board for t in tasklists):
            return JsonResponse(
                {"success": False, "error": "Columnas de distintos boards"},
                status=400
            )

        # Validar permisos
        if not board.user_has_access(request.user):
            return JsonResponse(
                {"success": False, "error": "No tienes permiso"},
                status=403
            )

        # Reordenar
        with transaction.atomic():
            for item in data:
                tasklist = tasklists.get(id=item["id"])
                tasklist.position = item["order"]
                tasklist.save()

        return JsonResponse({"success": True})
    except Exception as e:
        return JsonResponse(
            {"success": False, "error": str(e)},
            status=400
        )