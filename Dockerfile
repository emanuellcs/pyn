FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP=run.py

COPY requirements.txt .

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libffi-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get purge -y --auto-remove gcc libffi-dev \
    && rm -rf /var/lib/apt/lists/*

COPY . .

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
