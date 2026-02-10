import csv
import json

def carregar_dados(caminho):
    if caminho.endswith(".csv"):
        with open(caminho, newline='', encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return list(reader)

    elif caminho.endswith(".json"):
        with open(caminho, encoding="utf-8") as f:
            return json.load(f)

    else:
        raise ValueError("Formato não suportado")
