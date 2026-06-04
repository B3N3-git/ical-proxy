FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

# Gunicorn explizit anweisen, Logs auf stdout (mittels -) auszugeben
CMD ["gunicorn", "--bind", "0.0.0.0:44444", "--access-logfile", "/dev/null", "app:app"]