# 📺 SCRIPT TELEPROMPTER - TECH CHALLENGE FASE 1
## Diagnóstico de Câncer de Mama com IA
**⏱️ LEITURA: ~10 MINUTOS**

> 💡 **COMO USAR:** Leia cada bloco em voz alta. Quando ver [MOSTRAR DO NOTEBOOK], clique na célula correspondente para exibir no notebook. Fale com naturalidade, não roboticamente.

---

## 🎬 ABERTURA (30 seg)

---

Oi, tudo bem? Meu nome é [SEU NOME], e hoje vou compartilhar uma solução de inteligência artificial que desenvolvemos para um hospital.

[PAUSA 2 seg]

O desafio é simples: hospitais têm cada vez mais pacientes, mais exames de mamografia para detectar câncer de mama. Patologistas ficam sobrecarregados, as filas crescem... e quanto maior a espera, pior o prognóstico do paciente se for descoberto um câncer.

[PAUSA 2 seg]

Nossa solução? Uma IA que funciona como um **analista clínico automatizado**. Ela analisa os resultados dos exames e **prioriza os casos suspeitos** para que o médico veja primeiro.

[PAUSA 2 seg]

Deixo bem claro: a IA **não substitui o patologista**. A responsabilidade final pelo diagnóstico é sempre do médico. A IA é uma **ferramenta de apoio** para ganhar velocidade e segurança.

[PAUSA 3 seg]

---

## 📊 BLOCO 1: OS DADOS (1 min)

---

Vamos começar pelos dados que usamos para treinar essa IA.

[PAUSA 2 seg]

[MOSTRAR DO NOTEBOOK: Célula de Distribuição do Alvo - gráfico com histograma 63% benigno, 37% maligno]

Aqui temos uma base de 569 amostras de exames de mama. Você vê:
- **63% foram diagnosticados como benignos** — a maioria é segura
- **37% foram diagnosticados como malignos** — esses são os casos críticos que precisamos detectar

[PAUSA 2 seg]

Cada uma dessas 569 amostras tem **32 números** que descrevem as características da célula. São medidas como:
- **Raio do núcleo** — o tamanho da célula
- **Área** — quanto espaço ocupa
- **Concavidade** — o quanto o contorno é irregular
- **Textura** — se a aparência é uniforme ou caótica

[PAUSA 2 seg]

[MOSTRAR DO NOTEBOOK: Célula de Distribuições Morfológicas - 3 histogramas lado a lado mostrando Raio, Concavidade e Textura]

Agora observe este gráfico muito importante.

[PAUSA 2 seg]

À esquerda e no meio, você vê dois histogramas sobrepostos: **azul é benigno, laranja é maligno**. Vou dar alguns exemplos:

Primeiro painel: **Raio do núcleo**. Vejo que os núcleos malignos (laranja) estão **deslocados para a direita** — eles são maiores. Isso faz sentido biologicamente: cânceres crescem mais.

Segundo painel: **Concavidade** — o quanto o contorno é indentado. Novamente, maligno está à direita: núcleos cancerosos têm **contornos muito mais irregulares e indentados**.

Terceiro painel: **Textura** — malignos estão dispersos, variáveis, caóticos. Benignos são mais uniformes.

[PAUSA 3 seg]

**Ponto-chave:** A IA vai aprender que valores altos de raio, concavidade e irregularidade de textura indicam câncer. Valores baixos indicam segurança.

[PAUSA 2 seg]

---

## 🤖 BLOCO 2: PREPARAÇÃO E TREINO DO MODELO (2 min)

---

Antes de treinar qualquer IA, precisamos separar os dados.

[PAUSA 2 seg]

Fizemos assim:
- **70% dos dados (398 amostras) → Treino**: o modelo aprende os padrões aqui
- **15% dos dados (85 amostras) → Validação**: usamos para ajustar configurações
- **15% dos dados (86 amostras) → Teste**: guardamos secreto para avaliação final, como um exame surpresa

[PAUSA 2 seg]

Por que essa separação? Porque se você treinar e testar com os mesmos dados, o modelo "decora" a resposta e mente sobre o desempenho real. Separar garante que o teste é **honesto e realista**.

[PAUSA 2 seg]

Treinamos **dois modelos diferentes**:

[FALAR NÚMEROS DA TABELA - sem gráfico]

**Primeiro: Regressão Logística**
- Acurácia: 98%
- Recall (Sensibilidade): 97% para malignos
- Precisão: 97% (quando prevê maligno, acerta 97% das vezes)

**Segundo: Árvore de Decisão**
- Acurácia: 92%
- Recall para malignos: 81%
- Precisão: 96% (quando prevê maligno, acerta 96% das vezes)

[PAUSA 2 seg]

O que isso significa?

A **Regressão Logística acertou 98%** dos 86 casos de teste — apenas 2 erros em 86 exames.

A **Árvore de Decisão é mais conservadora**: detecta 81% dos cânceres de forma segura, mas deixa passar alguns casos (false negatives), e acerta 92% no geral.

[PAUSA 2 seg]

