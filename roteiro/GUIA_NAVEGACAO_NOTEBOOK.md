# 🎬 GUIA DE NAVEGAÇÃO - NOTEBOOK DURANTE A GRAVAÇÃO

## 📌 O QUE MUDOU?

O script agora indica **[MOSTRAR DO NOTEBOOK]** em vez de imagens separadas.

**Você vai:**
1. Manter o script aberto em uma tela/teleprompter
2. Manter o notebook `analise_diagnostico.ipynb` aberto na outra tela ou em janela flutuante
3. Clicar/navegar para a célula indicada quando ver [MOSTRAR DO NOTEBOOK]
4. Continuar lendo enquanto mostra o gráfico

---

## 🎯 CÉLULAS PARA MOSTRAR DURANTE A GRAVAÇÃO

### BLOCO 1: OS DADOS

#### Momento 1️⃣ - Distribuição do Alvo (após ~1 min)
```
Script diz: "[MOSTRAR DO NOTEBOOK: Célula de Distribuição do Alvo - 
gráfico com histograma 63% benigno, 37% maligno]"

O que fazer:
- Procure a célula com título "Distribuição da Classe Alvo" ou similar
- Clique para exibir o gráfico (histograma horizontal ou pizza)
- Mostre por ~15-20 segundos enquanto fala: "63% benigno, 37% maligno"
- Continue navegando quando [PAUSA 2 seg] terminar
```

**Dica:** No notebook, pode estar em:
- Seção "3. Análise Exploratória de Dados (EDA)" ou
- Procure por `plt.title` ou `ax.bar` com "diagnosis" ou "Alvo"

---

#### Momento 2️⃣ - Distribuições Morfológicas (após ~2 min 30 seg)
```
Script diz: "[MOSTRAR DO NOTEBOOK: Célula de Distribuições Morfológicas 
- 3 histogramas lado a lado mostrando Raio, Concavidade e Textura]"

O que fazer:
- Procure a célula com vários histogramas (figura com subplots)
- Deve mostrar radius_mean, concavity_mean, texture_mean
- Azul=Benigno, Laranja=Maligno
- Mostre por ~20-25 segundos enquanto explica cada painel
```

**Dica:** Procure por:
- Células com `for col in ['radius_mean', 'concavity_mean', ...]` ou
- Células que mostram 3-6 histogramas lado a lado

---

### BLOCO 3: EXPLICABILIDADE

#### Momento 3️⃣ - Feature Importance (após ~5 min 30 seg)
```
Script diz: "[MOSTRAR DO NOTEBOOK: Célula de Feature Importance 
- gráfico de barras com ranking das características]"

O que fazer:
- Procure gráfico com barras horizontais mostrando importância das features
- Concave Points, Radius, Texture devem estar no topo
- Mostre por ~15 segundos enquanto menciona top 3
```

**Dica:** Procure por:
- `feature_importance` ou `permutation_importance`
- Gráfico tipo `plt.barh()` com nomes de features

---

#### Momento 4️⃣ - SHAP Beeswarm Plot (após ~6 min)
```
Script diz: "[MOSTRAR DO NOTEBOOK: Célula SHAP Beeswarm Plot 
- gráfico mostrando padrão de explicações]"

O que fazer:
- Procure o gráfico SHAP com pontos coloridos
- Eixo horizontal mostra impacto na predição
- Cores: azul=baixo, vermelho=alto
- Posição: esquerda=benigno, direita=maligno
- Mostre por ~20-25 segundos
```

**Dica:** Procure por:
- `shap.plots.beeswarm()` ou `shap.summary_plot(..., plot_type="beeswarm")`
- Figura com título contendo "SHAP"

---

#### Momento 5️⃣ - SHAP Summary Bar Plot (após ~7 min)
```
Script diz: "[MOSTRAR DO NOTEBOOK: Célula SHAP Summary Bar Plot 
- explicação individual para pacientes]"

O que fazer:
- Procure gráfico SHAP com barras mostrando impacto de features individuais
- Exemplo de um paciente específico
- Setas vermelhas=empurra para maligno, azuis=empurra para benigno
- Mostre por ~15-20 segundos
```

**Dica:** Procure por:
- `shap.plots.beeswarm()` já apareceu? Pode haver outro depois com `force_plot`
- Ou `shap.summary_plot(..., plot_type="bar")`

---

#### Momento 6️⃣ - Matrizes de Confusão (após ~7 min 30 seg)
```
Script diz: "[MOSTRAR DO NOTEBOOK: Célula de Matrizes de Confusão 
- confusion matrices dos dois modelos]"

O que fazer:
- Procure 2 matrizes de confusão lado a lado
- Uma para Regressão Logística, outra para Árvore de Decisão
- Mostre por ~10-15 segundos
```

**Dica:** Procure por:
- `confusion_matrix()` na célula
- Gráfico tipo heatmap 2x2
- Deve ter 2 matrizes ou uma figura com 2 subplots

