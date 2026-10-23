# %% [markdown]
# # Análise Diagnóstica - Câncer de Mama

# %%
# ==========================================
# 1. IMPORTAÇÃO DAS BIBLIOTECAS E CONFIGURAÇÃO
# ==========================================
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configurações visuais
sns.set_theme(style="whitegrid")
pd.set_option('display.max_columns', None)

# %%
# ==========================================
# 2. CARREGAMENTO E INSPEÇÃO INICIAL DA BASE
# ==========================================
caminho_arquivo = "../data/BreastCancer.csv" if os.path.exists("../data/BreastCancer.csv") else "data/BreastCancer.csv"
df = pd.read_csv(caminho_arquivo)

print("--- 5 PRIMEIRAS LINHAS ---")
display(df.head())

print("\n--- ESTRUTURA E TIPOS DE DADOS ---")
df.info()

print(f"\nDimensão da base: {df.shape[0]} linhas e {df.shape[1]} colunas.")

# %%
# ==========================================
# 3. VERIFICAÇÃO DE VALORES NULOS E DUPLICADOS
# ==========================================
print("\n--- VALORES AUSENTES POR COLUNA ---")
nulos = df.isnull().sum()
print(nulos[nulos > 0] if nulos.sum() > 0 else "Nenhum valor ausente encontrado.")

print(f"\nLinhas duplicadas identificadas: {df.duplicated().sum()}")

# %%
# ==========================================
# 4. ESTATÍSTICAS DESCRITIVAS
# ==========================================
print("\n--- ESTATÍSTICAS DESCRITIVAS DAS VARIÁVEIS NUMÉRICAS ---")
display(df.describe().T)

# %%
# ==========================================
# 5. IDENTIFICAÇÃO E ANÁLISE DA VARIÁVEL ALVO (TARGET)
# ==========================================
# Busca automática da coluna de diagnóstico/classe
colunas_possiveis = ['diagnosis', 'Class', 'target', 'outcome', 'Class_or_target']
coluna_alvo = [col for col in df.columns if col in colunas_possiveis or col.lower() in colunas_possiveis]

if coluna_alvo:
    alvo = coluna_alvo[0]
    print(f"\n--- DISTRIBUIÇÃO DA VARIÁVEL ALVO: '{alvo}' ---")
    print(df[alvo].value_counts(normalize=True) * 100)

    plt.figure(figsize=(6, 4))
    sns.countplot(data=df, x=alvo, palette="Set2")
    plt.title(f"Distribuição dos Diagnósticos ({alvo})")
    plt.xlabel("Diagnóstico")
    plt.ylabel("Frequência")
    plt.show()

# %%
# ==========================================
# 6. ANÁLISE DE CORRELAÇÃO (HEATMAP)
# ==========================================
# Filtra variáveis numéricas e remove IDs não informativos se existirem
df_numeric = df.select_dtypes(include=[np.number])
colunas_para_remover = [col for col in ['id', 'Id', 'Sample_code_number', 'Unnamed: 32'] if col in df_numeric.columns]
df_numeric = df_numeric.drop(columns=colunas_para_remover)

plt.figure(figsize=(12, 8))
matriz_correlacao = df_numeric.corr()
sns.heatmap(matriz_correlacao, annot=False, cmap="coolwarm", linewidths=0.5)
plt.title("Matriz de Correlação das Características Numéricas")
plt.show()

# %%
# ==========================================
# 7. DISTRIBUIÇÃO DAS PRINCIPAIS CARACTERÍSTICAS
# ==========================================
# Histogramas das 6 primeiras variáveis numéricas para avaliação de assimetria/outliers
colunas_grafico = [c for c in df_numeric.columns if c not in colunas_possiveis][:6]

fig, axes = plt.subplots(2, 3, figsize=(15, 8))
axes = axes.flatten()

for i, col in enumerate(colunas_grafico):
    sns.histplot(data=df, x=col, hue=alvo if 'alvo' in locals() and alvo in df.columns else None, 
                 kde=True, ax=axes[i], palette="Set1")
    axes[i].set_title(f"Distribuição: {col}")

plt.tight_layout()
plt.show()
