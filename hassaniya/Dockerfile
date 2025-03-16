FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# Commande pour démarrer le serveur Django
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "hassaniya.wsgi:application"]
