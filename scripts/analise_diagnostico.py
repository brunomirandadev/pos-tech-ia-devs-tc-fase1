# %% [markdown]
# # Tech Challenge - Fase 1: Diagnóstico Assistido por Inteligência Artificial
# ## Análise Preditiva e Triagem de Câncer de Mama (*Wisconsin Diagnostic Breast Cancer*)
#
# ---
#
# ### Contextualização do Problema Hospitalar
# Nos departamentos de oncologia e patologia de um hospital universitário, a análise citopatológica detalhada
# de biópsias por Punção Aspirativa por Agulha Fina (PAAF) pode gerar gargalos operacionais no fluxo de atendimento.
#
# A Inteligência Artificial atua como um **Sistema de Suporte à Decisão Clínica (CDSS - *Clinical Decision Support System*)**,
# auxiliando em três frentes prioritárias:
# 1. **Triagem Automatizada e Priorização de Casos:** Identificação precoce de exames com alta suspeita de malignidade para análise imediata.
# 2. **Segunda Opinião Quantitativa:** Mitigação de viés de fadiga médica e redução máxima de falsos negativos.
# 3. **Interpretabilidade e Auditoria Clínica:** Explicabilidade total dos fatores que guiaram a predição através de técnicas como *Feature Importance* e **SHAP**.
#
# > **DIRETRIZ ÉTICA E CLÍNICA OBRIGATÓRIA:** O modelo computacional é estritamente uma ferramenta de suporte.
# > **A palavra final e o laudo diagnóstico definitivo cabem sempre e exclusivamente ao médico especialista.**

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
import shap

# Scikit-Learn: Divisão, Pipelines, Modelos e Métricas
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_curve, roc_auc_score
)

# Configurações visuais e de exibição
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
display(nulos[nulos > 0] if nulos.sum() > 0 else "Nenhum valor ausente identificado nas variáveis preditoras.")

print(f"Linhas duplicadas identificadas: {df.duplicated().sum()}")

# %%
# 3.1. Estatísticas descritivas
print("\n--- ESTATÍSTICAS DESCRITIVAS ---")
display(df.describe().T)

# %%
# 3.2. Distribuição da variável alvo (diagnosis)
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

# %% [markdown]
# ### Discussão Clínica da Distribuição do Alvo:
# Observa-se que 62.7% dos casos são benignos e 37.3% são malignos. Embora haja um desbalanceamento moderado,
# a proporção é favorável ao treinamento supervisionado, contanto que se utilize **estratificação** em todas
# as etapas de divisão dos dados para evitar sub-representação de tumores malignos em qualquer partição.

# %%
# 3.3. Matriz de correlação das características numéricas
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

# %% [markdown]
# ### Discussão dos Resultados da Matriz de Correlação:
# 1. **Multicolinearidade Acentuada:** Observa-se correlação quase perfeita (r > 0.98) entre medidas geométricas diretamente
#    interdependentes, como `radius_mean`, `perimeter_mean` e `area_mean`. O mesmo padrão se repete para os valores extremos (`_worst`).
# 2. **Impacto na Modelagem:** Em modelos lineares (como a Regressão Logística), a multicolinearidade infla a variância
#    dos coeficientes isolados. Por essa razão, a regularização L2 e técnicas de interpretabilidade aditiva como o **SHAP**
#    são fundamentais para atribuir a real importância de cada feature sem distorções causadas por correlações cruzadas.
# 3. **Indícios de Malignidade:** Características de irregularidade de contorno (`concavity_mean`, `concave points_mean`)
#    mostram forte correlação positiva com as dimensões nucleares, sugerindo que núcleos maiores também tendem a ser mais dismórficos.

# %%
# 3.4. Distribuição das principais características por diagnóstico
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

