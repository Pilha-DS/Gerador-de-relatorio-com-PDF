import json
import random
import string

def gerar_nome_aleatorio(tamanho=50):
    """Gera um nome de campo aleatório com letras."""
    return ''.join(random.choices(string.ascii_letters, k=tamanho))

def gerar_valor_aleatorio():
    """Gera um valor aleatório que pode ser string, número ou booleano."""
    tipo = random.choice(['int', 'float', 'str', 'bool'])
    if tipo == 'int':
        return random.randint(0, 1000)
    elif tipo == 'float':
        return round(random.uniform(0, 1000), 2)
    elif tipo == 'str':
        return ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    else:
        return random.choice([True, False])

def gerar_json(linhas=1000000, colunas=10):
    """Gera um JSON com a quantidade de linhas e colunas especificadas."""
    resultado = []
    for _ in range(linhas):
        linha = {gerar_nome_aleatorio(): gerar_valor_aleatorio() for _ in range(colunas)}
        resultado.append(linha)
    return resultado

if __name__ == "__main__":
    linhas = int(input("Quantidade de linhas: "))
    colunas = int(input("Quantidade de colunas: "))
    dados = gerar_json(linhas, colunas)
    
    # Exibir JSON formatado
    print(json.dumps(dados, indent=4))
    
    # Opcional: salvar em arquivo
    with open("dados_aleatorios.json", "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)
