# --- Build Stage ---
FROM python:3.11-slim as builder

WORKDIR /app

# Copia apenas o requirements para cache de build
COPY requirements.txt .

# Instala dependências localmente
RUN pip install --user --upgrade pip \
    && pip install --user -r requirements.txt

# --- Final Stage ---
FROM python:3.11-slim

WORKDIR /app

# Copia todo o código do projeto
COPY . .

# Copia dependências do builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Expõe porta 8000
EXPOSE 8000


# Comando final
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
