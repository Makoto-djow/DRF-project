import re

from rest_framework.exceptions import ValidationError


class YouTubeLinkOnlyValidator:
    regex = re.compile(r"\b(?!https?://(?:www\.)?youtube\.com)https?://(?:www\.)?\S+\b")

    def __init__(self, fields):
        self.fields = fields

    def __call__(self, value):
        for field_name in self.fields:
            field = value.get(field_name, '')
            if self.regex.findall(field):
                raise ValidationError('в учебном материале указан ресурс, '
                                      'не соответствующий требованиям платформы.')
