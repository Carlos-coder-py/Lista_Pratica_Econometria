# Lista Prática – Econometria I

---

## Integrantes e divisão do trabalho

| Integrante | Responsabilidade | Itens | Arquivo |
|---|---|:---:|---|
| **Carlos** | Código Python – Partes 1 a 4 (tratamento dos dados, estatística descritiva, correlações e testes de hipóteses) | 0 – 75 | [`lista_pratica_parte1.py`](lista_pratica_parte1.py) |
| **Winicius** | Código Python – Partes 5 a 7 e fechamento (análises gráficas, regressões, diagnóstico e tabela final) | 76 – 178 | [`lista_pratica_parte2.py`](lista_pratica_parte2.py) |
| **Gabriel** | Relatório com os resultados, respostas e interpretações dos itens (\*) e (\*\*) | 13 – 177 | [`Relatorio_Lista_Pratica.docx`](Relatorio_Lista_Pratica.docx) |

## Organização do trabalho

O código foi desenvolvido em colaboração e dividido em dois arquivos sequenciais. Carlos iniciou a análise a partir da base original e, ao final do item 75, salvou a base com todas as variáveis construídas. O Winicius deu continuidade a partir dessa base até o item 178. Assim Gabriel elaborou o relatório com base nas tabelas e figuras geradas.

```
dados/Base - LP1.xlsx
        │
        ▼
lista_pratica_parte1.py   (Carlos)  →  resultados/base_parte1.xlsx
        │
        ▼
lista_pratica_parte2.py   (Winicius)  →  resultados/base_final_analises.xlsx
        │
        ▼
Relatorio_Lista_Pratica.docx   (Gabriel)
```

## Estrutura do repositório

Todos os arquivos gerados pela execução dos códigos já estão salvos nas respectivas pastas e podem ser consultados diretamente.

```
Lista_Pratica_Econometria/
├── README.md
├── lista_pratica_parte1.py          código – itens 0 a 75
├── lista_pratica_parte2.py          código – itens 76 a 178
├── Relatorio_Lista_Pratica.docx     relatório de resultados
│
├── dados/                           base original, sem alterações manuais
│   └── Base - LP1.xlsx
│
├── resultados/                      tabelas (.xlsx/.csv), saídas das regressões e testes (.txt)
│                                    e bases tratadas (base_tratada, base_parte1, base_final_analises)
│
└── figuras/                         gráficos gerados ao longo da lista (.png)
```

- [`dados/`](dados/) – base utilizada na atividade
- [`resultados/`](resultados/) – 114 arquivos de resultados, nomeados conforme indicado na lista
- [`figuras/`](figuras/) – 33 gráficos, nomeados conforme indicado na lista

## Como reproduzir

1. Instalar as bibliotecas (no terminal):
   ```bash
   python -m pip install pandas numpy scipy statsmodels matplotlib openpyxl
   ```
2. Abrir a pasta `Lista_Pratica_Econometria` como diretório de trabalho (VS Code: `File → Open Folder`).
3. Executar os scripts **nesta ordem**:
   ```bash
   python lista_pratica_parte1.py
   python lista_pratica_parte2.py
   ```

A parte 2 depende da base salva ao final da parte 1. As pastas `resultados/` e `figuras/` são criadas automaticamente caso não existam. Os gráficos são exibidos com `plt.show()`, e a execução continua após cada janela ser fechada.

## Observações

- Na base, a coluna do passivo circulante foi importada como `"PasCir\n  "` (com dois espaços após a quebra de linha). O nome foi ajustado no código dos itens 12 e 21.
- Os itens 100, 110, 112, 117, 131, 135, 137, 144 e 177 foram identificados no código com "resposta no relatório".
