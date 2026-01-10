from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_email_task(
    to_emails: str,
    from_email: str,
    subject: str,
    html_body: str | None,
    body: str = "",
    fail_silently: bool = False,
):
    send_mail(
        subject=subject,
        message=body,
        html_message=html_body,
        from_email=from_email,
        recipient_list=to_emails,
        fail_silently=fail_silently,
    )
