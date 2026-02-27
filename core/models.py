from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Board(models.Model):
    name = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="boards_created")
    members = models.ManyToManyField(User, related_name="boards")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def user_has_access(self, user):
        return (
            user == self.created_by or
            self.members.filter(id=user.id).exists()
        )

class TaskList(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="tasklists")
    title = models.CharField(max_length=100)
    position = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["position"]

    def __str__(self):
        return f"{self.board.name} - {self.title}"

class Label(models.Model):
    name = models.CharField(max_length=50, unique=True)
    color = models.CharField(
        max_length=20,
        default="gray",
        help_text="Color hex, ej: #ff0000 o nombre de color"
    )

    def __str__(self):
        return self.name


class Task(models.Model):
    PRIORITY_CHOICES = [
        ("low", "Baja"),
        ("medium", "Media"),
        ("high", "Alta"),
    ]

    tasklist = models.ForeignKey(TaskList, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="tasks")
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default="medium")
    labels = models.ManyToManyField(Label, blank=True, related_name="tasks")
    due_date = models.DateField(null=True, blank=True)
    position = models.PositiveIntegerField(default=0) 
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    class Meta:
        ordering = ["position"]

    def __str__(self):
        return self.title
    


