from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


def send_task_assigned_email(task):
    try:
        subject = f"Nueva tarea asignada: {task.title}"

        context = {
            "task": task,
            "board": task.tasklist.board,
            "tasklist": task.tasklist,
        }

        text_content = render_to_string("emails/task_assigned.txt", context)
        html_content = render_to_string("emails/task_assigned.html", context)

        email = EmailMultiAlternatives(
            subject,
            text_content,
            settings.DEFAULT_FROM_EMAIL,
            [task.assigned_to.email]
        )

        email.attach_alternative(html_content, "text/html")
        email.send()
    except Exception as e:
        print(f"Error enviando email: {e}")