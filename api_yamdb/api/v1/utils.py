from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail

User = get_user_model()


def send_verify_code(user: User) -> None:
    """Send verification code for signup procedure from setting.EMAIL_SENDER
    mail.
    """
    confirmation_code = default_token_generator.make_token(user=user)
    send_mail(
        from_email=None,
        message=(
            'Спасибо за регистрацию!'
            + f'\n{confirmation_code} — ваш код подтверждения.'
        ),
        recipient_list=[user.email],
        subject='Подтвердите регистрацию на YaMDb.'
    )
