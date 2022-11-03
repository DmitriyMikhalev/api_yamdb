from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail

from api_yamdb.settings import EMAIL_SENDER

User = get_user_model()


def send_verify_code(user: User) -> None:
    """Send verification code for signup procedure from setting.EMAIL_SENDER
    mail.
    """
    confirmation_code = default_token_generator.make_token(user=user)
    send_mail(
        from_email=EMAIL_SENDER,
        message=(
            'Спасибо за регистрацию!'
            + f'\n{confirmation_code} — ваш код подтверждения.'
        ),
        recipient_list=[user.email],
        subject='Verification code YaMDb'
    )
