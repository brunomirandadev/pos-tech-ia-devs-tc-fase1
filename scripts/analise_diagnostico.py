# %% [markdown]
# # Tech Challenge - Fase 1: Diagnóstico Assistido por Inteligência Artificial
# ## Análise Preditiva e Triagem de Câncer de Mama (*Wisconsin Diagnostic Breast Cancer*)
#
# ### Bloco 1: Contextualização do Problema Hospitalar
# Nos departamentos de oncologia e patologia hospitalar, a análise citopatológica detalhada de biópsias
# por punção aspirativa por agulha fina (PAAF) pode gerar gargalos no fluxo de atendimento.
# A IA atua como um Sistema de Suporte à Decisão Clínica (CDSS) para triagem automatizada, priorização
# de exames suspeitos e segunda opinião quantitativa, reduzindo o risco de falsos negativos.
#
# *Diretriz Ética:* A decisão e o laudo definitivo cabem sempre e exclusivamente ao médico especialista.

# %%
# ==========================================
# 1. IMPORTAÇÃO DAS BIBLIOTECAS E CONFIGURAÇÃO
# ==========================================
import os
from pathlib import Path
from IPython.display import display
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Scikit-Learn: Pré-processamento, Modelagem e Métricas
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_curve, roc_auc_score
)

# Configurações visuais
sns.set_theme(style="whitegrid", palette="muted")
pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', lambda x: '%.4f' % x)
plt.rcParams['figure.dpi'] = 100

# %%
# ==========================================
# 2. CARREGAMENTO E INSPEÇÃO INICIAL DA BASE
# ==========================================
caminhos_possiveis = [
    Path("../data/BreastCancer.csv"),
    Path("data/BreastCancer.csv"),
    Path(__file__).resolve().parent.parent / "data" / "BreastCancer.csv" if "__file__" in locals() else None
]

caminho_arquivo = next((p for p in caminhos_possiveis if p is not None and p.exists()), Path("data/BreastCancer.csv"))
df = pd.read_csv(caminho_arquivo)

print(f"Base carregada com sucesso de: {caminho_arquivo}")
print(f"Dimensão inicial: {df.shape[0]} amostras e {df.shape[1]} colunas.\n")

print("--- 5 PRIMEIRAS LINHAS ---")
display(df.head())

# %%
# ==========================================
# 3. ANÁLISE EXPLORATÓRIA DE DADOS (EDA)
# ==========================================
print("--- ESTRUTURA E TIPOS DE DADOS ---")
df.info()

print("\n--- VALORES AUSENTES POR COLUNA ---")
nulos = df.isnull().sum()
display(nulos[nulos > 0] if nulos.sum() > 0 else "Nenhum valor ausente encontrado.")

print(f"Linhas duplicadas identificadas: {df.duplicated().sum()}")

# %%
# 3.1. Estatísticas descritivas
print("\n--- ESTATÍSTICAS DESCRITIVAS ---")
display(df.describe().T)

# %%
# 3.2. Distribuição da variável alvo
contagem = df['diagnosis'].value_counts()
percentual = df['diagnosis'].value_counts(normalize=True) * 100

resumo_alvo = pd.DataFrame({'Total': contagem, 'Percentual (%)': percentual})
print("\n--- DISTRIBUIÇÃO DA VARIÁVEL ALVO (diagnosis) ---")
display(resumo_alvo)

fig, ax = plt.subplots(figsize=(6, 4))
sns.countplot(data=df, x='diagnosis', hue='diagnosis', order=['B', 'M'], hue_order=['B', 'M'], palette=['#2b5c8f', '#d95f02'], legend=False, ax=ax)
ax.set_title("Distribuição dos Diagnósticos (B = Benigno | M = Maligno)", fontsize=12, fontweight='bold')
ax.set_xlabel("Diagnóstico Clínico")
ax.set_ylabel("Total de Casos")
ax.set_xticks([0, 1])
ax.set_xticklabels(["Benigno (B)", "Maligno (M)"])

