# persons/views/test_email.py
from django.core.mail import send_mail
from django.http import HttpResponse


def test_email_view(request):
    send_mail(
        "Test Email",
        "This is a test message.",
        "from@example.com",
        ["to@example.com"],
        fail_silently=False,
    )
    return HttpResponse("Email sent (to console)")
