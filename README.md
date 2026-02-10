<img src="https://img.shields.io/badge/Python-3+-blue.svg"> <img src="https://img.shields.io/badge/pyQT6+-red.svg">
# Gerador de Relatórios em PDF - Análise de Dados com PyQt6

## Descrição

Este projeto é um **sistema desktop em Python** que permite importar arquivos de dados (CSV ou JSON), analisar todas as variáveis automaticamente e gerar **relatórios simples em PDF**.  

O sistema identifica o tipo de cada coluna (numérica ou categórica), calcula estatísticas relevantes, mostra frequências de valores para colunas categóricas e inclui uma tabela consolidada com todos os dados.

O objetivo é facilitar a visualização e análise de conjuntos de dados de forma **rápida e profissional**, sem depender de bibliotecas externas de fontes ou gráficos.

---

## Funcionalidades

- Interface gráfica em **PyQt6**
- Suporte a arquivos **CSV** e **JSON**
- Análise automática de todas as variáveis
  - Colunas numéricas: total, média, mínimo, máximo
  - Colunas categóricas: total, valores únicos, valor mais comum, frequência de cada valor
- Relatório PDF gerado:
  - Seção individual para cada coluna
  - Separadores visuais entre variáveis
  - Seção final consolidando todas as variáveis em uma tabela
- Suporte a **valores longos e múltiplas páginas**
- Uso de **caracteres padrão**, sem necessidade de fontes externas
- Quebra automática de páginas e células

---

## Estrutura do Projeto

```
gerador_relatorios/
├── ui_main.py # Interface gráfica principal
├── data_loader.py # Funções para carregar CSV ou JSON
├── analyzer.py # Funções de análise de dados
├── pdf_report.py # Funções para gerar PDF
├── README.md # Este arquivo
└── requirements.txt # Dependências do projeto
```

---

## ⚙️ Requisitos

- Python 3.10 ou superior
- Bibliotecas Python:

```bash
pip install pyqt6 fpdf

🖥️ Como Usar

    Abra o terminal na pasta do projeto.

    Execute a interface:

python ui_main.py

    Na janela que abrir:

        Clique em “Carregar Arquivo” e selecione um CSV ou JSON.

        Clique em “Gerar PDF” para criar o relatório completo.

    Escolha o local e nome do arquivo PDF.
```

📌 Observações Técnicas

    O projeto usa FPDF clássico, garantindo compatibilidade sem fontes externas.

    Textos longos são automaticamente quebrados e distribuídos em múltiplas linhas e páginas.

    A seção “Resumo Consolidado” no final mostra todos os registros do arquivo em uma tabela, alinhando todas as colunas.

    Valores que não podem ser convertidos para Latin-1 são ignorados, evitando erros de geração do PDF.

💡 Possíveis Melhorias Futuras

    Adicionar gráficos (barras/pizza) para cada variável usando Matplotlib

    Layout mais profissional com cores, linhas alternadas e cabeçalho fixo

    Suporte a arquivos Excel (.xlsx)

    Exportação de relatório em HTML interativo

    Análise de outliers e estatísticas avançadas

📜 Licença

Este projeto está disponível sob a licença MIT, podendo ser usado, modificado e distribuído livremente.
👤 Autor

Jonathan S. Cardoso
Desenvolvedor Python | Projetos de Análise de Dados e Interfaces Gráficas
