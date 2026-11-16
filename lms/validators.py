from django.core.exceptions import ValidationError
from urllib.parse import urlparse


class YoutubeLinkValidator:
    """Проверяет, что ссылка ведет только на youtube.com или youtu.be."""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        if not value:
            return value

        parsed = urlparse(value)
        # Разрешенные домены
        allowed_domains = ['youtube.com', 'www.youtube.com', 'youtu.be']

        if parsed.netloc not in allowed_domains:
            raise ValidationError(
                f'Ссылка в поле "{self.field}" должна вести только на youtube.com. '
                f'Сторонние ресурсы запрещены.'
            )
        return value
