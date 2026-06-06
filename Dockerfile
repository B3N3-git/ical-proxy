FROM python:3.12-alpine

RUN apk update && apk upgrade && rm -rf /var/cache/apk/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

CMD ["gunicorn", "--bind", "0.0.0.0:44444", "--access-logfile", "/dev/null", "app:app"]