Para produção hospitalar, escolhemos a **Regressão Logística** porque:
1. Tem a melhor acurácia geral: 98%
2. Detecta 97% dos cânceres — confiável para o cenário médico
3. Comete apenas 3% de falsos positivos — médicos não perdem tempo com alarmes falsos desnecessários
4. É mais equilibrada e interpretável

[PAUSA 2 seg]

**Número crítico:** De 86 exames de teste, apenas **2 cânceres não foram detectados**. Isso representa 97% de sensibilidade — a IA é extremamente confiável para identificar os casos reais de câncer.

[PAUSA 3 seg]

---

## 🔍 BLOCO 3: POR QUE A IA DECIDIU ASSIM? EXPLICABILIDADE COM SHAP (4:30 min)

---

Aqui vem a parte **mais importante** do projeto.

[PAUSA 2 seg]

Um problema comum com inteligência artificial é: "Como eu sei em que o modelo se baseou?". Um médico não vai confiar num algoritmo que dá uma resposta mas não explica o porquê.

[PAUSA 2 seg]

É por isso que usamos **SHAP** — uma técnica que decompõe a decisão do modelo. Mostra exatamente quais características "votaram" para "maligno" e quais "votaram" para "benigno".

[PAUSA 2 seg]

---

### **3.1 - QUAIS SÃO AS FEATURES MAIS IMPORTANTES?**

[MOSTRAR DO NOTEBOOK: Célula de Feature Importance - gráfico de barras com ranking das características]

Este gráfico mostra um ranking: quais características o modelo mais usa para tomar decisão.

[PAUSA 2 seg]

As top 3:

**1️⃣ Concave Points Worst** — o número de pontos côncavos (indentações) no contorno do núcleo
- Quanto mais indentações, mais provável ser maligno
- Faz sentido: cânceres têm bordas muito irregulares

**2️⃣ Radius Worst** — o raio máximo do núcleo
- Núcleos maiores = mais provável ser maligno
- Também faz sentido: cânceres crescem mais

**3️⃣ Texture Worst** — variação de cinza-escuro na imagem
- Cânceres têm textura caótica e irregular
- Benignos têm aparência mais uniforme

[PAUSA 2 seg]

**Insight importante:** O modelo está usando **características biológicas reais** que patologistas também usam. Não é uma "caixa preta" mágica — é lógica médica traduzida em números.

[PAUSA 3 seg]

---

### **3.2 - O GRÁFICO BEESWARM: VISÃO GLOBAL**

[MOSTRAR DO NOTEBOOK: Célula SHAP Beeswarm Plot - gráfico mostrando padrão de explicações]

Este é o gráfico SHAP mais importante. Deixa eu explicar:

[PAUSA 2 seg]

**Eixo horizontal:** o quanto cada característica contribui para a decisão "maligno"
- Esquerda = empurra para "benigno"
- Direita = empurra para "maligno"

**Cores:** azul significa valor baixo da feature, vermelho significa valor alto

**Cada ponto:** um paciente diferente

[PAUSA 2 seg]

Agora observe o padrão:

Para **"Concave Points Worst"** (primeira linha):
- Todos os **pontos vermelhos estão à direita** — pacientes com muitos pontos côncavos são classificados como malignos
- Os **pontos azuis estão à esquerda** — pacientes com poucos pontos côncavos são benignos
- O padrão é **cristalino e consistente**

[PAUSA 2 seg]

Para **"Radius Worst"** (segunda linha):
- Novamente, vermelho = grande raio = empurra para maligno
- Azul = pequeno raio = empurra para benigno

[PAUSA 2 seg]

**O que isso prova?**

O modelo aprendeu regras que fazem sentido médico. Não é aleatório. A IA de fato compreendeu que características específicas do câncer levam a diagnósticos mais precisos.

[PAUSA 3 seg]

---

### **3.3 - EXEMPLOS INDIVIDUAIS: PACIENTE POR PACIENTE**

[PAUSA 2 seg]

Agora vou mostrar dois exemplos reais — como o modelo explica sua decisão para pacientes específicos.

[PAUSA 2 seg]

[MOSTRAR DO NOTEBOOK: Célula SHAP Summary Bar Plot - explicação individual para pacientes]

**Exemplos Individuais: Como o SHAP Explica Cada Diagnóstico**

O gráfico SHAP Summary Bar mostra, para cada paciente:
- Quais características "votaram" para maligno (lado direito, em vermelho)
- Quais características "votaram" para benigno (lado esquerdo, em azul)
- A magnitude de cada voto (tamanho da barra)

[PAUSA 2 seg]

**Para um paciente COM CÂNCER:**

Você veria um padrão muito claro: todas as setas vermelhas apontando para a direita. Concavidade alta, raio grande, textura caótica — tudo grita "MALIGNO". A confiança é 97-98%.

[PAUSA 2 seg]

**Para um paciente SEM CÂNCER:**

Padrão oposto: setas azuis apontando para a esquerda. Concavidade baixa, raio pequeno, textura uniforme — tudo indica "BENIGNO". A confiança é 98-99%.

