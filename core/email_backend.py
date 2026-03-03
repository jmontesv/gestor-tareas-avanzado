import resend
from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend

class ResendEmailBackend(BaseEmailBackend):
    def open(self):
        resend.api_key = settings.RESEND_API_KEY

    def close(self):
        pass

    def send_messages(self, email_messages):
        self.open()
        sent = 0
        for message in email_messages:
            try:
                params = {
                    "from": message.from_email,
                    "to": message.to,
                    "subject": message.subject,
                    "text": message.body,
                }

                for content, mimetype in getattr(message, 'alternatives', []):
                    if mimetype == 'text/html':
                        params["html"] = content
                        break

                resend.Emails.send(params)
                sent += 1
            except Exception as e:
                print(f"Error enviando email: {e}")
                if not self.fail_silently:
                    raise
        return sent