# %% [markdown]
# ### Discussão das Distribuições Morfológicas:
# - **Poder Discriminativo:** Variáveis como `radius_mean`, `area_mean` e `concavity_mean` apresentam separação visual marcante.
#   Os tumores malignos (laranja) apresentam curvas sistematicamente deslocadas para a direita, refletindo o crescimento desordenado
#   e o gigantismo típico de células neoplásicas.
# - **Assimetria e Escalas Distintas:** As distribuições de área e perímetro apresentam assimetria positiva pronunciada e ordens de grandeza
#   completamente distintas em relação à suavidade (`smoothness_mean`). Esse contraste comprova a necessidade estrita de
#   **padronização de escala (*StandardScaler*)** para algoritmos sensíveis à magnitude dos atributos.

# %%
# ==========================================
# 4. PRÉ-PROCESSAMENTO E PIPELINE EM PYTHON
# ==========================================
# 1. Remoção de colunas irrelevantes
colunas_para_remover = [c for c in ['id', 'Id', 'Unnamed: 32'] if c in df.columns]
df_model = df.drop(columns=colunas_para_remover).copy()

# 2. Codificação da variável alvo: M -> 1 (Maligno), B -> 0 (Benigno)
df_model['target'] = df_model['diagnosis'].map({'M': 1, 'B': 0})
X = df_model.drop(columns=['diagnosis', 'target'])
y = df_model['target']

print(f"Matriz de Atributos (X): {X.shape[0]} amostras, {X.shape[1]} atributos")
print(f"Vetor de Rótulos (y):   {y.shape[0]} amostras")

# 3. Separação Clara entre Treino (70%), Validação (15%) e Teste (15%)
# Primeiro split: 70% Treino e 30% Temporário (Validação + Teste)
X_train, X_temp, y_train, y_temp = train_test_split(
    X, y, test_size=0.30, random_state=42, stratify=y
)

# Segundo split: Divide o temporário igualmente em 15% Validação e 15% Teste
X_val, X_test, y_val, y_test = train_test_split(
    X_temp, y_temp, test_size=0.50, random_state=42, stratify=y_temp
)

print("\n--- SEPARAÇÃO DAS PARTIÇÕES (ESTRATIFICADA) ---")
print(f"Conjunto de Treino:    {X_train.shape[0]} amostras ({y_train.sum()} malignos - {y_train.mean():.1%})")
print(f"Conjunto de Validação: {X_val.shape[0]} amostras ({y_val.sum()} malignos - {y_val.mean():.1%})")
print(f"Conjunto de Teste:     {X_test.shape[0]} amostras ({y_test.sum()} malignos - {y_test.mean():.1%})")

# 4. Construção dos Pipelines do Scikit-Learn
# O Pipeline encapsula a normalização garantindo que os parâmetros de escala (média e desvio)
# sejam aprendidos exclusivamente no treino, prevenindo vazamento de dados (data leakage).
pipeline_lr = Pipeline([
    ('scaler', StandardScaler()),
    ('classifier', LogisticRegression(max_iter=1000, random_state=42))
])

pipeline_dt = Pipeline([
    ('classifier', DecisionTreeClassifier(max_depth=4, min_samples_split=5, random_state=42))
])

print("\nPipelines de pré-processamento e modelagem configurados com sucesso!")

# %%
# ==========================================
# 5. MODELAGEM PREDITIVA E AJUSTE DE HIPERPARÂMETROS
# ==========================================
# Treinamento nos dados de Treino
pipeline_lr.fit(X_train, y_train)
pipeline_dt.fit(X_train, y_train)

# Avaliação no Conjunto de Validação (Ajuste e Verificação de Overfitting)
y_val_pred_lr = pipeline_lr.predict(X_val)
y_val_proba_lr = pipeline_lr.predict_proba(X_val)[:, 1]

y_val_pred_dt = pipeline_dt.predict(X_val)
y_val_proba_dt = pipeline_dt.predict_proba(X_val)[:, 1]

