# 🎬 ROTEIRO VÍDEO - TECH CHALLENGE FASE 1
## Diagnóstico de Câncer de Mama com IA
**⏱️ DURAÇÃO: ~10 MINUTOS**

---

## 📋 ESTRUTURA ENXUTA

### **BLOCO 1: INTRODUÇÃO (1:00 min)**
- **Problema:** Hospital com fila de exames mamários; atraso pode comprometer prognóstico
- **Solução:** IA para triagem automatizada e priorização
- **Frase-chave:** "IA apoiando o médico, não substituindo. Sempre é o patologista quem decide."

---

### **BLOCO 2: DADOS (1:00 min)**
**[Mostrar 2 gráficos]**
- **569 amostras** (63% benigno, 37% maligno) — *mostrar pie chart*
- **30 medidas numéricas** das características do núcleo celular
- Núcleos malignos têm **raio, área e concavidade maiores** — *mostrar histogramas sobrepostos*

---

### **BLOCO 3: PREPARAÇÃO E MODELOS (2:00 min)**
**[Mostrar tabela de resultados]**
- Divisão: 70% treino, 15% validação, 15% teste
- **2 modelos testados:**

| Modelo | Acurácia | Recall |
|--------|----------|--------|
| **Regressão Logística** | 97.67% | 96.88% |
| **Árvore de Decisão** | 91.86% | 81.25% |

- Escolhida: **Regressão Logística** (97.67% de acurácia e 0.9988 de ROC-AUC)
- No teste, a Regressão Logística deixou passar **1 caso maligno**; a Árvore de Decisão, **6**

---

### **BLOCO 4: INTERPRETABILIDADE COM SHAP (4:30 min)**

#### **4.1 Quais features importam?**
**[Mostrar os dois gráficos: importância Gini da Árvore de Decisão e magnitude dos coeficientes da Regressão Logística]**
- Na Árvore de Decisão, `perimeter_worst` tem maior importância, seguido por `concave points_worst` e `texture_worst`
- Na Regressão Logística, as maiores magnitudes incluem `texture_worst`, `radius_se` e `symmetry_worst`

**Insight:** "Características de irregularidade celular indicam malignidade."

#### **4.2 SHAP Beeswarm — Visão Global**
**[Gráfico SHAP]**
- Eixo X: Contribuição para "maligno"
- Pontos vermelhos (valores altos) → **empurram para maligno**
- `texture_worst` aparece na primeira linha, seguida por `radius_se`, `radius_worst`, `area_worst` e `symmetry_worst`. Valores altos de `texture_worst` tendem a contribuir para a classe maligna, mas há variação entre as amostras.

#### **4.3 SHAP Bar Plot — Importância Global**
**[Mostrar gráfico SHAP de barras]**
- Resume a magnitude média absoluta das contribuições no conjunto de teste.
- `texture_worst` tem maior magnitude média, seguida por `radius_se`, `radius_worst`, `area_worst` e `symmetry_worst`.

**Frase:** "Este gráfico resume globalmente as contribuições SHAP; ele não explica um paciente específico."

#### **4.4 SHAP Waterfall — Exemplos Locais**
**[Mostrar os dois waterfall plots locais]**
- Caso maligno corretamente classificado: probabilidade estimada de malignidade de **53,1%**.
- Caso benigno corretamente classificado: probabilidade estimada de malignidade de **24,4%**.
- Pense em log-odds como um placar interno: contribuições positivas empurram para maligno e negativas para benigno; depois o modelo converte esse placar em probabilidade. Log-odds não é porcentagem. As entradas estão padronizadas, e os exemplos não substituem a avaliação médica.

---

### **BLOCO 5: APLICAÇÃO PRÁTICA (1:00 min)**
- **Integração LIS/PACS:** Como proposta, casos sinalizados podem ser priorizados para revisão pelo patologista.
- **Ajuste de sensibilidade:** O limiar deve ser selecionado na validação, considerando Recall e falsos positivos; o resultado final deve ser medido no teste. Este projeto não avaliou um limiar alternativo.
- **Auditoria:** O notebook inclui dois exemplos SHAP locais; seu uso para apoiar decisões em cada paciente ainda exige validação clínica e operacional.

---

### **BLOCO 6: CONCLUSÃO (0:30 min)**
✅ **97.67% de acurácia no teste** | ✅ **Análise global com SHAP** | ✅ **Protótipo para validação adicional, não pronto para uso clínico**

**Links:**
- Repositório: `github.com/brunomirandadev/pos-tech-ia-devs-tc-fase1`
- Relatório técnico: `tech_challenge/Relatorio_Tecnico_Tech_Challenge_Fase1.pdf`

