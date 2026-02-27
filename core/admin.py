from django.contrib import admin
from .models import Board, TaskList, Task, Label

# Register your models here.
@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    list_display = ("name", "color")
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "tasklist", "assigned_to", "priority", "due_date", "completed", "position")
    list_filter = ("priority", "completed", "due_date", "labels")
    search_fields = ("title", "description")
    filter_horizontal = ("labels",)
    ordering = ("tasklist", "position")


@admin.register(TaskList)
class TaskListAdmin(admin.ModelAdmin):
    list_display = ("title", "board", "position")
    search_fields = ("title",)
    ordering = ("board", "position")


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ("name", "created_by", "created_at")
    search_fields = ("name",)
    list_filter = ("created_at",)
    filter_horizontal = ("members",)
    ordering = ("-created_at",)