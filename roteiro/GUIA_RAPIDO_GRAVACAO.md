# 🎬 GUIA RÁPIDO - USAR O SCRIPT NA GRAVAÇÃO

## ⚡ Em 30 Segundos

1. Abra o arquivo `SCRIPT_TELEPROMPTER_10MIN.md`
2. Configure um teleprompter (software gratuito: 
   - **Online:** teleprompter.com ou prompt.so
   - **Desktop:** Teleprompter Premium ou PromptSmart
   - **Simples:** Abra em tela cheia e role com scroll)
3. Aumente a fonte para legibilidade (tamanho 28-32)
4. Configure velocidade auto-scroll (lento, natural)
5. Grave! ✅

---

## 📋 Leitura Passo-a-Passo

### Ao Começar ✅

```
🎬 ABERTURA (30 seg)
├─ Apresentação com seu nome
├─ Explique o problema (filas, demora)
├─ Apresente a solução (IA como assistente)
└─ Reforce: IA não substitui, é ferramenta
```

**Dica:** Olhe para câmera nessa parte, não para o teleprompter!

---

### Bloco 1: OS DADOS (1 min)

```
📊 BLOCO 1
├─ [MOSTRAR GRÁFICO #1: Distribuição da Classe Alvo]
│  └─ Explique 63% benigno, 37% maligno
│
├─ Mencione 569 amostras e 32 características
│
└─ [MOSTRAR GRÁFICO #2: Distribuições Morfológicas]
   └─ Explique os 3 histogramas (Raio, Concavidade, Textura)
```

**Timing:** Não apresse! Deixe o espectador absorver cada gráfico.

---

### Bloco 2: PREPARAÇÃO E TREINO (2 min)

```
🤖 BLOCO 2
├─ Explique divisão 70-15-15 (Treino-Val-Teste)
│
├─ [SEM GRÁFICO] Fale os números dos modelos:
│  ├─ Regressão Logística: 98%, 97%, 97%
│  └─ Árvore Decisão: 92%, 81%, 96%
│
└─ Justifique escolha da Regressão Logística
```

**Dica:** Use as pausas para deixar os números "pegarem"!

---

### Bloco 3: EXPLICABILIDADE (4:30 min)

```
🔍 BLOCO 3 - PARTE A: Features Importantes
├─ [MOSTRAR GRÁFICO #3: Feature Importance]
│  ├─ Árvore de Decisão: perimeter_worst, concave points_worst, texture_worst
│  └─ Regressão Logística: texture_worst, radius_se, symmetry_worst
│
└─ Explique que são rankings dos modelos, não relações causais

BLOCO 3 - PARTE B: SHAP Global
├─ [MOSTRAR GRÁFICO #4: SHAP Beeswarm]
│  ├─ Explique cores (azul=baixo, vermelho=alto)
│  ├─ Explique posição (contribuição negativa/positiva para a saída)
│  └─ Destaque texture_worst no ranking da Regressão Logística
│
└─ [MOSTRAR GRÁFICO #5: SHAP Bar global]
   └─ Compare a magnitude média das contribuições

BLOCO 3 - PARTE C: Exemplos Individuais
├─ [MOSTRAR GRÁFICO #6: Waterfall SHAP - caso maligno]
│  └─ Explique a probabilidade prevista e as contribuições em log-odds
│
├─ [MOSTRAR GRÁFICO #7: Waterfall SHAP - caso benigno]
│  └─ Compare contribuições que elevam ou reduzem a saída
│
└─ Reforce: exemplos ilustrativos, revisão médica continua necessária

BLOCO 3 - PARTE D: Avaliação
└─ [MOSTRAR GRÁFICO #8: Matrizes de Confusão]
```

**⚠️ Importante:** Este é o bloco mais longo. Não apresse!

---

### Bloco 4: COMO FUNCIONA (1 min)

```
🏥 BLOCO 4
├─ Cenário real: paciente → exame → análise → priorização
├─ Ganhos práticos: velocidade, segurança, auditoria
├─ Flexibilidade: pode ajustar threshold se necessário
└─ [SEM GRÁFICO] Apenas fale
```

---

### Encerramento (30 seg)

```
✅ ENCERRAMENTO
├─ Resuma: 569 amostras, 98%, 97%, interpretável
├─ Cite recursos: GitHub, Relatório Técnico, Dataset
└─ Agradeça e finalize
```

**Dica:** Olhe para câmera de novo aqui! Cria conexão com espectador.

---

## 🎯 Checklist Durante a Gravação

### Antes de Começar
- [ ] Câmera ligada e estável
- [ ] Teleprompter configurado e legível
- [ ] Áudio testado (sem ruído)
- [ ] Iluminação boa
- [ ] 8 gráficos de vídeo prontos para exibição
- [ ] Script aberto na tela
- [ ] Fez respiração profunda 😊

### Durante a Gravação
- [ ] Fale naturalmente (não roboticamente)
- [ ] Respeite [PAUSA X seg] — deixe tempo de silêncio
- [ ] Olhe para câmera na Abertura e Encerramento
- [ ] Olhe para teleprompter no meio
- [ ] Clique em gráficos quando vê [MOSTRAR GRÁFICO]
- [ ] Não acelerem! Fluxo natural é melhor

### Se Errar
- [ ] Pause a gravação
- [ ] Respire fundo
- [ ] Recomece do último [PAUSA] ou seção
- [ ] Edição depois da é sua amiga 😊

---

## 🎨 Dicas de Apresentação

| Elemento | Recomendação |
|----------|--------------|
| **Velocidade** | Fale como se explicasse para um colega inteligente (natural) |
| **Volume** | Constante, audível, sem gritar |
| **Ênfase** | Acentue números (98%, 97%, 81%) e conclusões importantes |
| **Gestos** | Aponte para gráficos quando citá-los |
| **Expressão** | Engaje-se com o conteúdo, mostre entusiasmo |
| **Postura** | Ombros relaxados, coluna reta |
| **Respiração** | Respire entre blocos, não no meio de frase |

---

## 🆘 Troubleshooting Rápido

**Problema:** Teleprompter muito rápido ou lento
**Solução:** Ajuste velocidade auto-scroll no software ou role manualmente

**Problema:** Esqueci uma palavra
**Solução:** Pausa, respira, continua do próximo [PAUSA]. Edita depois.

**Problema:** Gráfico demora para carregar
**Solução:** Clique antecipadamente, continue falando. Sincronize depois na edição.

**Problema:** Perdi a noção do timing
**Solução:** Não se preocupe! Grave tudo e edite. Melhor 15 min completo que 10 min incompleto.

**Problema:** Sombreado está contra-luz
**Solução:** Mude a iluminação ou ângulo da câmera. Teste antes de começar!

---

## ✅ Pós-Gravação

1. ✅ Revise a gravação completa
2. ✅ Se ficou muito longo, edite ou acelere a 1.15x
3. ✅ Confira áudio (sem ruído, volume OK)
4. ✅ Confira sincronismo dos gráficos
5. ✅ Adicione créditos/legendas se desejar
6. ✅ Exporte em qualidade HD (1080p+)
7. ✅ Upload no YouTube/apresentação

---

## 📞 Precisa de Ajuda?

- Script confuso? Veja `SCRIPT_TELEPROMPTER_10MIN.md` completo
- Timing? Veja `VALIDACAO_FINAL_SCRIPT.md`
- Estrutura? Veja `ROTEIRO_VIDEO_10MIN.md`
- Dados do notebook? Veja `notebook/analise_diagnostico.ipynb`

---

**BOM SORTE NA GRAVAÇÃO! 🎬🚀**

Você vai mandar bem! 💪
