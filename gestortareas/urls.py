"""
URL configuration for gestortareas project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from core.views import (
    home,
    dashboard,
    register_view,
    BoardListView,
    BoardCreateView,
    BoardDetailView,
    BoardUpdateView,
    BoardDeleteView,
    export_board_tasks_csv,    
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    TaskListCreateView,
    move_task,
    reorder_tasklists,
    ProfileUpdateView
)  

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),

    path("login/", auth_views.LoginView.as_view(template_name="auth/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("register/", register_view, name="register"),
    path('profile/', ProfileUpdateView.as_view(), name='profile'),

    path("boards/", BoardListView.as_view(), name="board_list"),
    path("boards/create/", BoardCreateView.as_view(), name="board_create"),
    path("boards/<int:pk>/", BoardDetailView.as_view(), name="board_detail"),
    path("boards/<int:pk>/edit/", BoardUpdateView.as_view(), name="board_update"),
    path("boards/<int:pk>/delete/", BoardDeleteView.as_view(), name="board_delete"),
    path("boards/<int:board_id>/export/", export_board_tasks_csv, name="board_export_csv"),

    path("tasklist/<int:tasklist_id>/task/create/", TaskCreateView.as_view(), name="task_create"),
    path("boards/<int:board_id>/tasklist/create/", TaskListCreateView.as_view(), name="tasklist_create"),
    path("tasklist/reorder/", reorder_tasklists, name="reorder_tasklists"),

    path("tasks/<int:task_id>/move/", move_task, name="move_task"),
    path("tasks/<int:pk>/update/", TaskUpdateView.as_view(), name="task_update"),
    path("tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task_delete"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
