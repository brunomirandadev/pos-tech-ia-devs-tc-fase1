import os
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import shap

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_auc_score
)

# Output directory for images
img_dir = Path("tech_challenge/imagens")
img_dir.mkdir(parents=True, exist_ok=True)

sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams['figure.dpi'] = 150

# Load dataset
df = pd.read_csv("data/BreastCancer.csv")

# 1. Target distribution
fig, ax = plt.subplots(figsize=(6, 4))
sns.countplot(data=df, x='diagnosis', hue='diagnosis', order=['B', 'M'], hue_order=['B', 'M'], palette=['#2b5c8f', '#d95f02'], legend=False, ax=ax)
ax.set_title("Distribuição dos Diagnósticos (B = Benigno | M = Maligno)", fontsize=11, fontweight='bold')
ax.set_xlabel("Diagnóstico Clínico")
ax.set_ylabel("Total de Casos")
ax.set_xticks([0, 1])
ax.set_xticklabels(["Benigno (B)", "Maligno (M)"])

for p in ax.patches:
    altura = int(p.get_height())
    ax.annotate(f"{altura} ({altura / len(df) * 100:.1f}%)",
                (p.get_x() + p.get_width() / 2., altura / 2),
                ha='center', va='center', color='white', fontweight='bold', fontsize=10)

plt.tight_layout()
plt.savefig(img_dir / "01_distribuicao_alvo.png")
plt.close()

# 2. Correlation heatmap
df_numeric = df.select_dtypes(include=[np.number])
colunas_ignorar = [c for c in ['id', 'Id', 'Unnamed: 32'] if c in df_numeric.columns]
df_numeric_clean = df_numeric.drop(columns=colunas_ignorar)

plt.figure(figsize=(12, 9))
corr = df_numeric_clean.corr()
mask = np.triu(np.ones_like(corr, dtype=bool))
sns.heatmap(corr, mask=mask, cmap="coolwarm", center=0, linewidths=0.5, annot=False)
plt.title("Matriz de Correlação das Características Numéricas do Núcleo Celular", fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig(img_dir / "02_matriz_correlacao.png")
plt.close()

# 3. Histograms
colunas_grafico = ['radius_mean', 'texture_mean', 'perimeter_mean', 'area_mean', 'smoothness_mean', 'concavity_mean']
fig, axes = plt.subplots(2, 3, figsize=(14, 7))
axes = axes.flatten()

for i, col in enumerate(colunas_grafico):
    sns.histplot(data=df, x=col, hue='diagnosis', kde=True, ax=axes[i], palette=['#d95f02', '#2b5c8f'], stat="density")
    axes[i].set_title(f"Distribuição: {col}", fontweight='bold', fontsize=10)
    axes[i].set_xlabel("")

plt.suptitle("Histogramas de Características Morfológicas (Maligno vs. Benigno)", fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig(img_dir / "03_distribuicoes_morfologicas.png")
plt.close()

# Preprocessing & 3-way split
colunas_para_remover = [c for c in ['id', 'Id', 'Unnamed: 32'] if c in df.columns]
df_model = df.drop(columns=colunas_para_remover).copy()
df_model['target'] = df_model['diagnosis'].map({'M': 1, 'B': 0})
X = df_model.drop(columns=['diagnosis', 'target'])
y = df_model['target']

X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.30, random_state=42, stratify=y)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.50, random_state=42, stratify=y_temp)

pipeline_lr = Pipeline([
    ('scaler', StandardScaler()),
    ('classifier', LogisticRegression(max_iter=1000, random_state=42))
])

pipeline_dt = Pipeline([
    ('classifier', DecisionTreeClassifier(max_depth=4, min_samples_split=5, random_state=42))
])

pipeline_lr.fit(X_train, y_train)
pipeline_dt.fit(X_train, y_train)

# Predictions on Test set
y_test_pred_lr = pipeline_lr.predict(X_test)
y_test_pred_dt = pipeline_dt.predict(X_test)

# 4. Confusion matrices
fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))

cm_lr = confusion_matrix(y_test, y_test_pred_lr)
rec_lr = recall_score(y_test, y_test_pred_lr)
sns.heatmap(cm_lr, annot=True, fmt='d', cmap='Blues', cbar=False, ax=axes[0],
            xticklabels=['Benigno (0)', 'Maligno (1)'], yticklabels=['Benigno (0)', 'Maligno (1)'])
axes[0].set_title(f"Regressão Logística (Teste)\nRecall: {rec_lr:.2%} | Acurácia: {accuracy_score(y_test, y_test_pred_lr):.2%}", fontweight='bold', fontsize=11)
axes[0].set_xlabel("Predição do Modelo")
axes[0].set_ylabel("Diagnóstico Real")

