from celery import shared_task
from django.conf import settings
from django.core.mail import (
    get_connection,
    EmailMultiAlternatives,
)
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from subscribe.models import SubscribeProduct


@shared_task(name="daily_in_stock_report_task")
def send_daily_in_stock_report_task():
    # Get subscriptions where Products have in_stock = True for this moment
    subscriptions = SubscribeProduct.objects.filter(
        product__in_stock=True
    ).select_related("user", "product")

    if not subscriptions.exists():
        return "No products in stock for subscribers."

    # Open mail connection
    connection = get_connection()

    # Email subject
    email_subject = "Your favorite Product In Stock!"

    # Messages
    messages = []

    for sub in subscriptions:
        # Render HTML message
        html_content = render_to_string(
            template_name="subscribe/emails/product_in_stock.html",
            context={
                "user": sub.user,
                "product": sub.product,
                "domain": settings.SITE_DOMAIN,
                "protocol": "https" if settings.IS_PRODUCTION else "http",
            },
        )
        text_content = strip_tags(html_content)

        # Create message with HTML support
        email = EmailMultiAlternatives(
            subject=email_subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[sub.user.email],
            connection=connection,
        )
        email.attach_alternative(html_content, "text/html")
        messages.append(email)

    # Send all messages
    if messages:
        connection.send_messages(messages)

    return f"Sent {len(messages)} in_stock daily notifications."
