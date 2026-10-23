# Usa uma imagem oficial e leve do Python
FROM python:3.13-slim

# Define a pasta de trabalho principal dentro do container
WORKDIR /app

COPY requirements.txt /app/requirements.txt

# Atualiza o pip e instala as dependências listadas no requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

RUN useradd --create-home --uid 1000 app && \
    chown app:app /app

COPY --chown=app:app . /app

USER app
ENV HOME=/home/app

# Expõe a porta caso queira rodar o Jupyter Notebook via container (opcional)
EXPOSE 8888

# Comando padrão que será executado quando o container subir 
# (Aqui deixamos pronto para abrir o Jupyter, ou você pode alterar para rodar um script python específico)
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser"]
