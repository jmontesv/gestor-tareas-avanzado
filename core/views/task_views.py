from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from core.models import Task, TaskList
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.db import transaction
import json
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from core.services.notifications import send_task_assigned_email

# Vista para crear una nueva tarea dentro de una columna específica
class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'assigned_to', 'priority', 'labels', 'due_date']

    def dispatch(self, request, *args, **kwargs):
        """
        Sobrescribimos dispatch para asegurar que la columna exista y el usuario tenga acceso
        """
        self.tasklist = get_object_or_404(TaskList, pk=self.kwargs['tasklist_id'])

        # Comprobar que el usuario es miembro del board de la columna
        if not self.tasklist.board.user_has_access(request.user):
            return HttpResponseForbidden("No tienes acceso a esta columna")
        
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        """Retorna el formulario vacío para crear una tarea (usado en el modal)"""
        form = self.get_form()
        html = render_to_string(
            "tasks/task_form.html",
            {"form": form},
            request=request
        )
        return JsonResponse({"html": html})

    def form_valid(self, form):
        """Cuando el formulario es válido, asignamos la columna y la posición antes de guardar"""
        
        # Asignar columna
        form.instance.tasklist = self.tasklist

        # Posición al final
        last_task = self.tasklist.tasks.order_by('-position').first()
        form.instance.position = (last_task.position + 1) if last_task else 0

          
        self.object = form.save()
        
        if self.object.assigned_to:
            send_task_assigned_email(self.object)
        

        return JsonResponse({
            "success": True,
            "task": {
                "id": self.object.id,
                "title": self.object.title,
                "tasklist_id": self.tasklist.id,
            }
        })
    
    def form_invalid(self, form):
        html = render_to_string(
            "tasks/task_form.html",
            {"form": form},
            request=self.request
        )
        return JsonResponse({"html": html})

# Vista para mover una tarea a otra columna (drag & drop)
@login_required
@require_POST
def move_task(request, task_id):
    """
    Mueve una tarea a otra columna y reordena las tareas según el frontend.
    Valida que el usuario tenga acceso tanto a la tarea original como a la columna destino.
    """
    try:
        data = json.loads(request.body)
        new_tasklist_id = data.get("tasklist_id")
        new_order = data.get("order", [])

        # Obtener la tarea original
        task = get_object_or_404(
            Task.objects.select_related("tasklist__board"),
            id=task_id
        )
        if not task.tasklist.board.user_has_access(request.user):
            return JsonResponse(
                {"success": False, "error": "No tienes permiso para mover esta tarea"},
                status=403
            )

        # Obtener la columna destino
        new_tasklist = get_object_or_404(TaskList.objects.select_related("board"), id=new_tasklist_id)
        if not new_tasklist.board.user_has_access(request.user):
            return JsonResponse(
                {"success": False, "error": "No tienes permiso para mover tareas a esta columna"},
                status=403
            )

        # Transacción atómica: mover tarea y reordenar destino
        with transaction.atomic():
            task.tasklist = new_tasklist
            task.save()

            for item in new_order:
                t = Task.objects.select_related("tasklist__board").filter(id=item["id"]).first()
                if t and t.tasklist.board.user_has_access(request.user):
                    t.position = item["order"]
                    t.save()

        return JsonResponse({"success": True})

    except json.JSONDecodeError:
        return JsonResponse({"success": False, "error": "JSON inválido"}, status=400)
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)

# Vista para obtener el formulario de edición de una tarea (usado en el modal)
class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'completed', 'assigned_to', 'priority', 'labels', 'due_date']

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        # Comprobar que el usuario es miembro del board de la tarea
        if not self.object.tasklist.board.user_has_access(request.user):
            return HttpResponseForbidden("No tienes acceso a editar esta tarea")

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.get_form()
        html = render_to_string(
            "tasks/task_form.html",
            {
                "form": form,
                "task": form.instance
            },
            request=request
        )
        return JsonResponse({"html": html})

    def form_valid(self, form):
        # Obtener estado anterior
        old_task = Task.objects.get(pk=self.get_object().pk)
        old_assigned = old_task.assigned_to

        # Guardar cambios
        self.object = form.save()

        new_assigned = self.object.assigned_to

        # Enviar email solo si cambió el asignado
        if (
            new_assigned
            and new_assigned != old_assigned
            and new_assigned != self.request.user 
        ):
            send_task_assigned_email(self.object)

        return JsonResponse({
            "success": True,
            "task": {
                "id": self.object.id,
                "title": self.object.title,
                "tasklist_id": self.object.tasklist_id,
            }
        })

    def form_invalid(self, form):
        html = render_to_string(
            "tasks/task_form.html",
            {
                "form": form,
                "task": form.instance 
            },
            request=self.request
        )
        return JsonResponse({"html": html})

# Vista para eliminar una tarea (usado en el modal)
class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task

    def dispatch(self, request, *args, **kwargs):
        self.task = get_object_or_404(Task, pk=kwargs["pk"])
        board = self.task.tasklist.board
        
        # Comprobar que el usuario es miembro del board de la tarea
        if not board.user_has_access(request.user):
            return HttpResponseForbidden("No tienes acceso a eliminar esta tarea")

        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        task_id = self.task.id
        self.task.delete()
        return JsonResponse({"success": True, "task_id": task_id})