metricas_val = {
    "Acurácia (Val)": [accuracy_score(y_val, y_val_pred_lr), accuracy_score(y_val, y_val_pred_dt)],
    "Precisão (Val)": [precision_score(y_val, y_val_pred_lr), precision_score(y_val, y_val_pred_dt)],
    "Recall (Val)":   [recall_score(y_val, y_val_pred_lr), recall_score(y_val, y_val_pred_dt)],
    "F1-Score (Val)": [f1_score(y_val, y_val_pred_lr), f1_score(y_val, y_val_pred_dt)],
    "ROC-AUC (Val)":  [roc_auc_score(y_val, y_val_proba_lr), roc_auc_score(y_val, y_val_proba_dt)]
}

df_val = pd.DataFrame(metricas_val, index=["Regressão Logística", "Árvore de Decisão"])
print("--- DESEMPENHO NO CONJUNTO DE VALIDAÇÃO ---")
display(df_val)

# %% [markdown]
# ### Análise da Validação:
# - A Regressão Logística atinge alto desempenho no conjunto de validação (Acurácia ~96.5% e Recall ~90.6%).
# - A Árvore de Decisão com restrição de profundidade (`max_depth=4`) atinge ~89.4% de acurácia, evitando o sobreajuste
#   completo dos dados de treino e mantendo uma estrutura de regras compreensível para auditoria clínica.

# %%
# ==========================================
# 6. AVALIAÇÃO FINAL NO CONJUNTO DE TESTE
# ==========================================
# Predições cegas nos dados de teste nunca vistos
y_test_pred_lr = pipeline_lr.predict(X_test)
y_test_proba_lr = pipeline_lr.predict_proba(X_test)[:, 1]

y_test_pred_dt = pipeline_dt.predict(X_test)
y_test_proba_dt = pipeline_dt.predict_proba(X_test)[:, 1]

metricas_teste = {
    "Acurácia":               [accuracy_score(y_test, y_test_pred_lr), accuracy_score(y_test, y_test_pred_dt)],
    "Precisão":               [precision_score(y_test, y_test_pred_lr), precision_score(y_test, y_test_pred_dt)],
    "Recall (Sensibilidade)": [recall_score(y_test, y_test_pred_lr), recall_score(y_test, y_test_pred_dt)],
    "F1-Score":               [f1_score(y_test, y_test_pred_lr), f1_score(y_test, y_test_pred_dt)],
    "ROC-AUC":                [roc_auc_score(y_test, y_test_proba_lr), roc_auc_score(y_test, y_test_proba_dt)]
}

df_teste = pd.DataFrame(metricas_teste, index=["Regressão Logística", "Árvore de Decisão"])
print("--- COMPARATIVO DE MÉTRICAS (CONJUNTO DE TESTE) ---")
display(df_teste)

# %%
# 6.1. Matrizes de Confusão e Relatórios Detalhados
fig, axes = plt.subplots(1, 2, figsize=(13, 5))

# Matriz Regressão Logística
cm_lr = confusion_matrix(y_test, y_test_pred_lr)
sns.heatmap(cm_lr, annot=True, fmt='d', cmap='Blues', cbar=False, ax=axes[0],
            xticklabels=['Benigno (0)', 'Maligno (1)'], yticklabels=['Benigno (0)', 'Maligno (1)'])
axes[0].set_title(f"Regressão Logística (Teste)\nRecall: {df_teste.loc['Regressão Logística', 'Recall (Sensibilidade)']:.2%}", fontweight='bold')
axes[0].set_xlabel("Predição do Modelo")
axes[0].set_ylabel("Diagnóstico Real")

# Matriz Árvore de Decisão
cm_dt = confusion_matrix(y_test, y_test_pred_dt)
sns.heatmap(cm_dt, annot=True, fmt='d', cmap='Greens', cbar=False, ax=axes[1],
            xticklabels=['Benigno (0)', 'Maligno (1)'], yticklabels=['Benigno (0)', 'Maligno (1)'])
