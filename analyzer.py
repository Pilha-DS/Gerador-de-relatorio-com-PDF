from collections import Counter

def analisar_dados_completo(dados):
    if not dados:
        return {}

    resultado = {}
    colunas = dados[0].keys()

    for coluna in colunas:
        valores = []
        numericos = True

        for linha in dados:
            valor = linha.get(coluna)
            if valor is None or valor == "":
                continue
            try:
                valor_float = float(valor)
                valores.append(valor_float)
            except:
                numericos = False
                valores.append(str(valor))

        if not valores:
            resultado[coluna] = None
            continue

        # Coluna numérica
        if numericos:
            resultado[coluna] = {
                "tipo": "Numérica",
                "total": len(valores),
                "media": round(sum(valores) / len(valores), 2),
                "min": min(valores),
                "max": max(valores)
            }
        else:
            contagem = Counter(valores)
            mais_comum = contagem.most_common(1)[0]
            resultado[coluna] = {
                "tipo": "Categórica",
                "total": len(valores),
                "valores_unicos": len(contagem),
                "mais_comum": f"{mais_comum[0]} ({mais_comum[1]}x)",
                "frequencias": dict(contagem)
            }

    return resultado
