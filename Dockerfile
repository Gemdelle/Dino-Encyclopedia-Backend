FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el archivo .env si existe
COPY .env* ./ 

COPY . .

CMD ["python", "main.py"] 