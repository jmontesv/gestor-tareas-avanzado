from django.shortcuts import render, redirect
from core.models import Board, Task, Profile
from django.db.models import Q
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from core.forms import CustomUserCreationForm

# Vista para la página de inicio (landing page)
def home(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    return render(request, "landing.html")

# Vista para el dashboard principal
@login_required
def dashboard(request):
    # Boards donde el usuario es creador o miembro
    boards = Board.objects.filter(
        Q(created_by=request.user) | Q(members=request.user)
    ).distinct()

    boards_with_progress = []

    total_tasks_global = 0
    completed_tasks_global = 0

    for board in boards:

        # Todas las tareas del board
        tasks = Task.objects.filter(tasklist__board=board)

        total_tasks = tasks.count()
        completed_tasks = tasks.filter(completed=True).count()

        progress = int((completed_tasks / total_tasks) * 100) if total_tasks > 0 else 0

        total_tasks_global += total_tasks
        completed_tasks_global += completed_tasks

        boards_with_progress.append({
            "board": board,
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "progress": progress,
        })

    context = {
        "boards_with_progress": boards_with_progress,
        "total_tasks_global": total_tasks_global,
        "completed_tasks_global": completed_tasks_global,
    }

    return render(request, "home.html", context)

# Vista para registro de usuarios
def register_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            login(request, user) 
            return redirect("home")
    else:
        form = CustomUserCreationForm()

    return render(request, "auth/register.html", {"form": form})