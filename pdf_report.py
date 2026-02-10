from fpdf import FPDF

def normalizar_texto(texto):
    if texto is None:
        return ""
    return str(texto).encode("latin-1", errors="ignore").decode("latin-1")

def gerar_pdf_completo(caminho, dados, analise):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, normalizar_texto("Relatório Completo de Análise de Dados"), ln=True)
    pdf.ln(5)

    # ===== Seção individual de cada coluna =====
    for coluna, stats in analise.items():
        if not stats:
            continue

        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 8, normalizar_texto(f"Coluna: {coluna}"), ln=True)

        pdf.set_font("Arial", "", 12)
        pdf.cell(0, 6, normalizar_texto(f"Tipo: {stats['tipo']}"), ln=True)

        for chave, valor in stats.items():
            if chave in ["tipo", "frequencias"]:
                continue
            pdf.cell(0, 6, normalizar_texto(f"{chave.capitalize()}: {valor}"), ln=True)

        if stats["tipo"] == "Categórica":
            pdf.ln(2)
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 6, normalizar_texto("Frequência dos valores:"), ln=True)
            pdf.set_font("Arial", "", 11)
            for valor, qtd in stats["frequencias"].items():
                pdf.multi_cell(0, 5, normalizar_texto(f"{valor}: {qtd}"))

        # Linha separadora
        pdf.ln(5)
        pdf.set_draw_color(0, 0, 0)
        pdf.set_line_width(0.3)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(5)

    # ===== Resumo Consolidado =====
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, normalizar_texto("Resumo Consolidado (Todos os Valores)"), ln=True)
    pdf.ln(3)

    colunas = list(dados[0].keys())
    n_colunas = len(colunas)
    largura = max(30, 180 // n_colunas)  # largura mínima 30mm

    # Cabeçalho
    pdf.set_font("Arial", "B", 12)
    for c in colunas:
        x = pdf.get_x()
        y = pdf.get_y()
        pdf.multi_cell(largura, 6, normalizar_texto(c), border=1)
        pdf.set_xy(x + largura, y)
    pdf.ln(6)

    # Linhas da tabela
    pdf.set_font("Arial", "", 10)
    for linha in dados:
        y_inicial = pdf.get_y()
        x_inicial = pdf.get_x()
        alturas = []

        # calcula altura máxima das células da linha
        for c in colunas:
            texto = normalizar_texto(linha.get(c, ""))
            n_linhas = texto.count("\n") + 1
            alturas.append(n_linhas * 6)
        altura_linha = max(alturas)

        # nova página se necessário
        if pdf.get_y() + altura_linha > pdf.page_break_trigger:
            pdf.add_page()
            y_inicial = pdf.get_y()

        x = 10
        for c in colunas:
            pdf.set_xy(x, y_inicial)
            pdf.multi_cell(largura, 6, normalizar_texto(linha.get(c, "")), border=1)
            x += largura

        pdf.ln(altura_linha)

    pdf.output(caminho)