axes[1].set_title(f"Árvore de Decisão (Teste)\nRecall: {df_teste.loc['Árvore de Decisão', 'Recall (Sensibilidade)']:.2%}", fontweight='bold')
axes[1].set_xlabel("Predição do Modelo")
axes[1].set_ylabel("Diagnóstico Real")

plt.tight_layout()
plt.show()

print("\n--- CLASSIFICATION REPORT: REGRESSÃO LOGÍSTICA ---")
print(classification_report(y_test, y_test_pred_lr, target_names=['Benigno', 'Maligno']))

print("\n--- CLASSIFICATION REPORT: ÁRVORE DE DECISÃO ---")
print(classification_report(y_test, y_test_pred_dt, target_names=['Benigno', 'Maligno']))

# %% [markdown]
# ### Discussão Médica Crítica sobre a Escolha das Métricas:
# No contexto oncológico:
# - **Recall (Sensibilidade) é a métrica mandatória:** Um **Falso Negativo (FN)** significa que uma paciente portadora de tumor
#   maligno recebe um resultado falso de benignidade, atrasando o início do tratamento e agravando o prognóstico de sobrevivência.
# - A **Regressão Logística** demonstrou superioridade decisiva, alcançando um Recall de **96.88%** no conjunto de teste,
#   cometendo apenas 1 falso negativo em 32 casos malignos, enquanto a Árvore de Decisão obteve 81.25% de Recall (6 falsos negativos).

# %%
# ==========================================
# 7. INTERPRETABILIDADE: FEATURE IMPORTANCE E SHAP
# ==========================================
# 7.1. Importância Intrínseca Tradicional
dt_model = pipeline_dt.named_steps['classifier']
lr_model = pipeline_lr.named_steps['classifier']

importancias_dt = pd.Series(dt_model.feature_importances_, index=X.columns)
top_dt = importancias_dt[importancias_dt > 0].sort_values(ascending=True)

coef_lr = pd.Series(np.abs(lr_model.coef_[0]), index=X.columns).sort_values(ascending=True).tail(10)

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

top_dt.plot(kind='barh', color='#2ca02c', ax=axes[0])
axes[0].set_title("Feature Importance (Árvore de Decisão - Impureza Gini)", fontweight='bold')
axes[0].set_xlabel("Importância Relativa")

coef_lr.plot(kind='barh', color='#1f77b4', ax=axes[1])
axes[1].set_title("Top 10 Características (|Coeficientes|) - Regressão Logística", fontweight='bold')
axes[1].set_xlabel("Magnitude do Coeficiente")

plt.tight_layout()
plt.show()

# %%
# 7.2. SHAP Global e Local para a Regressão Logística
print("--- CALCULANDO SHAP GLOBAL E LOCAL PARA A REGRESSÃO LOGÍSTICA ---")
scaler = pipeline_lr.named_steps['scaler']
X_train_scaled = pd.DataFrame(scaler.transform(X_train), columns=X_train.columns, index=X_train.index)
X_test_scaled = pd.DataFrame(scaler.transform(X_test), columns=X_test.columns, index=X_test.index)
masker = shap.maskers.Independent(X_train_scaled, max_samples=len(X_train_scaled))
explainer_lr = shap.LinearExplainer(lr_model, masker)
shap_values_lr = explainer_lr(X_test_scaled)

# Gráfico 1: Importância global (Bar Plot)
shap.plots.bar(shap_values_lr, show=False)
plt.title("SHAP: Importância Global na Regressão Logística", fontsize=12, fontweight='bold')
plt.tight_layout()
plt.show()

# Gráfico 2: Distribuição e direção das contribuições (Beeswarm)
shap.plots.beeswarm(shap_values_lr, show=False)
plt.title("SHAP Beeswarm: Impacto e Direção na Regressão Logística", fontsize=12, fontweight='bold')
plt.tight_layout()
plt.show()