for p in ax.patches:
    altura = int(p.get_height())
    ax.annotate(f"{altura} ({altura / len(df) * 100:.1f}%)",
                (p.get_x() + p.get_width() / 2., altura / 2),
                ha='center', va='center', color='white', fontweight='bold')

plt.tight_layout()
plt.show()

# %%
# 3.3. Matriz de correlação
df_numeric = df.select_dtypes(include=[np.number])
colunas_ignorar = [c for c in ['id', 'Id', 'Unnamed: 32'] if c in df_numeric.columns]
df_numeric_clean = df_numeric.drop(columns=colunas_ignorar)

plt.figure(figsize=(14, 10))
corr = df_numeric_clean.corr()
mask = np.triu(np.ones_like(corr, dtype=bool))
sns.heatmap(corr, mask=mask, cmap="coolwarm", center=0, linewidths=0.5, annot=False)
plt.title("Matriz de Correlação das Características Numéricas do Núcleo Celular", fontsize=13, fontweight='bold')
plt.tight_layout()
plt.show()

# %%
# 3.4. Distribuição das principais variáveis por diagnóstico
colunas_grafico = ['radius_mean', 'texture_mean', 'perimeter_mean', 'area_mean', 'smoothness_mean', 'concavity_mean']

fig, axes = plt.subplots(2, 3, figsize=(16, 8))
axes = axes.flatten()

for i, col in enumerate(colunas_grafico):
    sns.histplot(data=df, x=col, hue='diagnosis', kde=True, ax=axes[i], palette=['#d95f02', '#2b5c8f'], stat="density")
    axes[i].set_title(f"Distribuição: {col}", fontweight='bold')
    axes[i].set_xlabel("")

