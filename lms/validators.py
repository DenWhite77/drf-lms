from django.core.exceptions import ValidationError
from urllib.parse import urlparse


class YoutubeLinkValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        # Если пришел словарь (при использовании в Meta), берем значение поля
        if isinstance(value, dict):
            value = value.get(self.field)

        if not value:
            return

        parsed = urlparse(value)
        allowed_domains = ['youtube.com', 'www.youtube.com', 'youtu.be']

        if parsed.netloc not in allowed_domains:
            raise ValidationError(
                f'Ссылка в поле "{self.field}" должна вести только на youtube.com. '
                f'Сторонние ресурсы запрещены.'
            )
