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

**PRONTO PARA GRAVAR!** 🎬