# Gráficos 3 e 4: Explicações locais de casos corretamente classificados no teste
for class_value, class_name in [(1, "Maligno"), (0, "Benigno")]:
    candidates = np.flatnonzero((y_test.to_numpy() == class_value) & (y_test_pred_lr == class_value))
    if candidates.size == 0:
        raise ValueError(f"Nenhum caso de teste corretamente classificado para a classe {class_name}.")

    position = candidates[np.argmin(np.abs(y_test_proba_lr[candidates] - 0.5))]
    shap.plots.waterfall(shap_values_lr[position], max_display=10, show=False)
    plt.title(
        f"SHAP local - Caso {class_name} corretamente classificado\n"
        f"Probabilidade estimada de malignidade: {y_test_proba_lr[position]:.1%}",
        fontsize=10,
        fontweight='bold'
    )
    plt.tight_layout()
    plt.show()
    print(f"Caso {class_name}: linha {X_test.index[position]}, probabilidade de malignidade {y_test_proba_lr[position]:.1%}")

# %% [markdown]
# ### Interpretação Clínica com SHAP:
# - **Atributo Chave (`concave points_worst`):** O gráfico Beeswarm evidencia que valores elevados deste atributo (pontos em vermelho)
#   deslocam o valor SHAP fortemente para a direita, aumentando de maneira drástica a probabilidade de predição maligna.
#   Clinicamente, isso indica que a severidade e número de deformidades/indentações na membrana dos núcleos celulares
#   são o biomarcador morfológico mais decisivo para diagnóstico de malignidade.
# - **Transparência para a Equipe Médica:** Diferente de métricas globais opacas, o SHAP fornece fundamentação embasada
#   na Teoria dos Jogos, permitindo que o médico audite a razão exata pela qual o algoritmo sinalizou determinado paciente para triagem prioritária.

# %% [markdown]
# ==========================================
# ## 8. CONCLUSÕES E DIRETRIZES DE IMPLANTAÇÃO CLÍNICA
# ==========================================
#
# ### 8.1. Síntese dos Resultados Técnicos
# 1. **Regressão Logística em Pipeline:** Demonstrou a melhor capacidade de generalização e segurança clínica, atingindo
#    **97.67% de acurácia** e **96.88% de Recall** no conjunto de teste final não visto.
# 2. **Árvore de Decisão:** Apresentou **91.86% de acurácia** e **81.25% de Recall**, servindo como excelente modelo de
#    regras de decisão transparentes, corroborado pela convergência das análises de SHAP e Gini.
# 3. **Separação Rigorosa:** A adoção da divisão em três etapas (Treino 70%, Validação 15% e Teste 15%) assegurou que não
#    houvesse vazamento de dados nem otimização oportunista no conjunto de teste.
#
# ### 8.2. Recomendações Hospitalares para Triagem (Uso na Prática)
# - **Triagem de Prioridade em Filas de Laudo:** Integrar o modelo ao PACS/LIS do hospital universitário. Amostras que apresentarem
#   probabilidade calculada de malignidade superior ao limiar de segurança devem ser imediatamente marcadas com bandeira vermelha
#   para análise prioritária pelo médico patologista.
# - **Seleção do Limiar:** Qualquer ajuste deve ser escolhido no conjunto de validação, considerando o impacto sobre Recall
#   e falsos positivos. O desempenho final deve ser medido no conjunto de teste; esta análise não avaliou um limiar alternativo.
#
# ---
# > **DIRETRIZ ÉTICA E CLÍNICA OBRIGATÓRIA:**
# > Este sistema de inteligência artificial atua exclusivamente como ferramenta computacional de triagem e
# > **Sistema de Suporte à Decisão Clínica (CDSS)**. O modelo não substitui o julgamento profissional:
# > **a avaliação clínica integral, o contexto do paciente e o laudo definitivo cabem sempre e exclusivamente ao médico especialista.**