plt.suptitle("Histogramas de Características Morfológicas (Maligno vs. Benigno)", fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()

# %%
# ==========================================
# 4. PRÉ-PROCESSAMENTO E PREPARAÇÃO DOS DADOS
# ==========================================
colunas_para_remover = [c for c in ['id', 'Id', 'Unnamed: 32'] if c in df.columns]
df_model = df.drop(columns=colunas_para_remover).copy()

# Mapeamento do alvo: M -> 1, B -> 0
df_model['target'] = df_model['diagnosis'].map({'M': 1, 'B': 0})
X = df_model.drop(columns=['diagnosis', 'target'])
y = df_model['target']

print(f"Matriz de Características (X): {X.shape[0]} amostras, {X.shape[1]} atributos")
print(f"Vetor de Alvo (y): {y.shape[0]} rótulos")

# Divisão Treino e Teste com Estratificação (80/20)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

print(f"Conjunto de Treino: {X_train.shape[0]} amostras ({y_train.sum()} malignos, {len(y_train) - y_train.sum()} benignos)")
print(f"Conjunto de Teste:  {X_test.shape[0]} amostras ({y_test.sum()} malignos, {len(y_test) - y_test.sum()} benignos)")

# Normalização de Escala (StandardScaler)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
print("Padronização concluída com sucesso!")

# %%
# ==========================================
# 5. MODELAGEM PREDITIVA (TREINAMENTO)
# ==========================================
# 1. Regressão Logística
modelo_lr = LogisticRegression(max_iter=1000, random_state=42)
modelo_lr.fit(X_train_scaled, y_train)

# 2. Árvore de Decisão
modelo_dt = DecisionTreeClassifier(max_depth=4, min_samples_split=5, random_state=42)
modelo_dt.fit(X_train, y_train)

print("Modelos de Regressão Logística e Árvore de Decisão treinados com sucesso!")

# %%
# ==========================================
# 6. AVALIAÇÃO DE MÉTRICAS E COMPARAÇÃO
# ==========================================
y_pred_lr = modelo_lr.predict(X_test_scaled)
y_proba_lr = modelo_lr.predict_proba(X_test_scaled)[:, 1]

y_pred_dt = modelo_dt.predict(X_test)
y_proba_dt = modelo_dt.predict_proba(X_test)[:, 1]

metricas = {
    "Acurácia": [accuracy_score(y_test, y_pred_lr), accuracy_score(y_test, y_pred_dt)],
    "Precisão": [precision_score(y_test, y_pred_lr), precision_score(y_test, y_pred_dt)],
    "Recall (Sensibilidade)": [recall_score(y_test, y_pred_lr), recall_score(y_test, y_pred_dt)],
    "F1-Score": [f1_score(y_test, y_pred_lr), f1_score(y_test, y_pred_dt)],
    "ROC-AUC": [roc_auc_score(y_test, y_proba_lr), roc_auc_score(y_test, y_proba_dt)]
}

df_metricas = pd.DataFrame(metricas, index=["Regressão Logística", "Árvore de Decisão"])
print("\n--- COMPARATIVO DE MÉTRICAS (CONJUNTO DE TESTE) ---")
display(df_metricas)

# %%
# 6.1. Matrizes de Confusão
fig, axes = plt.subplots(1, 2, figsize=(13, 5))

cm_lr = confusion_matrix(y_test, y_pred_lr)
sns.heatmap(cm_lr, annot=True, fmt='d', cmap='Blues', cbar=False, ax=axes[0],
            xticklabels=['Benigno (0)', 'Maligno (1)'], yticklabels=['Benigno (0)', 'Maligno (1)'])
axes[0].set_title(f"Regressão Logística\nAcurácia: {df_metricas.loc['Regressão Logística', 'Acurácia']:.2%}", fontweight='bold')
axes[0].set_xlabel("Predição do Modelo")
axes[0].set_ylabel("Diagnóstico Real")

cm_dt = confusion_matrix(y_test, y_pred_dt)
sns.heatmap(cm_dt, annot=True, fmt='d', cmap='Greens', cbar=False, ax=axes[1],
            xticklabels=['Benigno (0)', 'Maligno (1)'], yticklabels=['Benigno (0)', 'Maligno (1)'])
axes[1].set_title(f"Árvore de Decisão\nAcurácia: {df_metricas.loc['Árvore de Decisão', 'Acurácia']:.2%}", fontweight='bold')
axes[1].set_xlabel("Predição do Modelo")
axes[1].set_ylabel("Diagnóstico Real")

plt.tight_layout()
plt.show()

print("\n--- CLASSIFICATION REPORT: REGRESSÃO LOGÍSTICA ---")
print(classification_report(y_test, y_pred_lr, target_names=['Benigno', 'Maligno']))

print("\n--- CLASSIFICATION REPORT: ÁRVORE DE DECISÃO ---")
print(classification_report(y_test, y_pred_dt, target_names=['Benigno', 'Maligno']))

# %%
# ==========================================
# 7. IMPORTÂNCIA DAS VARIÁVEIS (FEATURE IMPORTANCE)
# ==========================================
importancias_dt = pd.Series(modelo_dt.feature_importances_, index=X.columns)
top_dt = importancias_dt[importancias_dt > 0].sort_values(ascending=True)

coef_lr = pd.Series(np.abs(modelo_lr.coef_[0]), index=X.columns).sort_values(ascending=True).tail(10)

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

top_dt.plot(kind='barh', color='#2ca02c', ax=axes[0])
axes[0].set_title("Importância de Atributos (Árvore de Decisão - Impureza Gini)", fontweight='bold')
axes[0].set_xlabel("Importância Relativa")

coef_lr.plot(kind='barh', color='#1f77b4', ax=axes[1])
axes[1].set_title("Top 10 Características (|Coef|) na Regressão Logística", fontweight='bold')
axes[1].set_xlabel("Valor Absoluto do Coeficiente")

plt.tight_layout()
plt.show()

# %% [markdown]
# # ==========================================
# # 8. CONCLUSÕES E DIRETRIZES CLÍNICAS
# # ==========================================
# # - Regressão Logística: Alta acurácia (~96.5%) e excelente sensibilidade/recall (>92%).
# # - Árvore de Decisão: Boa acurácia (~91.2%) e alta interpretabilidade com destaque para
# #   'concave points_worst' e 'perimeter_worst'.
# #
# # AVISO ÉTICO E CLÍNICO OBRIGATÓRIO:
# # O modelo atua exclusivamente como ferramenta de triagem prévia.
# # A palavra final e o laudo definitivo cabem sempre e exclusivamente ao médico especialista.
