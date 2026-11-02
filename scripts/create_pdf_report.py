import os
from pathlib import Path
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, inch
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#555555"))
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 800, "POSTECH IA for Devs | Tech Challenge - Fase 1")
            self.setStrokeColor(colors.HexColor("#dddddd"))
            self.setLineWidth(0.5)
            self.line(54, 792, 541, 792)
        # Footer
        self.setStrokeColor(colors.HexColor("#dddddd"))
        self.setLineWidth(0.5)
        self.line(54, 45, 541, 45)
        page_str = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(541, 32, page_str)
        self.drawString(54, 32, "Relatório Técnico - Sistema Inteligente de Diagnóstico Citológico")
        self.restoreState()

def build_pdf():
    pdf_path = Path("tech_challenge/Relatorio_Tecnico_Tech_Challenge_Fase1.pdf")
    img_dir = Path("tech_challenge/imagens")
    
    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=A4,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#1a365d"),
        alignment=1, # Center
        spaceAfter=8
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#2b6cb0"),
        alignment=1,
        spaceAfter=15
    )
    
    h1_style = ParagraphStyle(
        'CustomH1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor("#1a365d"),
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'CustomH2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor("#2b6cb0"),
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#2d3748"),
        alignment=4, # Justify
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'CustomBullet',
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=3
    )

    callout_style = ParagraphStyle(
        'Callout',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#742a2a"),
        backColor=colors.HexColor("#fff5f5"),
        borderColor=colors.HexColor("#feb2b2"),
        borderWidth=1,
        borderPadding=6,
        spaceBefore=6,
        spaceAfter=8
    )

    table_header = ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=8.5, leading=11, textColor=colors.white, alignment=1)
    table_cell = ParagraphStyle('TC', fontName='Helvetica', fontSize=8, leading=10, textColor=colors.HexColor("#2d3748"), alignment=1)
    table_cell_left = ParagraphStyle('TCL', fontName='Helvetica', fontSize=8, leading=10, textColor=colors.HexColor("#2d3748"), alignment=0)
    table_cell_bold = ParagraphStyle('TCB', fontName='Helvetica-Bold', fontSize=8, leading=10, textColor=colors.HexColor("#1a365d"), alignment=1)

    story = []

    # Title & Metadata
    story.append(Paragraph("POSTECH IA FOR DEVS | TECH CHALLENGE - FASE 1", title_style))
    story.append(Paragraph("Sistema Inteligente de Suporte ao Diagnóstico Citológico e Triagem Oncológica", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#2b6cb0"), spaceAfter=10))

    # Link Info Box
    links_data = [
        [Paragraph("<b>Aluno:</b>", table_cell_left), Paragraph("Bruno Miranda de Araujo", table_cell_left)],
        [Paragraph("<b>Matrícula:</b>", table_cell_left), Paragraph("RM378093", table_cell_left)],
        [Paragraph("<b>Link do Repositório Git:</b>", table_cell_left), Paragraph('<font color="#2b6cb0"><u>https://github.com/brunomirandadev/pos-tech-ia-devs-tc-fase1.git</u></font>', table_cell_left)],
        [Paragraph("<b>Link do Dataset (Kaggle):</b>", table_cell_left), Paragraph('<font color="#2b6cb0"><u>https://www.kaggle.com/datasets/uciml/breast-cancer-wisconsin-data/data</u></font>', table_cell_left)],
        [Paragraph("<b>Vídeo de Demonstração (YouTube/Vimeo):</b>", table_cell_left), Paragraph('<font color="#c53030"><b>https://youtu.be/x-sVhvrblck</b></font>', table_cell_left)]
    ]
    t_links = Table(links_data, colWidths=[150, 337])
    t_links.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#edf2f7")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e0")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_links)
    story.append(Spacer(1, 10))

    # 1. Contexto e Desafio
    story.append(Paragraph("1. Contextualização do Problema Hospitalar", h1_style))
    story.append(Paragraph(
        "Em hospitais universitários e centros de referência oncológica, o volume contínuo de biópsias por Punção Aspirativa por Agulha Fina (PAAF) "
        "impõe um desafio crítico aos médicos patologistas. A análise morfológica visual de cada lâmina exige extremo rigor técnico e tempo substancial, "
        "gerando filas de espera onde dias de atraso no início da intervenção médica podem comprometer o prognóstico do paciente. "
        "A presente solução estabelece um <b>Sistema de Suporte à Decisão Clínica (CDSS - <i>Clinical Decision Support System</i>)</b> com aprendizado de máquina "
        "para realizar a triagem preliminar automatizada, ordenar prioridades de atendimento por gravidade e oferecer uma segunda opinião quantitativa e explicável.",
        body_style
    ))
    story.append(Paragraph(
        "<b>DIRETRIZ ÉTICA OBRIGATÓRIA:</b> O algoritmo atua estritamente como triagem e suporte auxiliar. "
        "A interpretação definitiva, o cruzamento com o histórico do paciente e a <b>palavra final sobre o laudo cabem sempre e exclusivamente ao médico especialista</b>.",
        callout_style
    ))

    # 2. EDA
    story.append(Paragraph("2. Análise Exploratória de Dados (EDA)", h1_style))
    story.append(Paragraph(
        "A base utilizada é a <i>Wisconsin Diagnostic Breast Cancer (WDBC)</i>, compreendendo <b>569 exames citológicos</b> e 30 atributos morfológicos "
        "extraídos de imagens digitalizadas dos núcleos celulares. Não foram identificados dados ausentes nas colunas preditoras nem registros duplicados.",
        body_style
    ))

    # Target Distribution
    story.append(Paragraph("2.1. Distribuição da Variável Alvo e Implicações de Amostragem", h2_style))
    story.append(Paragraph(
        "A base apresenta 357 casos Benignos (62.7%) e 212 casos Malignos (37.3%). Esse desbalanceamento moderado exige a aplicação "
        "de <b>amostragem estratificada (<i>stratify</i>)</b> em todas as etapas de partição dos dados, assegurando representatividade idêntica da patologia.",
        body_style
    ))
    if (img_dir / "01_distribuicao_alvo.png").exists():
        story.append(Image(str(img_dir / "01_distribuicao_alvo.png"), width=4.8*inch, height=2.4*inch))
        story.append(Spacer(1, 6))

    # Correlation Matrix
    story.append(Paragraph("2.2. Matriz de Correlação e Multicolinearidade", h2_style))
    story.append(Paragraph(
        "A análise de correlação linear (Pearson) revelou níveis extremos de multicolinearidade (r > 0.98) entre medidas geométricas interdependentes "
        "(como <i>radius</i>, <i>perimeter</i> e <i>area</i>). Em algoritmos lineares, a colinearidade distorce coeficientes pontuais, justificando "
        "a aplicação de penalização regularizada (L2) e técnicas robustas de interpretabilidade aditiva como o <b>SHAP</b>.",
        body_style
    ))
    if (img_dir / "02_matriz_correlacao.png").exists():
        story.append(Image(str(img_dir / "02_matriz_correlacao.png"), width=5.2*inch, height=3.3*inch))
        story.append(Spacer(1, 6))

    # Histograms
    story.append(Paragraph("2.3. Distribuições Morfológicas e Discriminação de Classes", h2_style))
    story.append(Paragraph(
        "Os histogramas demonstram que núcleos malignos (laranja) apresentam sistemático deslocamento para valores mais altos de raio, "
        "área e concavidade, refletindo o gigantismo e o polimorfismo nuclear típico de células cancerosas. A forte disparidade de escalas "
        "(área na casa dos milhares vs. suavidade na casa decimal) torna obrigatória a padronização das características.",
        body_style
    ))
    if (img_dir / "03_distribuicoes_morfologicas.png").exists():
        story.append(Image(str(img_dir / "03_distribuicoes_morfologicas.png"), width=5.8*inch, height=2.7*inch))
        story.append(Spacer(1, 8))

    # 3. Pré-processamento e Pipeline
    story.append(Paragraph("3. Pré-processamento e Estratégia de Partição dos Dados", h1_style))
    story.append(Paragraph(
        "Para garantir máxima fidelidade aos requisitos do edital e conformidade com os mais rigorosos padrões da ciência de dados, "
        "adotou-se a seguinte metodologia:",
        body_style
    ))
    story.append(Paragraph("• <b>Remoção de Colunas Espúrias:</b> Eliminação do identificador do paciente (<i>id</i>) e de colunas residuais de exportação (<i>Unnamed: 32</i>).", bullet_style))
    story.append(Paragraph("• <b>Codificação do Alvo:</b> Mapeamento estrito da classe clínica para notação computacional (Maligno = 1, Benigno = 0).", bullet_style))
    story.append(Paragraph("• <b>Separação em 3 Vias (Treino, Validação e Teste):</b> Os dados foram divididos em <b>70% Treino</b> (398 amostras), <b>15% Validação</b> (85 amostras) e <b>15% Teste</b> (86 amostras), ambos estratificados. O conjunto de validação serviu para selecionar modelos e hiperparâmetros, enquanto o conjunto de teste foi mantido completamente cego para a auditoria final.", bullet_style))
    story.append(Paragraph("• <b>Pipelines do Scikit-Learn:</b> A Regressão Logística usa <code>StandardScaler</code> dentro de um <code>Pipeline</code>, ajustado somente com os dados de treino. A Árvore de Decisão usa um pipeline sem padronização, pois esse modelo não depende da escala das variáveis.", bullet_style))
    story.append(Spacer(1, 8))

    # 4. Modelagem e Resultados
    story.append(Paragraph("4. Modelagem Preditiva e Avaliação Comparativa", h1_style))
    story.append(Paragraph(
        "Foram implementados e comparados dois modelos preditivos complementares: "
        "<b>Regressão Logística</b> (modelo linear que estima probabilidades, sem calibração adicional neste estudo) e <b>Árvore de Decisão</b> (modelo baseado em regras determinísticas com <code>max_depth=4</code> para controle de sobreajuste).",
        body_style
    ))

    # Metrics Table
    metrics_data = [
        [Paragraph("<b>Modelo Avaliado</b>", table_header), Paragraph("<b>Acurácia</b>", table_header), Paragraph("<b>Precisão</b>", table_header), Paragraph("<b>Recall (Sensibilidade)</b>", table_header), Paragraph("<b>F1-Score</b>", table_header), Paragraph("<b>ROC-AUC</b>", table_header)],
        [Paragraph("Regressão Logística (Validação)", table_cell_left), Paragraph("96.47%", table_cell), Paragraph("100.00%", table_cell), Paragraph("90.62%", table_cell), Paragraph("95.08%", table_cell), Paragraph("0.9965", table_cell)],
        [Paragraph("Árvore de Decisão (Validação)", table_cell_left), Paragraph("89.41%", table_cell), Paragraph("96.00%", table_cell), Paragraph("75.00%", table_cell), Paragraph("84.21%", table_cell), Paragraph("0.8777", table_cell)],
        [Paragraph("<b>Regressão Logística (Teste Final)</b>", table_cell_left), Paragraph("<b>97.67%</b>", table_cell_bold), Paragraph("<b>96.88%</b>", table_cell_bold), Paragraph("<b>96.88%</b>", table_cell_bold), Paragraph("<b>96.88%</b>", table_cell_bold), Paragraph("<b>0.9988</b>", table_cell_bold)],
        [Paragraph("Árvore de Decisão (Teste Final)", table_cell_left), Paragraph("91.86%", table_cell), Paragraph("96.30%", table_cell), Paragraph("81.25%", table_cell), Paragraph("88.14%", table_cell), Paragraph("0.9413", table_cell)]
    ]
    t_metrics = Table(metrics_data, colWidths=[150, 65, 65, 80, 65, 62])
    t_metrics.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1a365d")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e0")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('BACKGROUND', (0,3), (-1,3), colors.HexColor("#ebf8ff")),
    ]))
    story.append(t_metrics)
    story.append(Spacer(1, 8))

    # Discussão Médica do Recall
    story.append(Paragraph("4.1. Discussão Médica Crítica sobre a Métrica Principal (Recall)", h2_style))
    story.append(Paragraph(
        "No diagnóstico de câncer de mama, a assimetria do custo do erro é brutal. Um <b>Falso Negativo (FN)</b> representa uma paciente com câncer "
        "que é incorretamente liberada como saudável, postergando o tratamento e reduzindo drasticamente as chances de cura. "
        "Já um <b>Falso Positivo (FP)</b> acarreta ansiedade passageira e biópsias confirmatórias, sem ameaça iminente à vida. "
        "Portanto, o <b>Recall (Sensibilidade) é a métrica primordial</b>. A Regressão Logística alcançou <b>96.88% de Recall</b> no teste cego, "
        "cometendo apenas 1 falso negativo em 32 casos malignos, superando com folga a Árvore de Decisão (6 falsos negativos).",
        body_style
    ))
    if (img_dir / "04_matrizes_confusao.png").exists():
        story.append(Image(str(img_dir / "04_matrizes_confusao.png"), width=5.6*inch, height=2.3*inch))
        story.append(Spacer(1, 8))

    # 5. Interpretabilidade & SHAP
    story.append(Paragraph("5. Interpretabilidade Clínica: Feature Importance e SHAP", h1_style))
    story.append(Paragraph(
        "Para mitigar o risco de modelos 'caixa-preta' em saúde pública, foram empregadas duas frentes de auditoria preditiva: "
        "a <b>Feature Importance tradicional</b> (baseada na impureza Gini e magnitude de coeficientes) e o <b>SHAP (<i>SHapley Additive exPlanations</i>)</b>, "
        "fundamentado na teoria dos jogos cooperativos.",
        body_style
    ))
    if (img_dir / "05_feature_importance.png").exists():
        story.append(Image(str(img_dir / "05_feature_importance.png"), width=5.6*inch, height=2.2*inch))
        story.append(Spacer(1, 6))

    story.append(Paragraph("5.1. Explicabilidade Avançada com SHAP", h2_style))
    story.append(Paragraph(
        "Os gráficos globais foram calculados para a Regressão Logística selecionada. O gráfico de barras resume a magnitude média das contribuições "
        "e o <i>Beeswarm</i> mostra sua distribuição e direção no conjunto de teste. <b><code>texture_worst</code></b> tem a maior magnitude média, "
        "seguida por <code>radius_se</code>, <code>radius_worst</code>, <code>area_worst</code> e <code>symmetry_worst</code>. Valores altos de "
        "<code>texture_worst</code> tendem a elevar a saída do modelo para a classe maligna. Isso descreve associações aprendidas, não causalidade.",
        body_style
    ))
    if (img_dir / "06_shap_summary_bar.png").exists() and (img_dir / "07_shap_beeswarm.png").exists():
        story.append(Image(str(img_dir / "06_shap_summary_bar.png"), width=5.4*inch, height=2.5*inch))
        story.append(Spacer(1, 4))
        story.append(Image(str(img_dir / "07_shap_beeswarm.png"), width=5.4*inch, height=2.5*inch))
        story.append(Spacer(1, 8))

    story.append(PageBreak())
    story.append(Paragraph("5.2. Explicações locais em exemplos do conjunto de teste", h2_style))
    story.append(Paragraph(
        "Os gráficos <i>Waterfall</i> mostram como as características contribuem para a saída da Regressão Logística em dois casos de teste "
        "corretamente classificados: um maligno e um benigno. Os exemplos foram escolhidos entre as previsões corretas de cada classe, "
        "priorizando as mais próximas do limiar 0.5. As entradas estão padronizadas e as contribuições se somam na escala de <i>log-odds</i>. "
        "Em termos simples, log-odds é um placar interno: contribuições positivas empurram a saída para maligno e negativas para benigno; "
        "depois o placar é convertido na probabilidade mostrada no título. Log-odds não é porcentagem. São exemplos ilustrativos, "
        "não uma avaliação adicional de desempenho nem um diagnóstico clínico.",
        body_style
    ))
    if (img_dir / "08_shap_local_maligno.png").exists():
        story.append(Image(str(img_dir / "08_shap_local_maligno.png"), width=6.2*inch, height=3.3*inch))
        story.append(Spacer(1, 6))
    if (img_dir / "09_shap_local_benigno.png").exists():
        story.append(Image(str(img_dir / "09_shap_local_benigno.png"), width=6.2*inch, height=3.3*inch))
        story.append(Spacer(1, 8))

    story.append(PageBreak())

    # 6. Conclusões e Implantação
    story.append(Paragraph("6. Conclusões e Diretrizes de Implantação Hospitalar", h1_style))
    story.append(Paragraph(
        "O sistema inteligente atingiu resultados de alta robustez técnica e alinhamento com a rotina de patologia clínica:",
        body_style
    ))
    story.append(Paragraph("1. <b>Fila de Triagem Prioritária (LIS/PACS):</b> O modelo deve ser acoplado ao sistema de prontuários do hospital. Pacientes cujo exame apresentar probabilidade calculada de malignidade acima de um patamar seguro são automaticamente alocados no topo da lista de laudos prioritários do patologista.", bullet_style))
    story.append(Paragraph("2. <b>Seleção do Limiar de Decisão:</b> Qualquer ajuste do limiar deve ser escolhido com base no conjunto de validação, considerando o equilíbrio entre Recall e falsos positivos. O desempenho final deve ser medido no conjunto de teste, sem atribuir um resultado de Recall a um limiar que não foi avaliado.", bullet_style))
    story.append(Paragraph("3. <b>Auditoria Médica Caso a Caso:</b> Este relatório inclui dois exemplos SHAP locais para ilustrar as contribuições do modelo. Uma integração clínica deve gerar explicações locais por caso, validar sua apresentação e manter a revisão do médico especialista.", bullet_style))
    story.append(Spacer(1, 6))

    # 7. Instruções de Execução
    story.append(Paragraph("7. Instruções de Execução e Reprodutibilidade", h1_style))
    story.append(Paragraph(
        "O repositório foi estruturado para reprodução integral em ambiente Docker ou localmente com <code>uv</code>:<br/>"
        "• <b>Via Docker:</b> <code>docker build -t tech-challenge-fase1 .</code> e <code>docker run -p 8888:8888 tech-challenge-fase1</code><br/>"
        "• <b>Via Script Python Local:</b> <code>python scripts/analise_diagnostico.py</code><br/>"
        "• <b>Via Jupyter Notebook:</b> Execução interativa através de <code>notebook/analise_diagnostico.ipynb</code>.",
        body_style
    ))

    # Build PDF
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF Report generated successfully at: {pdf_path}")

if __name__ == "__main__":
    build_pdf()

