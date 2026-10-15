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

- Python 3.9
- Pandas & NumPy (Manipulação e análise de dados)
- Matplotlib & Seaborn (Visualização de dados e gráficos)
- Scikit-Learn (Modelagem preditiva e métricas de avaliação)
- Docker (Empacotamento e isolamento do ambiente com Jupyter Notebook)

## 🚀 Como Executar o Container e Acessar o Projeto

Para garantir a reprodutibilidade exata do ambiente de desenvolvimento, o projeto utiliza Docker para rodar um container isolado contendo o Jupyter Notebook.

### Pré-requisitos Importantes

- O Docker Desktop precisa estar instalado e aberto/rodando na sua máquina (verifique se o ícone na barra de tarefas está ativo).
- Certifique-se de que o seu arquivo `requirements.txt` utiliza o pacote de ambiente correto (ex: `notebook>=6.5.0`).

### Passo a passo detalhado para execução

1. Clone o repositório em sua máquina:

	```bash
	git clone https://github.com/SEU-USUARIO/tech-challenge-fase1-ia-devs.git
	cd tech-challenge-fase1-ia-devs
	```

2. Construa a imagem Docker:

	Abra o seu terminal na pasta raiz do projeto e execute o comando abaixo para compilar a imagem (a flag `--no-cache` garante uma instalação limpa):

	```bash
	docker build --no-cache -t tech-challenge-fase1 .
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