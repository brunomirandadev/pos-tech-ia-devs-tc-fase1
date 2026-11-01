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
- **32 features** derivadas de medidas citológicas
- Núcleos malignos têm **raio, área e concavidade maiores** — *mostrar histogramas sobrepostos*

---

### **BLOCO 3: PREPARAÇÃO E MODELOS (2:00 min)**
**[Mostrar tabela de resultados]**
- Divisão: 70% treino, 15% validação, 15% teste
- **2 modelos testados:**

| Modelo | Acurácia | Recall |
|--------|----------|--------|
| **Regressão Logística** | 97.7% | 97.6% |
| **Árvore de Decisão** | 95.3% | 98.8% |

- Escolhida: **Regressão Logística** (97.7% acurácia, 0.99 ROC-AUC)
- **Apenas 3 casos de câncer não detectados** em 86 testes

---

### **BLOCO 4: INTERPRETABILIDADE COM SHAP (4:30 min)**

#### **4.1 Quais features importam?**
**[Feature Importance - barras]**
- `concave_points_worst` — contorno celular indentado
- `radius_worst` — tamanho do núcleo
- `texture_worst` — irregularidade da textura

**Insight:** "Características de irregularidade celular indicam malignidade."

#### **4.2 SHAP Beeswarm — Visão Global**
**[Gráfico SHAP]**
- Eixo X: Contribuição para "maligno"
- Pontos vermelhos (valores altos) → **empurram para maligno**
- "Concave_points alto (vermelho) = forte indicador de câncer"

#### **4.3 SHAP Force Plot — Exemplo Individual**
**[2 Exemplos]**
1. **Paciente maligno:** concave_points alto (+0.8) + radius alto (+0.5) = 97% maligno
2. **Paciente benigno:** features baixas → 2% maligno = seguro

**Frase:** "Médico vê exatamente quais características dispararam o alerta."

---

### **BLOCO 5: APLICAÇÃO PRÁTICA (1:00 min)**
- **Integração LIS/PACS:** Exames com prob > 50% vão para o topo da fila
- **Ajuste de sensibilidade:** Pode reduzir threshold para 0.35 se quiser 100% recall
- **Auditoria:** Cada predição vem com explicação SHAP

---

### **BLOCO 6: CONCLUSÃO (0:30 min)**
✅ **97.7% acurácia** | ✅ **Interpretável** | ✅ **Pronto para produção**

**Links:**
- Repositório: `github.com/brunomirandadev/pos-tech-ia-devs-tc-fase1`
- Relatório técnico: `tech_challenge/Relatorio_Tecnico_Tech_Challenge_Fase1.pdf`

---

## 🎯 CHECKLIST DE EXECUÇÃO

| Item | Status |
|------|--------|
| 1️⃣ Mostrar distribuição de classes (pie chart) | ⬜ |
| 2️⃣ Mostrar histogramas: malignos vs benignos | ⬜ |
| 3️⃣ Mostrar tabela de métricas (97.7% acurácia) | ⬜ |
| 4️⃣ Mostrar gráfico Feature Importance | ⬜ |
| 5️⃣ Mostrar SHAP beeswarm | ⬜ |
| 6️⃣ Mostrar 2 exemplos SHAP force plot | ⬜ |
| 7️⃣ Explicar aplicação clínica (LIS/PACS) | ⬜ |

---

## ⏱️ TIMING (10 min total)

```
0:00  | Introdução
1:00  | Dados (gráficos)
2:00  | Modelos e resultados
4:00  | SHAP (Feature Imp + Beeswarm + Exemplos)
8:30  | Aplicação prática
9:30  | Conclusão e links
10:00 | FIM
```

---

## 📊 GRÁFICOS A MOSTRAR (NA ORDEM)

1. ✅ Pie chart: distribuição de classes (63% benigno, 37% maligno)
2. ✅ Histogramas sobrepostos: benignos vs malignos
3. ✅ Tabela de comparação de modelos (acurácia, recall, ROC-AUC)
4. ✅ Feature Importance (top 5 features)
5. ✅ SHAP Beeswarm (contribuição global)
6. ✅ SHAP Force Plot (2 exemplos: 1 maligno, 1 benigno)

---

## 💡 DICAS DE APRESENTAÇÃO

| Aspecto | Recomendação |
|---------|--------------|
| **Ritmo** | 1 conceito por 30-45 seg, fala clara |
| **Visuais** | Maximize gráficos, minimize código |
| **Números** | Cite: 97.7%, 0.99 ROC-AUC, apenas 3 falsos negativos |
| **Jargão** | Explique SHAP como "decomposição de contribuição" |
| **Pausa** | 2-3 seg após cada resultado importante |
| **Áudio** | Fundo neutro, sem ruído, qualidade boa |

---

## 🎬 SCRIPT BREVE POR BLOCO

**BLOCO 1:**
"Bem-vindo! Essa solução resolve um problema real de hospitais: com crescimento de pacientes, fila de exames mamários gera atraso que prejudica diagnóstico. Nossa IA ajuda a priorizar os casos críticos para análise prioritária. Importante: a IA é uma ferramenta de apoio; a palavra final é sempre do médico."

**BLOCO 2:**
"Usamos 569 amostras de exames de mama. Aqui vemos que 63% são benignos e 37% malignos. Esses 32 números que aparecem em cada amostra são medidas do núcleo da célula. Veja: núcleos cancerosos (laranja) têm raio, área e contorno muito mais irregulares que os benignos."

**BLOCO 3:**
"Treinamos 2 modelos de IA. A Regressão Logística alcançou 97.7% de acurácia — significa que acertou 84 de 86 casos de teste. Apenas 3 cânceres não foram detectados. A Árvore de Decisão detecta mais cânceres, mas comete falsos alarmes, então escolhemos a Regressão Logística."

**BLOCO 4:**
"Agora o mais importante: qual foi a razão de cada predição? Usamos SHAP, que decompõe a decisão do modelo. Aqui vemos que 'contorno indentado' é o maior indicador. Para um paciente maligno, essas características (valores altos) empurram a predição para câncer. Para um benigno, as características baixas afastam o risco."

**BLOCO 5:**
"Como isso funciona na prática? O modelo integra no sistema do hospital. Quando um exame chega, se tem probabilidade > 50% de câncer, sobe para o topo da fila de análise. O patologista vê também um gráfico que explica por que a IA alertou, aumentando confiança no sistema."

**BLOCO 6:**
"Resumindo: modelo com 97.7% acurácia, totalmente interpretável, pronto para usar. Se quiser mais detalhes, acesse o repositório no GitHub ou o relatório técnico em PDF."

---

**PRONTO PARA GRAVAR!** 🎬