---

## 🎯 CHECKLIST DE EXECUÇÃO

| Item | Status |
|------|--------|
| 1️⃣ Mostrar distribuição de classes (pie chart) | ⬜ |
| 2️⃣ Mostrar histogramas: malignos vs benignos | ⬜ |
| 3️⃣ Mostrar tabela de métricas dos dois modelos | ⬜ |
| 4️⃣ Mostrar Feature Importance dos dois modelos | ⬜ |
| 5️⃣ Mostrar SHAP bar global | ⬜ |
| 6️⃣ Mostrar SHAP beeswarm global | ⬜ |
| 7️⃣ Mostrar waterfall local do caso maligno | ⬜ |
| 8️⃣ Mostrar waterfall local do caso benigno | ⬜ |
| 9️⃣ Explicar aplicação proposta e limites de uso | ⬜ |

---

## ⏱️ TIMING (10 min total)

```
0:00  | Introdução
1:00  | Dados (gráficos)
2:00  | Modelos e resultados
4:00  | SHAP (Feature Importance + bar global + beeswarm)
8:30  | Aplicação prática
9:30  | Conclusão e links
10:00 | FIM
```

---

## 📊 GRÁFICOS A MOSTRAR (NA ORDEM)

1. ✅ Pie chart: distribuição de classes (63% benigno, 37% maligno)
2. ✅ Histogramas sobrepostos: benignos vs malignos
3. ✅ Tabela de comparação de modelos (acurácia, recall, F1-Score e ROC-AUC)
4. ✅ Feature Importance dos dois modelos
5. ✅ SHAP bar (importância global)
6. ✅ SHAP Beeswarm (distribuição e direção global)

---

## 💡 DICAS DE APRESENTAÇÃO

| Aspecto | Recomendação |
|---------|--------------|
| **Ritmo** | 1 conceito por 30-45 seg, fala clara |
| **Visuais** | Maximize gráficos, minimize código |
| **Números** | Cite: 97.67% de acurácia, 0.9988 de ROC-AUC e 1 falso negativo na Regressão Logística |
| **Jargão** | Explique SHAP como "decomposição de contribuição" |
| **Pausa** | 2-3 seg após cada resultado importante |
| **Áudio** | Fundo neutro, sem ruído, qualidade boa |

---

## 🎬 SCRIPT BREVE POR BLOCO

**BLOCO 1:**
"Bem-vindo! Essa solução resolve um problema real de hospitais: com crescimento de pacientes, fila de exames mamários gera atraso que prejudica diagnóstico. Nossa IA ajuda a priorizar os casos críticos para análise prioritária. Importante: a IA é uma ferramenta de apoio; a palavra final é sempre do médico."

**BLOCO 2:**
"Usamos 569 amostras de exames de mama. Cerca de 63% são benignas e 37% malignas. Cada amostra tem 30 medidas numéricas do núcleo celular, além do identificador e do diagnóstico. Nos histogramas, algumas medidas apresentam distribuições diferentes entre os grupos, com sobreposição entre benignos e malignos."

**BLOCO 3:**
"Treinamos dois modelos. No conjunto de teste, a Regressão Logística alcançou 97,67% de acurácia, 96,88% de recall e 96,88% de precisão. Errou dois casos no total, incluindo um caso maligno não detectado. A Árvore de Decisão alcançou 91,86% de acurácia e 81,25% de recall, deixando passar seis dos 32 casos malignos."

**BLOCO 4:**
"Para entender o comportamento do modelo, usamos SHAP. Na Regressão Logística, texture_worst tem a maior magnitude média global, seguida por radius_se e radius_worst. Os dois waterfall plots mostram as contribuições em um caso benigno e um maligno corretamente classificados. Os valores SHAP somam na escala de log-odds; os exemplos ajudam a inspecionar o modelo, mas não substituem a avaliação médica."

**BLOCO 5:**
"Como poderia funcionar na prática? Em uma integração futura, casos sinalizados poderiam ser priorizados para revisão pelo patologista. O limiar precisaria ser escolhido com dados de validação e seu impacto em recall e falsos positivos medido no teste. Este notebook mostra dois exemplos SHAP locais; seu uso para apoiar decisões clínicas exige validação adicional."

**BLOCO 6:**
"Resumindo: modelo com 97.7% acurácia, totalmente interpretável, pronto para usar. Se quiser mais detalhes, acesse o repositório no GitHub ou o relatório técnico em PDF."

---

**PRONTO PARA GRAVAR!** 🎬

