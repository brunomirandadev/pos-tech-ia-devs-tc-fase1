# Usa uma imagem oficial e leve do Python
FROM python:3.9-slim

# Define a pasta de trabalho principal dentro do container
WORKDIR /app

# Copia todos os arquivos da sua pasta atual para dentro do container
COPY . /app

# Atualiza o pip e instala as dependências listadas no requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Expõe a porta caso queira rodar o Jupyter Notebook via container (opcional)
EXPOSE 8888

# Comando padrão que será executado quando o container subir 
# (Aqui deixamos pronto para abrir o Jupyter, ou você pode alterar para rodar um script python específico)
CMD ["jupyter", "notebook", "--ip='0.0.0.0'", "--port=8888", "--no-browser", "--allow-root"]
