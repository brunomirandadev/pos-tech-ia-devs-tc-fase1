# Tech Challenge - Fase 1 | POSTECH IA for Devs (FIAP)

Repositório dedicado à entrega do **Tech Challenge da Fase 1** da pós-graduação **IA for Devs**. O projeto consiste na implementação de um sistema inteligente de suporte ao diagnóstico médico utilizando Machine Learning.

---

## 🎯 Sobre o Desafio

O objetivo principal é construir uma solução inicial com foco em IA para o processamento de exames médicos, realizando a classificação automática (maligno vs. benigno ou presença/ausência de patologia) a partir de dados tabulares estruturados, aplicando fundamentos essenciais de Ciência de Dados e Machine Learning.

---

## 📂 Estrutura do Repositório

```text
📦 tech-challenge-fase1-ia-devs
 ┣ 📂 data/                 # Pasta contendo o dataset utilizado (CSV)
 ┣ 📂 notebook/             # Jupyter Notebooks com a análise, EDA e modelagem
 ┣ 📜 Dockerfile            # Arquivo de configuração do container Docker
 ┣ 📜 requirements.txt      # Dependências e bibliotecas Python utilizadas
 ┗ 📜 README.md             # Documentação do projeto
```

## 🛠️ Tecnologias Utilizadas

- Python 3.13
- Pandas & NumPy (Manipulação e análise de dados)
- Matplotlib & Seaborn (Visualização de dados e gráficos)
- Scikit-Learn (Modelagem preditiva e métricas de avaliação)
- Docker (Empacotamento e isolamento do ambiente com Jupyter Notebook)

## Execução Local com uv (Sem Docker)

Execute os comandos abaixo no PowerShell, na raiz do projeto. O ambiente local usa Python 3.13, assim como o Dockerfile.

### Instalar o uv

```powershell
winget install --id astral-sh.uv --exact
```

Após a instalação, abra um novo terminal e confirme:

```powershell
uv --version
```

### Preparar o Python e o Ambiente Virtual

```powershell
uv python install 3.13
uv python pin 3.13
uv venv --python 3.13
uv pip install -r requirements.txt
```

O comando `uv python pin 3.13` registra a versão escolhida no arquivo `.python-version` para os comandos do uv neste projeto. Ele não altera uma venv existente nem o kernel selecionado no VS Code.

Opcionalmente, para definir o Python 3.13 como padrão do uv para o seu usuário:

```powershell
uv python pin --global 3.13
```

A opção `--global` grava a preferência na configuração do usuário do uv. Uma versão definida no projeto tem prioridade sobre essa preferência global. Isso não substitui o Python do sistema nem altera uma venv existente ou o kernel do VS Code.

O uv cria e detecta automaticamente o ambiente padrão `.venv`. Não versione essa pasta nem a inclua na imagem Docker.

Para listar os interpretadores instalados:

```powershell
uv python list --only-installed
```

### Executar o Notebook no VS Code

1. Instale as extensões **Python** e **Jupyter** da Microsoft no VS Code.
2. Abra `notebook/analise_diagnostico.ipynb`.
3. Clique em **Selecionar Kernel**, escolha **Ambientes Python** e selecione `.venv/Scripts/python.exe`. Se não aparecer, use **Python: Select Interpreter** na paleta de comandos para informar esse caminho e selecione novamente o kernel.
4. Execute as células em ordem ou use **Executar Tudo**.

O `ipykernel` já está incluído em `requirements.txt`. Ativar uma venv no terminal não altera automaticamente o kernel do notebook.

Para confirmar o interpretador e a disponibilidade do kernel:

```powershell
uv pip check
.\.venv\Scripts\python.exe -c "import sys, ipykernel; print(sys.executable); print(sys.version)"
```

### Executar o Jupyter no Navegador

```powershell
.\.venv\Scripts\jupyter.exe notebook
```

Abra a URL com token exibida no terminal. Para encerrar o servidor, use `Ctrl+C` no mesmo terminal.

## 🚀 Como Executar o Container e Acessar o Projeto

O projeto utiliza Docker para rodar um container isolado contendo o Jupyter Notebook. As dependências diretas têm versões fixadas em `requirements.txt`; a reprodução exata ainda depende de fixar as dependências transitivas e a imagem base por digest.

O Jupyter executa como usuário sem privilégios (`app`). As dependências são instaladas no Python da imagem durante o build, e a `.venv` local é excluída pelo `.dockerignore`.

### Pré-requisitos Importantes

- O Docker Desktop precisa estar instalado e aberto/rodando na sua máquina (verifique se o ícone na barra de tarefas está ativo).
- Mantenha o arquivo `requirements.txt` disponível na raiz do projeto para a instalação das dependências.

### Passo a passo detalhado para execução

1. Clone o repositório em sua máquina:

	```bash
	git clone https://github.com/brunomirandadev/pos-tech-ia-devs-tc-fase1.git
	cd tech-challenge-fase1-ia-devs
	```

2. Construa a imagem Docker:

	Abra o seu terminal na pasta raiz do projeto e execute o comando abaixo. O cache da instalação das dependências é reutilizado enquanto `requirements.txt` não mudar. Use `--no-cache` apenas quando precisar reconstruir todas as camadas.

	```bash
	docker build -t tech-challenge-fase1 .
	```

3. Execute o container Docker:

	Inicie o container mapeando a porta padrão do Jupyter (8888) para a sua máquina local:

	```bash
	docker run -p 8888:8888 tech-challenge-fase1
	```

4. Acesse o ambiente pelo navegador:

	Após rodar o comando anterior, o terminal exibirá uma mensagem contendo links de acesso ao Jupyter com um token de segurança (exemplo: `http://127.0.0.1:8888/?token=abc123xyz...`).

	Copie esse link completo que apareceu no seu terminal.

	Abra o seu navegador web (Chrome, Firefox, Edge, etc.), cole o link na barra de endereços e aperte Enter.

	Pronto! O ambiente do Jupyter Notebook abrirá visualmente no seu browser.

### 💡 Comandos Úteis do Docker (Dicas de Uso)

Rodar o container em segundo plano (Modo Detached): Caso queira liberar o terminal enquanto o Jupyter roda:

```bash
docker run -d -p 8888:8888 --name container-tech-challenge tech-challenge-fase1
```

Ver os logs ou o token de acesso caso precise recuperar a URL:

```bash
docker logs container-tech-challenge
```

Parar o container:

```bash
docker stop container-tech-challenge
```

## 📊 Principais Etapas Desenvolvidas

- **Análise Exploratória de Dados (EDA):** Carregamento, inspeção de nulos/tipos, estatísticas descritivas e matriz de correlação.
- **Pré-processamento:** Tratamento de dados e divisão robusta entre conjuntos de treino e teste.
- **Modelagem Preditiva:** Treinamento de algoritmos de classificação supervisionada (Regressão Logística e Árvore de Decisão).
- **Avaliação e Métricas:** Extração de Acurácia, Recall e F1-Score, seguidas de uma discussão crítica sobre a aplicabilidade clínica da IA (enfatizando o médico sempre como o tomador de decisão final).