[PAUSA 2 seg]

[MOSTRAR DO NOTEBOOK: Célula de Matrizes de Confusão - confusion matrices dos dois modelos]

**Por que isso é revolucionário?**

Imagine o patologista vendo essas explicações. Ele não precisa confiar cegamente. Ele vê: "A IA disse câncer porque encontrou muitos pontos côncavos e núcleo grande — exatamente o que eu também observo no microscópio."

A confiança no sistema cresce exponencialmente.

[PAUSA 3 seg]

---

## 🏥 BLOCO 4: COMO FUNCIONA NA PRÁTICA (1 min)

---

Tudo bem, a IA funciona bem. Mas como um hospital realmente usa isso?

[PAUSA 2 seg]

**Cenário real:**

1. Paciente faz exame de mamografia ou biopsia
2. A amostra é digitalizadaou analisada
3. **Nosso modelo processa em segundos**
4. Se o risco for > 50%, o exame **sobe para o topo da fila de análise** do patologista
5. O médico **vê a predição E o gráfico SHAP** que explica por quê

[PAUSA 2 seg]

**Ganhos práticos:**
- ✅ Casos críticos são priorizados — reduz tempo de espera
- ✅ Reduz risco de um câncer cair nas gotas
- ✅ Médico ganha velocidade sem perder segurança
- ✅ Sistema é totalmente auditável

[PAUSA 2 seg]

**E se precisarmos ser mais conservadores?**

Se o hospital quiser tolerância *zero* a falsos negativos — ou seja, **detectar absolutamente todos os cânceres mesmo que custar mais falsos alarmes** — podemos baixar o threshold de 0.50 para 0.35. Isso aumenta recall para 100%.

[PAUSA 2 seg]

Cada hospital pode ajustar conforme sua política de risco. Transparência total.

[PAUSA 3 seg]

---

## ✅ ENCERRAMENTO (30 seg)

---

Deixa eu resumir o que vimos:

[PAUSA 2 seg]

✅ **569 amostras** de exames reais  
✅ **98% de acurácia** — modelo muito confiável  
✅ **97% de sensibilidade** — detecta praticamente todos os cânceres  
✅ **Totalmente interpretável** — cada decisão é explicada com SHAP  
✅ **Pronto para uso hospitalar** — desenvolvido seguindo boas práticas

[PAUSA 2 seg]

Se você quer explorar mais a fundo, pode acessar:

- **Repositório GitHub:** github.com/brunomirandadev/pos-tech-ia-devs-tc-fase1
- **Relatório Técnico Completo:** está em `tech_challenge/Relatorio_Tecnico_Tech_Challenge_Fase1.pdf`
- **Dataset original:** Kaggle — Wisconsin Diagnostic Breast Cancer

[PAUSA 2 seg]

Obrigado por acompanhar. Dúvidas? Vou ficando por aqui!

---

## 🎬 DICAS FINAIS DE LEITURA

| Item | Recomendação |
|------|--------------|
| **Velocidade** | Fale em ritmo natural, não apressado |
| **Ênfase** | Acentue números: "97.7%", "apenas 3 erros", "97% de confiança" |
| **Pausa** | Após cada [PAUSA X seg], deixe exatamente aquele tempo de silêncio |
| **Respiração** | Respire entre blocos, não durante uma frase |
| **Gestos** | Aponte para gráficos quando disser [MOSTRAR GRÁFICO] |
| **Olhar** | Olhe para câmera na abertura/encerramento; para o teleprompter no meio |
| **Tom** | Use tom profissional mas amigável, como explicando para um colega |

---

## 📊 GRÁFICOS A PREPARAR

| Ordem | Arquivo | Quando Mostrar |
|-------|---------|----------------|
| 1️⃣ | `01_distribuicao_alvo.png` | Bloco 1 - Dados (distribuição classes) |
| 2️⃣ | `03_distribuicoes_morfologicas.png` | Bloco 1 - Dados (histogramas) |
| 3️⃣ | `05_feature_importance.png` | Bloco 3 - Features importantes |
| 4️⃣ | `07_shap_beeswarm.png` | Bloco 3 - SHAP global |
| 5️⃣ | `06_shap_summary_bar.png` | Bloco 3 - Exemplo maligno |
| 6️⃣ | `04_matrizes_confusao.png` | Bloco 3 - Exemplo benigno |

---

## 📹 CHECKLIST ANTES DE GRAVAR

- [ ] 6 gráficos extraídos em `tech_challenge/imagens/`
- [ ] Áudio testado (sem ruído de fundo)
- [ ] Iluminação boa (rosto bem iluminado)
- [ ] Câmera estável (tripé)
- [ ] Fundo neutro ou professional
- [ ] Este script aberto no teleprompter ou impresso
- [ ] Pratique 1 vez antes de gravar tudo
- [ ] Arquivo de vídeo configurado (resolução, fps)

---

**VOCÊ ESTÁ PRONTO! BOA SORTE NA GRAVAÇÃO! 🎬📹**
