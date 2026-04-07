# 1. On part d'une image python officielles (la base)
From python:3.11-slim

# 2. On dit a docker qu'on va travailler dans l'app
WORKDIR /app

#3. On copie d'abord requirements.txt (pour le cache)
COPY requirements.txt .

# 4. On installe les dependances
RUN pip install --no-cache-dir -r requirements.txt

# 5. On copie tous le reste du code
COPY . .

# 6. On expose le port 8000 (celui de FastAPI)
EXPOSE 8000

# 7. La commande a lance quand le contenaire demarre
CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]