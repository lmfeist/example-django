FROM python:3.13.8-alpine3.22 AS builder

WORKDIR /app

RUN python3 -m venv venv
ENV VIRTUAL_ENV=/app/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt

# Stage 2
FROM python:3.13.8-alpine3.22 AS runner

ENV VIRTUAL_ENV=/app/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV PORT=8000

WORKDIR /app

COPY --from=builder /app/venv venv
COPY example_django example_django
COPY static static
COPY manage.py manage.py

EXPOSE ${PORT}

CMD uvicorn example_django.asgi:application --host 0.0.0.0 --port ${PORT}
