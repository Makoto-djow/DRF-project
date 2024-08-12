FROM python:3.12

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip install --upgrade pip \
    && pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-root

COPY . .

CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]