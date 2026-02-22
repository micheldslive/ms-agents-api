FROM python:3.12.1

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Criação do usuário "runuser"
RUN useradd -m -d /home/runuser -s /bin/bash runuser

# Copiar o arquivo de dependências
COPY pyproject.toml /app/

# Instalar o uv
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh
ENV PATH="/root/.local/bin/:$PATH"

# Instalar as dependências Python
RUN uv pip install --system -r pyproject.toml
COPY . /app

# Mudar a propriedade para o usuário "runuser"
RUN chown -R runuser:runuser /app && \
    chmod -R 755 /app

# Alterar para o usuário "runuser"
USER runuser

# Expor a porta
EXPOSE 8000

# Comando para rodar o servidor
CMD ["uvicorn", "app.api.server:app", "--host", "0.0.0.0", "--port", "8000"]