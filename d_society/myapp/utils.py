def send_confirmation_email(user_email):
    from django.core.mail import send_mail
    send_mail(
        'Confirm your registration',
        'Click the link to confirm your registration.',
        'your-email@gmail.com',
        [user_email],
        fail_silently=False,
    )