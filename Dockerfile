# 1. base image
FROM python:3.10-slim

# 2. prevent pycache, buffer logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 3. set workdir & install deps
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install -r requirements.txt

# 4. copy project
COPY . .

# 5. collect static into /app/staticfiles
RUN python manage.py collectstatic --noinput

# 6. expose port & default command
EXPOSE 8000
CMD ["gunicorn", "hirehub.wsgi:application",
     "--bind", "0.0.0.0:8000",
     "--workers", "3",
     "--log-level", "info"]