---

## 🔍 COMO LOCALIZAR CÉLULAS NO NOTEBOOK

### Método 1: Procura por Título (Rápido)
```
No Jupyter:
1. Pressione Ctrl+F (ou Cmd+F no Mac)
2. Digite uma palavra-chave: "Distribuição", "Feature", "SHAP", "Confusão"
3. Pula para a célula encontrada
```

### Método 2: Procura por Código (Preciso)
```
No Jupyter:
1. Pressione Ctrl+F
2. Procure por: "plt.title", "shap", "confusion_matrix"
3. Encontra exatamente a célula de código que gera o gráfico
```

### Método 3: Navegação Manual (Seguro)
```
1. Abra o notebook
2. Procure a seção "3. Análise Exploratória" ou "5. Avaliação"
3. Role até encontrar cada gráfico (está na ordem do script!)
4. Anote o número da célula (ou deixe aberto para referenciar)
```

---

## ⏱️ TIMING DE CADA GRÁFICO

| Momento | Gráfico | Apareça em | Mostre por |
|---------|---------|-----------|-----------|
| 1️⃣ | Distribuição do Alvo | ~1:00 min | 15-20 seg |
| 2️⃣ | Distribuições Morfológicas | ~2:30 min | 20-25 seg |
| 3️⃣ | Feature Importance | ~5:30 min | 15 seg |
| 4️⃣ | SHAP Beeswarm | ~6:00 min | 20-25 seg |
| 5️⃣ | SHAP Summary Bar | ~7:00 min | 15-20 seg |
| 6️⃣ | Matrizes de Confusão | ~7:30 min | 10-15 seg |

**Total de tempo mostrando gráficos: ~2 minutos**  
**Tempo falando: ~10 minutos**  
**TOTAL: ~12 minutos** ✅

---

## 🎬 SETUP RECOMENDADO PARA GRAVAÇÃO

### Opção 1: Tela Dividida (Recomendado)
```
Tela Esquerda (70%):
  └─ Notebook Jupyter com os gráficos
    └─ Você aponta/destaca o gráfico enquanto fala

Tela Direita (30%):
  └─ Teleprompter com o script
    └─ Você lê enquanto olha ocasionalmente
```

**Como fazer:**
- Windows: Win+Left (notebook), Win+Right (teleprompter)
- Mac: Arranjar janelas lado a lado manualmente
- Linux: Usar gerenciador de janelas

---

### Opção 2: Segunda Tela (Ideal)
```
Monitor 1:
  └─ Notebook em tela cheia (onde câmera aponta)

Monitor 2 (fora de câmera):
  └─ Teleprompter com script
```

**Benefício:** Você alterna olhar entre notebook (para câmera) e script (fora de câmera)

---

### Opção 3: Tela Flutuante (Simples)
```
Fundo: Notebook Jupyter com gráficos
Frente: Janela flutuante/popup com script em teleprompter
  └─ Posicione na lateral, semi-transparente
  └─ Maximize quando precisar ler, minimize quando mostrar gráfico
```

---

## 📋 CHECKLIST DE NAVEGAÇÃO

Antes de começar a gravar:

- [ ] Notebook aberto e executado completamente
- [ ] Identifiquei as 6 células com gráficos (anotei números ou fiz favoritos)
- [ ] Testei a navegação (Ctrl+F para procurar)
- [ ] Teleprompter aberto com o script
- [ ] Telas/monitores configurados conforme escolhido
- [ ] Fiz um teste de "clique-e-mostre" (simular a gravação)

---

## 🆘 Se Perder Durante a Gravação

**Se não encontrar o gráfico a tempo:**

```
✓ Continue falando naturalmente
✓ Diga algo como: "Enquanto isso carrega..." 
✓ Pause a gravação, encontre o gráfico, recomece
✓ Edite depois para sincronia perfeita
```

**Se clicar no gráfico errado:**

```
✓ Você sabe? Continue como se nada acontecesse
✓ Diga: "Aqui a gente vê..." (descrevendo o que tem na tela)
✓ A audiência não saberá que "errou"
✓ (Ou pause, corrija, recomece)
```

**Se o notebook travar:**

```
✓ Você já executou tudo antes, certo?
✓ Pause, execute a célula novamente
✓ Continue a gravação
```

---

## 📚 Referência Rápida de Busca

Copie e cole no Ctrl+F para encontrar rapidinho:

```
Distribuição → procura: "diagnosis" ou "alvo"
Histogramas → procura: "radius_mean" ou "concavity_mean"  
Feature Importance → procura: "feature_importance" ou "permutation"
SHAP Beeswarm → procura: "beeswarm" ou "shap.summary"
Matrizes Confusão → procura: "confusion_matrix"
```

---

**Dica Final:** Execute o notebook uma vez ANTES de gravar para saber exatamente onde estão os gráficos. Não faça isso "ao vivo"! 😊

---

**Status:** ✅ PRONTO PARA NAVEGAR!
