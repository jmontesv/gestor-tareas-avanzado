from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from core.models import Board, Task
from django.db.models import Q
from django.urls import reverse_lazy
from core.forms import TaskForm
from django.db import models
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
import csv
from django.contrib.auth.decorators import login_required

# Vista para listar los tableros del usuario
class BoardListView(LoginRequiredMixin, ListView):
    model = Board
    template_name = "boards/list.html"  
    context_object_name = "boards"

    def get_queryset(self):
        # Solo boards donde el usuario es miembro o creador
        return Board.objects.filter(
            Q(members=self.request.user) | Q(created_by=self.request.user)
        ).distinct()

# Vista para crear un nuevo tablero
class BoardCreateView(LoginRequiredMixin, CreateView):
    model = Board
    fields = ['name', 'members']
    template_name = "boards/create.html"
    success_url = reverse_lazy('board_list')

    def form_valid(self, form):
        # Asignar automáticamente el usuario que crea el board
        form.instance.created_by = self.request.user
        response = super().form_valid(form)

        # Asegurarse que el creador también sea miembro
        if self.request.user not in form.instance.members.all():
            form.instance.members.add(self.request.user)

        return response

# Vista para mostrar los detalles de un tablero
class BoardDetailView(LoginRequiredMixin, DetailView):
    model = Board
    template_name = "boards/detail.html"
    context_object_name = "board"

    def get_queryset(self):
        # Solo boards que el usuario puede ver
        return Board.objects.filter(
            Q(created_by=self.request.user) |
            Q(members=self.request.user)
        ).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pasamos el formulario vacío para el modal
        context['task_form'] = TaskForm()
         
        tasklists = self.object.tasklists.all().prefetch_related(
            models.Prefetch(
                "task",
                queryset=Task.objects.order_by("position")
            )
        )

        context["tasklists"] = tasklists
        return context

# Vista para actualizar un tablero (solo el creador puede hacerlo) 
class BoardUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Board
    fields = ['name', 'members']
    template_name = "boards/board_form.html"

    def test_func(self):
        board = self.get_object()
        return self.request.user == board.created_by

    def get_success_url(self):
        return reverse_lazy('board_detail', kwargs={'pk': self.object.pk})

# Vista para eliminar un tablero (solo el creador puede hacerlo) 
class BoardDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Board
    template_name = "boards/board_confirm_delete.html"
    success_url = reverse_lazy('board_list')

    def test_func(self):
        board = self.get_object()
        return self.request.user == board.created_by

# Vista para exportar las tareas de un tablero a CSV
@login_required
def export_board_tasks_csv(request, board_id):

    board = get_object_or_404(
        Board.objects.filter(
            Q(created_by=request.user) |
            Q(members=request.user)
        ).distinct(),
        id=board_id
    )

    # Crear respuesta tipo CSV
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f'attachment; filename="{board.name}_tasks.csv"'

    writer = csv.writer(response)

    # Cabeceras
    writer.writerow([
        "Board",
        "Columna",
        "Título",
        "Descripción",
        "Completada",
        "Asignado a",
        "Posición",
        "Fecha creación",
    ])

    tasks = Task.objects.filter(
        tasklist__board=board
    ).select_related("tasklist", "assigned_to")

    for task in tasks:
        writer.writerow([
            board.name,
            task.tasklist.title,
            task.title,
            task.description,
            "Sí" if task.completed else "No",
            task.assigned_to.username if task.assigned_to else "",
            task.position,
            task.created_at.strftime("%Y-%m-%d %H:%M"),
        ])

    return response