cm_dt = confusion_matrix(y_test, y_test_pred_dt)
rec_dt = recall_score(y_test, y_test_pred_dt)
sns.heatmap(cm_dt, annot=True, fmt='d', cmap='Greens', cbar=False, ax=axes[1],
            xticklabels=['Benigno (0)', 'Maligno (1)'], yticklabels=['Benigno (0)', 'Maligno (1)'])
axes[1].set_title(f"Árvore de Decisão (Teste)\nRecall: {rec_dt:.2%} | Acurácia: {accuracy_score(y_test, y_test_pred_dt):.2%}", fontweight='bold', fontsize=11)
axes[1].set_xlabel("Predição do Modelo")
axes[1].set_ylabel("Diagnóstico Real")

plt.tight_layout()
plt.savefig(img_dir / "04_matrizes_confusao.png")
plt.close()

# 5. Feature Importance
dt_model = pipeline_dt.named_steps['classifier']
lr_model = pipeline_lr.named_steps['classifier']

importancias_dt = pd.Series(dt_model.feature_importances_, index=X.columns)
top_dt = importancias_dt[importancias_dt > 0].sort_values(ascending=True)
coef_lr = pd.Series(np.abs(lr_model.coef_[0]), index=X.columns).sort_values(ascending=True).tail(10)

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
top_dt.plot(kind='barh', color='#2ca02c', ax=axes[0])
axes[0].set_title("Feature Importance (Árvore de Decisão - Impureza Gini)", fontweight='bold', fontsize=11)
axes[0].set_xlabel("Importância Relativa")

coef_lr.plot(kind='barh', color='#1f77b4', ax=axes[1])
axes[1].set_title("Top 10 Características (|Coef|) na Regressão Logística", fontweight='bold', fontsize=11)
axes[1].set_xlabel("Valor Absoluto do Coeficiente")

plt.tight_layout()
plt.savefig(img_dir / "05_feature_importance.png")
plt.close()

# 6. SHAP Plots for the selected Logistic Regression model
scaler = pipeline_lr.named_steps['scaler']
X_train_scaled = pd.DataFrame(scaler.transform(X_train), columns=X_train.columns, index=X_train.index)
X_test_scaled = pd.DataFrame(scaler.transform(X_test), columns=X_test.columns, index=X_test.index)
masker = shap.maskers.Independent(X_train_scaled, max_samples=len(X_train_scaled))
explainer = shap.LinearExplainer(lr_model, masker)
shap_values = explainer(X_test_scaled)

# Plot Bar
plt.figure(figsize=(9, 5))
shap.plots.bar(shap_values, show=False)
plt.title("SHAP: Importância Global dos Atributos na Detecção de Malignidade", fontsize=11, fontweight='bold')
plt.tight_layout()
plt.savefig(img_dir / "06_shap_summary_bar.png")
plt.close()

# Plot Beeswarm
plt.figure(figsize=(9, 5))
shap.plots.beeswarm(shap_values, show=False)
plt.title("SHAP Beeswarm: Impacto e Direção das Características Citológicas", fontsize=11, fontweight='bold')
plt.tight_layout()
plt.savefig(img_dir / "07_shap_beeswarm.png")
plt.close()

# Local explanations for correctly classified malignant and benign test samples.
y_test_values = y_test.to_numpy()
y_test_pred_lr = pipeline_lr.predict(X_test)
y_test_proba_lr = pipeline_lr.predict_proba(X_test)[:, 1]

for class_value, class_name, file_name in [
    (1, "Maligno", "08_shap_local_maligno.png"),
    (0, "Benigno", "09_shap_local_benigno.png"),
]:
    candidates = np.flatnonzero((y_test_values == class_value) & (y_test_pred_lr == class_value))
    if candidates.size == 0:
        raise ValueError(f"Nenhum caso de teste corretamente classificado para a classe {class_name}.")

    position = candidates[np.argmin(np.abs(y_test_proba_lr[candidates] - 0.5))]
    shap.plots.waterfall(shap_values[position], max_display=10, show=False)
    plt.title(
        f"SHAP local - Caso {class_name} corretamente classificado\n"
        f"Probabilidade estimada de malignidade: {y_test_proba_lr[position]:.1%}",
        fontsize=10,
        fontweight='bold'
    )
    plt.tight_layout()
    plt.savefig(img_dir / file_name, dpi=150, bbox_inches="tight")
    plt.close()

print("All 9 report charts generated successfully in tech_challenge/imagens/")

