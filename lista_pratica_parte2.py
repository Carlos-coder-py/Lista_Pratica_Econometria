# =============================================================================
# Conteúdo: Parte 5 (análises gráficas)                       itens 76  a 94
#           Parte 6 (análise de regressão)                    itens 95  a 167
#           Parte 7 (diagnóstico e especificação)             itens 168 a 175
#           Fechamento                                        itens 176 a 178
# Pré-requisito: executar antes lista_pratica_parte1.py (Integrante 1), que
# gera "resultados/base_parte1.xlsx" com todas as variáveis tratadas.
# =============================================================================

# Importação das bibliotecas item 7
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import statsmodels.api as sm
import statsmodels.formula.api as smf

# Garante que as pastas de saída existam (caso o script rode em outra máquina)
for pasta in ["resultados", "figuras"]:
    os.makedirs(pasta, exist_ok=True)

# Continuidade do trabalho: carrega a base salva ao final da parte 1
# (já contém as variáveis winsorizadas, roe, roe_w e d_rc)
df = pd.read_excel("resultados/base_parte1.xlsx")
df = df.sort_values(["id", "Ano"]).reset_index(drop=True)
print(df.shape)

# =============================================================================
# Parte 5 - Análises gráficas
# =============================================================================

# Item 76 - Gráfico de dispersão entre retenção de caixa e Q de Tobin
plt.figure(figsize=(8, 6))
plt.scatter(df["retcaixa_w"], df["qtobin_w"], alpha=0.5)
plt.xlabel("Retenção de caixa")
plt.ylabel("Q de Tobin")
plt.title("Retenção de caixa e Q de Tobin")
plt.tight_layout()
plt.savefig("figuras/dispersao_retcaixa_qtobin.png", dpi=300,
            bbox_inches="tight")
plt.show()

# Item 77 - Mesmo gráfico separado para gov = 0 e gov = 1
for grupo in [0, 1]:
    dados = df[df["gov"] == grupo]
    plt.figure(figsize=(8, 6))
    plt.scatter(dados["retcaixa_w"], dados["qtobin_w"], alpha=0.5)
    plt.xlabel("Retenção de caixa")
    plt.ylabel("Q de Tobin")
    plt.title(f"Retenção de caixa e Q de Tobin - gov = {grupo}")
    plt.tight_layout()
    plt.savefig(f"figuras/dispersao_retcaixa_qtobin_gov_{grupo}.png", dpi=300,
                bbox_inches="tight")
    plt.show()

# Item 78 - Média, desvio padrão e máximo do Q de Tobin e da retenção (barras)
estatisticas_78 = pd.DataFrame({
    "Q de Tobin": [df["qtobin_w"].mean(), df["qtobin_w"].std(),
                   df["qtobin_w"].max()],
    "Retenção de caixa": [df["retcaixa_w"].mean(), df["retcaixa_w"].std(),
                          df["retcaixa_w"].max()]
}, index=["Média", "Desvio padrão", "Máximo"])
print(estatisticas_78)
estatisticas_78.to_excel("resultados/estatisticas_grafico_qtobin_retcaixa.xlsx")
estatisticas_78.plot(kind="bar", figsize=(9, 6))
plt.ylabel("Valor")
plt.title("Estatísticas do Q de Tobin e da retenção de caixa")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("figuras/barras_estatisticas_qtobin_retcaixa.png", dpi=300,
            bbox_inches="tight")
plt.show()

# Item 79 - Mesmas estatísticas em barras horizontais
estatisticas_78.plot(kind="barh", figsize=(9, 6))
plt.xlabel("Valor")
plt.title("Estatísticas do Q de Tobin e da retenção de caixa")
plt.tight_layout()
plt.savefig("figuras/barras_horizontais_qtobin_retcaixa.png", dpi=300,
            bbox_inches="tight")
plt.show()

# Item 80 - Q de Tobin médio e retenção média por grupo de governança
medias_80 = df.groupby("gov")[["qtobin_w", "retcaixa_w"]].mean()
print(medias_80)
medias_80.to_excel("resultados/medias_qtobin_retcaixa_por_gov.xlsx")
medias_80.plot(kind="bar", figsize=(8, 6))
plt.xlabel("Governança")
plt.ylabel("Média")
plt.title("Q de Tobin e retenção de caixa por governança")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("figuras/medias_qtobin_retcaixa_por_gov.png", dpi=300,
            bbox_inches="tight")
plt.show()

# Item 81 - Número de observações por segmento de governança
freq_81 = df["governanca"].value_counts()
print(freq_81)
freq_81.to_excel("resultados/frequencia_segmentos_governanca.xlsx")
freq_81.plot(kind="bar", figsize=(9, 6))
plt.xlabel("Segmento de governança")
plt.ylabel("Número de observações")
plt.title("Distribuição das observações por segmento de governança")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("figuras/frequencia_segmentos_governanca.png", dpi=300,
            bbox_inches="tight")
plt.show()

# Item 82 - Segmentos de governança x crescimento da receita (frequências)
freq_82 = pd.crosstab(df["governanca"], df["d_crescrec"])
print(freq_82)
freq_82.to_excel("resultados/governanca_crescimento_receita.xlsx")
freq_82.plot(kind="bar", figsize=(10, 6))
plt.xlabel("Segmento de governança")
plt.ylabel("Número de observações")
plt.title("Governança e crescimento da receita")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("figuras/governanca_crescimento_receita.png", dpi=300,
            bbox_inches="tight")
plt.show()

# Item 83 - Mesma análise em participação percentual (dentro de cada segmento)
perc_83 = pd.crosstab(df["governanca"], df["d_crescrec"], normalize="index") * 100
print(perc_83)
perc_83.to_excel("resultados/governanca_crescimento_percentual.xlsx")
perc_83.plot(kind="bar", figsize=(10, 6))
plt.xlabel("Segmento de governança")
plt.ylabel("Percentual (%)")
plt.title("Crescimento da receita por segmento de governança")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("figuras/governanca_crescimento_percentual.png", dpi=300,
            bbox_inches="tight")
plt.show()

# Item 84 - Distribuição das observações por setor e segmento de governança
freq_84 = pd.crosstab(df["setor"], df["governanca"])
print(freq_84)
freq_84.to_excel("resultados/setor_governanca_grafico.xlsx")
freq_84.plot(kind="bar", figsize=(12, 7))
plt.xlabel("Setor")
plt.ylabel("Número de observações")
plt.title("Distribuição por setor e segmento de governança")
plt.xticks(rotation=60)
plt.tight_layout()
plt.savefig("figuras/setor_governanca.png", dpi=300, bbox_inches="tight")
plt.show()

# Item 85 - Média e desvio padrão do Q de Tobin por governança
grafico_85 = df.groupby("gov")["qtobin_w"].agg(["mean", "std"])
print(grafico_85)
grafico_85.to_excel("resultados/media_dp_qtobin_governanca.xlsx")
plt.figure(figsize=(7, 5))
plt.errorbar(grafico_85.index, grafico_85["mean"], yerr=grafico_85["std"],
             fmt="o", capsize=5)
plt.xlabel("Governança")
plt.ylabel("Q de Tobin")
plt.title("Média e desvio padrão do Q de Tobin")
plt.xticks([0, 1])
plt.tight_layout()
plt.savefig("figuras/media_dp_qtobin_governanca.png", dpi=300,
            bbox_inches="tight")
plt.show()

# Item 86 - Gráfico de pizza com a distribuição por segmento de governança
freq_86 = df["governanca"].value_counts()
plt.figure(figsize=(8, 8))
plt.pie(freq_86.values, labels=freq_86.index, autopct="%1.1f%%")
plt.title("Distribuição por segmento de governança")
plt.tight_layout()
plt.savefig("figuras/pizza_segmentos_governanca.png", dpi=300,
            bbox_inches="tight")
plt.show()

# Item 87 - Pizza dos segmentos para retenção abaixo (0) e acima (1) da mediana
for grupo in [0, 1]:
    dados = df[df["d_rc"] == grupo]
    freq = dados["governanca"].value_counts()
    plt.figure(figsize=(8, 8))
    plt.pie(freq.values, labels=freq.index, autopct="%1.1f%%")
    plt.title(f"Segmentos de governança - d_rc = {grupo}")
    plt.tight_layout()
    plt.savefig(f"figuras/pizza_governanca_drc_{grupo}.png", dpi=300,
                bbox_inches="tight")
    plt.show()

# Item 88 - Histograma do Q de Tobin
plt.figure(figsize=(8, 6))
plt.hist(df["qtobin_w"], bins=30)
plt.xlabel("Q de Tobin")
plt.ylabel("Frequência")
plt.title("Distribuição do Q de Tobin")
plt.tight_layout()
plt.savefig("figuras/histograma_qtobin.png", dpi=300, bbox_inches="tight")
plt.show()

# Item 89 - Histograma do Q de Tobin com curva normal sobreposta
media_q = df["qtobin_w"].mean()
dp_q = df["qtobin_w"].std()
x = np.linspace(df["qtobin_w"].min(), df["qtobin_w"].max(), 300)
normal_q = stats.norm.pdf(x, loc=media_q, scale=dp_q)
plt.figure(figsize=(8, 6))
plt.hist(df["qtobin_w"], bins=30, density=True, alpha=0.6)
plt.plot(x, normal_q, linewidth=2)
plt.xlabel("Q de Tobin")
plt.ylabel("Densidade")
plt.title("Distribuição do Q de Tobin e curva normal")
plt.tight_layout()
plt.savefig("figuras/histograma_qtobin_normal.png", dpi=300, bbox_inches="tight")
plt.show()

# Item 90 - Histograma da retenção de caixa com curva normal sobreposta
media_rc = df["retcaixa_w"].mean()
dp_rc = df["retcaixa_w"].std()
x = np.linspace(df["retcaixa_w"].min(), df["retcaixa_w"].max(), 300)
normal_rc = stats.norm.pdf(x, loc=media_rc, scale=dp_rc)
plt.figure(figsize=(8, 6))
plt.hist(df["retcaixa_w"], bins=30, density=True, alpha=0.6)
plt.plot(x, normal_rc, linewidth=2)
plt.xlabel("Retenção de caixa")
plt.ylabel("Densidade")
plt.title("Distribuição da retenção de caixa e curva normal")
plt.tight_layout()
plt.savefig("figuras/histograma_retcaixa_normal.png", dpi=300,
            bbox_inches="tight")
plt.show()

# Item 91 - Distribuição do Q de Tobin para retenção abaixo e acima da mediana
for grupo in [0, 1]:
    dados = df.loc[df["d_rc"] == grupo, "qtobin_w"]
    media = dados.mean()
    dp = dados.std()
    x = np.linspace(dados.min(), dados.max(), 300)
    normal = stats.norm.pdf(x, loc=media, scale=dp)
    plt.figure(figsize=(8, 6))
    plt.hist(dados, bins=30, density=True, alpha=0.6)
    plt.plot(x, normal, linewidth=2)
    plt.xlabel("Q de Tobin")
    plt.ylabel("Densidade")
    plt.title(f"Distribuição do Q de Tobin - d_rc = {grupo}")
    plt.tight_layout()
    plt.savefig(f"figuras/histograma_qtobin_drc_{grupo}.png", dpi=300,
                bbox_inches="tight")
    plt.show()

# Item 92 - Distribuição das observações entre gov = 0 e gov = 1
freq_92 = df["gov"].value_counts().sort_index()
plt.figure(figsize=(7, 5))
plt.bar(freq_92.index.astype(str), freq_92.values)
plt.xlabel("Governança")
plt.ylabel("Número de observações")
plt.title("Distribuição da variável gov")
plt.tight_layout()
plt.savefig("figuras/distribuicao_gov.png", dpi=300, bbox_inches="tight")
plt.show()

# Item 93 - Matriz de dispersão incluindo o ROE
vars_grafico = ["qtobin_w", "retcaixa_w", "roa_w", "roe_w", "tam_w"]
dados_93 = df[vars_grafico].dropna()
pd.plotting.scatter_matrix(dados_93, figsize=(12, 12), diagonal="hist",
                           alpha=0.5)
plt.suptitle("Matriz de dispersão das variáveis")
plt.tight_layout()
plt.savefig("figuras/matriz_dispersao_com_roe.png", dpi=300, bbox_inches="tight")
plt.show()

# Item 94 - Matriz de dispersão separada para gov = 0 e gov = 1
for grupo in [0, 1]:
    dados = df.loc[df["gov"] == grupo, vars_grafico].dropna()
    pd.plotting.scatter_matrix(dados, figsize=(12, 12), diagonal="hist",
                               alpha=0.5)
    plt.suptitle(f"Matriz de dispersão - gov = {grupo}")
    plt.tight_layout()
    plt.savefig(f"figuras/matriz_dispersao_gov_{grupo}.png", dpi=300,
                bbox_inches="tight")
    plt.show()

# =============================================================================
# Parte 6 - Análise de regressão
# =============================================================================

# Item 95 - Regressão simples por MQO: qtobin = b0 + b1*retcaixa + e
modelo_95 = smf.ols("qtobin_w ~ retcaixa_w", data=df).fit()
print(modelo_95.summary())
with open("resultados/modelo_95_regressao_simples.txt", "w",
          encoding="utf-8") as arquivo:
    arquivo.write(modelo_95.summary().as_text())

# Item 96 - (resposta no relatório)

# Item 97 - Gráfico de dispersão com a reta estimada pelo modelo simples
plt.figure(figsize=(8, 6))
plt.scatter(df["retcaixa_w"], df["qtobin_w"], alpha=0.4)
x_97 = np.linspace(df["retcaixa_w"].min(), df["retcaixa_w"].max(), 200)
y_97 = modelo_95.params["Intercept"] + modelo_95.params["retcaixa_w"] * x_97
plt.plot(x_97, y_97, linewidth=2)
plt.xlabel("Retenção de caixa")
plt.ylabel("Q de Tobin")
plt.title("Regressão simples: retenção de caixa e Q de Tobin")
plt.tight_layout()
plt.savefig("figuras/regressao_simples_retcaixa_qtobin.png", dpi=300,
            bbox_inches="tight")
plt.show()

# Item 98 - Valores previstos e resíduos do modelo simples
df["qtobinest"] = modelo_95.fittedvalues
df["resid"] = modelo_95.resid
print(df[["qtobin_w", "qtobinest", "resid"]].head())

# Item 99 - Histograma dos resíduos com curva normal sobreposta
media_resid = df["resid"].mean()
dp_resid = df["resid"].std()
x = np.linspace(df["resid"].min(), df["resid"].max(), 300)
normal_resid = stats.norm.pdf(x, loc=media_resid, scale=dp_resid)
plt.figure(figsize=(8, 6))
plt.hist(df["resid"], bins=30, density=True, alpha=0.6)
plt.plot(x, normal_resid, linewidth=2)
plt.xlabel("Resíduo")
plt.ylabel("Densidade")
plt.title("Distribuição dos resíduos do modelo simples")
plt.tight_layout()
plt.savefig("figuras/histograma_residuos_modelo_simples.png", dpi=300,
            bbox_inches="tight")
plt.show()

# Item 100 - (resposta no relatório)

# Item 101 - Regressão linear múltipla por MQO
modelo_101 = smf.ols("qtobin_w ~ retcaixa_w + roa_w + tam_w + gov + c_rec_w + prej",
                     data=df).fit()
print(modelo_101.summary())
with open("resultados/modelo_101_regressao_multipla.txt", "w",
          encoding="utf-8") as arquivo:
    arquivo.write(modelo_101.summary().as_text())

# Item 102 - Valores previstos e resíduos do modelo múltiplo
df["qtobinest2"] = modelo_101.fittedvalues
df["resid2"] = modelo_101.resid

# Item 103 - Modelo múltiplo sem constante ("0 +" remove o intercepto)
modelo_103 = smf.ols("qtobin_w ~ 0 + retcaixa_w + roa_w + tam_w + gov + c_rec_w + prej",
                     data=df).fit()
print(modelo_103.summary())
with open("resultados/modelo_103_sem_constante.txt", "w",
          encoding="utf-8") as arquivo:
    arquivo.write(modelo_103.summary().as_text())

# Item 104 - Intervalos de confiança de 90% (alpha = 0,10)
modelo_104 = modelo_101
ic_90 = modelo_104.conf_int(alpha=0.10)
ic_90.columns = ["Limite inferior", "Limite superior"]
print(ic_90)
ic_90.to_excel("resultados/intervalos_confianca_90_modelo_multiplo.xlsx")

# Item 105 - Modelo múltiplo controlando por setor (C() cria as dummies)
modelo_105 = smf.ols("qtobin_w ~ retcaixa_w + roa_w + tam_w + gov + c_rec_w + "
                     "prej + C(setor)", data=df).fit()
print(modelo_105.summary())
with open("resultados/modelo_105_controle_setor.txt", "w",
          encoding="utf-8") as arquivo:
    arquivo.write(modelo_105.summary().as_text())

# Item 106 - Modelo múltiplo controlando por setor e ano
modelo_106 = smf.ols("qtobin_w ~ retcaixa_w + roa_w + tam_w + gov + c_rec_w + "
                     "prej + C(setor) + C(Ano)", data=df).fit()
print(modelo_106.summary())
with open("resultados/modelo_106_controle_setor_ano.txt", "w",
          encoding="utf-8") as arquivo:
    arquivo.write(modelo_106.summary().as_text())

# Item 107 - Tabela comparativa dos modelos M1 a M4
from statsmodels.iolib.summary2 import summary_col
tabela_107 = summary_col([modelo_95, modelo_101, modelo_105, modelo_106],
                         stars=True, model_names=["M1", "M2", "M3", "M4"],
                         info_dict={"N": lambda x: f"{int(x.nobs)}",
                                    "R²": lambda x: f"{x.rsquared:.4f}"})
print(tabela_107)
with open("resultados/tabela_modelos_M1_M4.txt", "w",
          encoding="utf-8") as arquivo:
    arquivo.write(tabela_107.as_text())

# Item 108 - Interação entre retenção de caixa e governança
df["rc_gov"] = df["retcaixa_w"] * df["gov"]

# Item 109 - Modelo com interação retenção x governança
modelo_109 = smf.ols("qtobin_w ~ retcaixa_w + roa_w + tam_w + c_rec_w + prej + "
                     "gov + rc_gov", data=df).fit()
print(modelo_109.summary())
with open("resultados/modelo_109_interacao_gov.txt", "w",
          encoding="utf-8") as arquivo:
    arquivo.write(modelo_109.summary().as_text())

# Item 110 - (resposta no relatório)

# Item 111 - Teste conjunto: a retenção de caixa afeta o valor de mercado?
teste_111 = modelo_109.wald_test("retcaixa_w = 0, rc_gov = 0", scalar=True)
print(teste_111)
with open("resultados/teste_111_retencao_modelo_interacao.txt", "w",
          encoding="utf-8") as arquivo:
    arquivo.write(str(teste_111))

# Item 112 - (resposta no relatório)

# Item 113 - Teste conjunto: a governança afeta o valor no modelo com interação?
teste_113 = modelo_109.wald_test("gov = 0, rc_gov = 0", scalar=True)
print(teste_113)
with open("resultados/teste_113_governanca_modelo_interacao.txt", "w",
          encoding="utf-8") as arquivo:
    arquivo.write(str(teste_113))

# Item 114 - Os coeficientes de ROA e tamanho são estatisticamente iguais?
teste_114 = modelo_109.t_test("roa_w = tam_w")
print(teste_114)
with open("resultados/teste_114_roa_tamanho.txt", "w",
          encoding="utf-8") as arquivo:
    arquivo.write(str(teste_114))

# Item 115 - Interações entre retenção de caixa e Nível 1, Nível 2 e Novo Mercado
df["rc_n1"] = df["retcaixa_w"] * df["n1"]
df["rc_n2"] = df["retcaixa_w"] * df["n2"]
df["rc_nm"] = df["retcaixa_w"] * df["nm"]

# Item 116 - Modelo com efeito da retenção variando entre N1, N2 e NM
modelo_116 = smf.ols("qtobin_w ~ retcaixa_w + roa_w + tam_w + c_rec_w + prej + n1 "
                     "+ n2 + nm + rc_n1 + rc_n2 + rc_nm", data=df).fit()
print(modelo_116.summary())
with open("resultados/modelo_116_interacoes_niveis.txt", "w",
          encoding="utf-8") as arquivo:
    arquivo.write(modelo_116.summary().as_text())

# Item 117 - (resposta no relatório)

# Item 118 - Teste conjunto: a retenção afeta o valor no modelo com níveis?
teste_118 = modelo_116.wald_test("retcaixa_w = 0, rc_n1 = 0, rc_n2 = 0, rc_nm = 0",
                                 scalar=True)
print(teste_118)
with open("resultados/teste_118_retencao_niveis.txt", "w",
          encoding="utf-8") as arquivo:
    arquivo.write(str(teste_118))

# Item 119 - Teste conjunto: pertencer ao Novo Mercado afeta o valor?
teste_119 = modelo_116.wald_test("nm = 0, rc_nm = 0", scalar=True)
print(teste_119)
with open("resultados/teste_119_nm.txt", "w", encoding="utf-8") as arquivo:
    arquivo.write(str(teste_119))

# Item 120 - Teste conjunto: pertencer ao Nível 2 afeta o valor?
teste_120 = modelo_116.wald_test("n2 = 0, rc_n2 = 0", scalar=True)
print(teste_120)
with open("resultados/teste_120_n2.txt", "w", encoding="utf-8") as arquivo:
    arquivo.write(str(teste_120))

# Item 121 - Teste conjunto: pertencer ao Nível 1 afeta o valor?
teste_121 = modelo_116.wald_test("n1 = 0, rc_n1 = 0", scalar=True)
print(teste_121)
with open("resultados/teste_121_n1.txt", "w", encoding="utf-8") as arquivo:
    arquivo.write(str(teste_121))

# Item 122 - Os efeitos adicionais da retenção são iguais entre N1 e N2?
teste_122 = modelo_116.t_test("rc_n1 = rc_n2")
print(teste_122)
with open("resultados/teste_122_rc_n1_rc_n2.txt", "w",
          encoding="utf-8") as arquivo:
    arquivo.write(str(teste_122))

# Item 123 - O efeito adicional da retenção é significativo em pelo menos um nível?
teste_123 = modelo_116.wald_test("rc_n1 = 0, rc_n2 = 0, rc_nm = 0", scalar=True)
print(teste_123)
with open("resultados/teste_123_interacoes_niveis.txt", "w",
          encoding="utf-8") as arquivo:
    arquivo.write(str(teste_123))

# Item 124 - Retenção afeta o valor E efeito adicional no NM = 2 x efeito no N1
teste_124 = modelo_116.wald_test("retcaixa_w = 0, rc_n1 = 0, rc_n2 = 0, rc_nm = 0, "
                                 "rc_nm = 2*rc_n1", scalar=True)
print(teste_124)
with open("resultados/teste_124_conjunto.txt", "w", encoding="utf-8") as arquivo:
    arquivo.write(str(teste_124))

# Item 125 - Modelos conjuntos para ROA e ROE (formato longo + interações)
dados_125 = df[["roa_w", "roe_w", "retcaixa_w", "tam_w", "gov", "c_rec_w",
                "prej"]].dropna().copy()
dados_roa = dados_125.rename(columns={"roa_w": "rentabilidade"}).copy()
dados_roa["tipo_roe"] = 0
dados_roe = dados_125.rename(columns={"roe_w": "rentabilidade"}).copy()
dados_roe["tipo_roe"] = 1
dados_125_long = pd.concat([dados_roa, dados_roe], ignore_index=True)
modelo_125 = smf.ols("rentabilidade ~ retcaixa_w + tam_w + gov + c_rec_w + prej + "
                     "tipo_roe + tipo_roe:retcaixa_w + tipo_roe:tam_w + tipo_roe:gov "
                     "+ tipo_roe:c_rec_w + tipo_roe:prej", data=dados_125_long).fit()
print(modelo_125.summary())
with open("resultados/modelo_125_comparacao_roa_roe.txt", "w",
          encoding="utf-8") as arquivo:
    arquivo.write(modelo_125.summary().as_text())

# Item 126 - Os efeitos da retenção no ROA e no ROE são os mesmos?
teste_126 = modelo_125.t_test("tipo_roe:retcaixa_w = 0")
print(teste_126)

# Item 127 - Os efeitos do tamanho no ROA e no ROE são os mesmos?
teste_127 = modelo_125.t_test("tipo_roe:tam_w = 0")
print(teste_127)

# Item 128 - O efeito da governança no ROA é o dobro do efeito no ROE?
teste_128 = modelo_125.t_test("gov = 2*(gov + tipo_roe:gov)")
print(teste_128)

# Item 129 - Retenção de caixa ao quadrado
df["rc2"] = df["retcaixa_w"] ** 2

# Item 130 - Modelo para avaliar efeito não linear da retenção sobre o Q
modelo_130 = smf.ols("qtobin_w ~ retcaixa_w + rc2 + roa_w + tam_w + gov + c_rec_w "
                     "+ prej", data=df).fit()
print(modelo_130.summary())
with open("resultados/modelo_130_quadratico.txt", "w",
          encoding="utf-8") as arquivo:
    arquivo.write(modelo_130.summary().as_text())

# Item 131 - (resposta no relatório)

# Item 132 - Teste conjunto da retenção no modelo quadrático
teste_132 = modelo_130.wald_test("retcaixa_w = 0, rc2 = 0", scalar=True)
print(teste_132)

# Item 133 - Interação entre retenção ao quadrado e governança
df["rc2_gov"] = df["rc2"] * df["gov"]

# Item 134 - Modelo não linear com interações de governança, ano e setor
modelo_134 = smf.ols("qtobin_w ~ retcaixa_w + rc2 + roa_w + tam_w + c_rec_w + prej "
                     "+ gov + rc_gov + rc2_gov + C(Ano) + C(setor)", data=df).fit()
print(modelo_134.summary())
with open("resultados/modelo_134_quadratico_governanca.txt", "w",
          encoding="utf-8") as arquivo:
    arquivo.write(modelo_134.summary().as_text())

# Item 135 - (resposta no relatório)

# Item 136 - Teste conjunto da retenção no modelo não linear com governança
teste_136 = modelo_134.wald_test("retcaixa_w = 0, rc2 = 0, rc_gov = 0, rc2_gov = 0",
                                 scalar=True)
print(teste_136)

# Item 137 - (resposta no relatório)

# Item 138 - Teste conjunto: a governança afeta o valor no modelo não linear?
teste_138 = modelo_134.wald_test("gov = 0, rc_gov = 0, rc2_gov = 0", scalar=True)
print(teste_138)

# Item 139 - A governança faz com que o efeito da retenção seja diferente?
teste_139 = modelo_134.wald_test("rc_gov = 0, rc2_gov = 0", scalar=True)
print(teste_139)

# Item 140 - O efeito da retenção é não linear para empresas com governança?
teste_140 = modelo_134.t_test("rc2 + rc2_gov = 0")
print(teste_140)

# Item 141 - Existe efeito não linear da retenção independentemente da governança?
teste_141 = modelo_134.wald_test("rc2 = 0, rc2_gov = 0", scalar=True)
print(teste_141)

# Item 142 - Interações entre retenção ao quadrado e N1, N2 e NM
df["rc2_n1"] = df["rc2"] * df["n1"]
df["rc2_n2"] = df["rc2"] * df["n2"]
df["rc2_nm"] = df["rc2"] * df["nm"]

# Item 143 - Modelo não linear com níveis específicos, ano e setor
modelo_143 = smf.ols("qtobin_w ~ retcaixa_w + rc2 + roa_w + tam_w + c_rec_w + prej "
                     "+ n1 + n2 + nm + rc_n1 + rc_n2 + rc_nm + rc2_n1 + rc2_n2 + "
                     "rc2_nm + C(Ano) + C(setor)", data=df).fit()
print(modelo_143.summary())
with open("resultados/modelo_143_quadratico_niveis.txt", "w",
          encoding="utf-8") as arquivo:
    arquivo.write(modelo_143.summary().as_text())

# Item 144 - (resposta no relatório)

# Item 145 - Teste conjunto da retenção no modelo não linear com níveis
teste_145 = modelo_143.wald_test("retcaixa_w = 0, rc2 = 0, rc_n1 = 0, rc_n2 = 0, "
                                 "rc_nm = 0, rc2_n1 = 0, rc2_n2 = 0, rc2_nm = 0",
                                 scalar=True)
print(teste_145)

# Item 146 - Pertencer ao Novo Mercado afeta o valor no modelo não linear?
teste_146 = modelo_143.wald_test("nm = 0, rc_nm = 0, rc2_nm = 0", scalar=True)
print(teste_146)

# Item 147 - Pertencer ao Nível 2 afeta o valor no modelo não linear?
teste_147 = modelo_143.wald_test("n2 = 0, rc_n2 = 0, rc2_n2 = 0", scalar=True)
print(teste_147)

# Item 148 - Pertencer ao Nível 1 afeta o valor no modelo não linear?
teste_148 = modelo_143.wald_test("n1 = 0, rc_n1 = 0, rc2_n1 = 0", scalar=True)
print(teste_148)

# Item 149 - O Novo Mercado faz com que o efeito da retenção seja diferente?
teste_149 = modelo_143.wald_test("rc_nm = 0, rc2_nm = 0", scalar=True)
print(teste_149)

# Item 150 - O Nível 2 faz com que o efeito da retenção seja diferente?
teste_150 = modelo_143.wald_test("rc_n2 = 0, rc2_n2 = 0", scalar=True)
print(teste_150)

# Item 151 - O Nível 1 faz com que o efeito da retenção seja diferente?
teste_151 = modelo_143.wald_test("rc_n1 = 0, rc2_n1 = 0", scalar=True)
print(teste_151)

# Item 152 - O efeito da retenção é não linear no Novo Mercado?
teste_152 = modelo_143.t_test("rc2 + rc2_nm = 0")
print(teste_152)

# Item 153 - O efeito da retenção é não linear no Nível 2?
teste_153 = modelo_143.t_test("rc2 + rc2_n2 = 0")
print(teste_153)

# Item 154 - O efeito da retenção é não linear no Nível 1?
teste_154 = modelo_143.t_test("rc2 + rc2_n1 = 0")
print(teste_154)

# Item 155 - Existe efeito não linear em pelo menos um grupo de governança?
teste_155 = modelo_143.wald_test("rc2 = 0, rc2_n1 = 0, rc2_n2 = 0, rc2_nm = 0",
                                 scalar=True)
print(teste_155)

# Item 156 - Modelo quadrático separado para gov = 0 e gov = 1
dados_sub = df.copy()
resultados_156 = {}
for grupo, dados in dados_sub.groupby("gov"):
    modelo = smf.ols("qtobin_w ~ retcaixa_w + rc2 + roa_w + tam_w + c_rec_w + prej "
                     "+ C(Ano) + C(setor)", data=dados).fit()
    resultados_156[grupo] = modelo
    print(f"\ngov = {grupo}")
    print(modelo.summary())
    with open(f"resultados/modelo_156_gov_{grupo}.txt", "w",
              encoding="utf-8") as arquivo:
        arquivo.write(modelo.summary().as_text())

# Item 157 - Modelo quadrático por gov, apenas empresas sem prejuízo
dados_sub = df[df["prej"] == 0].copy()
resultados_157 = {}
for grupo, dados in dados_sub.groupby("gov"):
    modelo = smf.ols("qtobin_w ~ retcaixa_w + rc2 + roa_w + tam_w + c_rec_w + C(Ano) "
                     "+ C(setor)", data=dados).fit()
    resultados_157[grupo] = modelo
    print(f"\ngov = {grupo}")
    print(modelo.summary())
    with open(f"resultados/modelo_157_gov_{grupo}.txt", "w",
              encoding="utf-8") as arquivo:
        arquivo.write(modelo.summary().as_text())

# Item 158 - Modelo quadrático por gov, apenas empresas com prejuízo
dados_sub = df[df["prej"] == 1].copy()
resultados_158 = {}
for grupo, dados in dados_sub.groupby("gov"):
    modelo = smf.ols("qtobin_w ~ retcaixa_w + rc2 + roa_w + tam_w + c_rec_w + C(Ano) "
                     "+ C(setor)", data=dados).fit()
    resultados_158[grupo] = modelo
    print(f"\ngov = {grupo}")
    print(modelo.summary())
    with open(f"resultados/modelo_158_gov_{grupo}.txt", "w",
              encoding="utf-8") as arquivo:
        arquivo.write(modelo.summary().as_text())

# Item 159 - Modelo quadrático separado para dentro e fora do Novo Mercado
dados_sub = df.copy()
resultados_159 = {}
for grupo, dados in dados_sub.groupby("nm"):
    modelo = smf.ols("qtobin_w ~ retcaixa_w + rc2 + roa_w + tam_w + c_rec_w + prej "
                     "+ C(Ano) + C(setor)", data=dados).fit()
    resultados_159[grupo] = modelo
    print(f"\nnm = {grupo}")
    print(modelo.summary())
    with open(f"resultados/modelo_159_nm_{grupo}.txt", "w",
              encoding="utf-8") as arquivo:
        arquivo.write(modelo.summary().as_text())

# Item 160 - Modelo quadrático por nm, apenas empresas sem prejuízo
dados_sub = df[df["prej"] == 0].copy()
resultados_160 = {}
for grupo, dados in dados_sub.groupby("nm"):
    modelo = smf.ols("qtobin_w ~ retcaixa_w + rc2 + roa_w + tam_w + c_rec_w + C(Ano) "
                     "+ C(setor)", data=dados).fit()
    resultados_160[grupo] = modelo
    print(f"\nnm = {grupo}")
    print(modelo.summary())
    with open(f"resultados/modelo_160_nm_{grupo}.txt", "w",
              encoding="utf-8") as arquivo:
        arquivo.write(modelo.summary().as_text())

# Item 161 - Modelo quadrático por nm, apenas empresas com prejuízo
dados_sub = df[df["prej"] == 1].copy()
resultados_161 = {}
for grupo, dados in dados_sub.groupby("nm"):
    modelo = smf.ols("qtobin_w ~ retcaixa_w + rc2 + roa_w + tam_w + c_rec_w + C(Ano) "
                     "+ C(setor)", data=dados).fit()
    resultados_161[grupo] = modelo
    print(f"\nnm = {grupo}")
    print(modelo.summary())
    with open(f"resultados/modelo_161_nm_{grupo}.txt", "w",
              encoding="utf-8") as arquivo:
        arquivo.write(modelo.summary().as_text())

# Item 162 - Modelo quadrático separado para dentro e fora do Nível 2
dados_sub = df.copy()
resultados_162 = {}
for grupo, dados in dados_sub.groupby("n2"):
    modelo = smf.ols("qtobin_w ~ retcaixa_w + rc2 + roa_w + tam_w + c_rec_w + prej "
                     "+ C(Ano) + C(setor)", data=dados).fit()
    resultados_162[grupo] = modelo
    print(f"\nn2 = {grupo}")
    print(modelo.summary())
    with open(f"resultados/modelo_162_n2_{grupo}.txt", "w",
              encoding="utf-8") as arquivo:
        arquivo.write(modelo.summary().as_text())

# Item 163 - Modelo quadrático por n2, apenas empresas sem prejuízo
dados_sub = df[df["prej"] == 0].copy()
resultados_163 = {}
for grupo, dados in dados_sub.groupby("n2"):
    modelo = smf.ols("qtobin_w ~ retcaixa_w + rc2 + roa_w + tam_w + c_rec_w + C(Ano) "
                     "+ C(setor)", data=dados).fit()
    resultados_163[grupo] = modelo
    print(f"\nn2 = {grupo}")
    print(modelo.summary())
    with open(f"resultados/modelo_163_n2_{grupo}.txt", "w",
              encoding="utf-8") as arquivo:
        arquivo.write(modelo.summary().as_text())

# Item 164 - Modelo quadrático por n2, apenas empresas com prejuízo
dados_sub = df[df["prej"] == 1].copy()
resultados_164 = {}
for grupo, dados in dados_sub.groupby("n2"):
    modelo = smf.ols("qtobin_w ~ retcaixa_w + rc2 + roa_w + tam_w + c_rec_w + C(Ano) "
                     "+ C(setor)", data=dados).fit()
    resultados_164[grupo] = modelo
    print(f"\nn2 = {grupo}")
    print(modelo.summary())
    with open(f"resultados/modelo_164_n2_{grupo}.txt", "w",
              encoding="utf-8") as arquivo:
        arquivo.write(modelo.summary().as_text())

# Item 165 - Modelo quadrático separado para dentro e fora do Nível 1
dados_sub = df.copy()
resultados_165 = {}
for grupo, dados in dados_sub.groupby("n1"):
    modelo = smf.ols("qtobin_w ~ retcaixa_w + rc2 + roa_w + tam_w + c_rec_w + prej "
                     "+ C(Ano) + C(setor)", data=dados).fit()
    resultados_165[grupo] = modelo
    print(f"\nn1 = {grupo}")
    print(modelo.summary())
    with open(f"resultados/modelo_165_n1_{grupo}.txt", "w",
              encoding="utf-8") as arquivo:
        arquivo.write(modelo.summary().as_text())

# Item 166 - Modelo quadrático por n1, apenas empresas sem prejuízo
dados_sub = df[df["prej"] == 0].copy()
resultados_166 = {}
for grupo, dados in dados_sub.groupby("n1"):
    modelo = smf.ols("qtobin_w ~ retcaixa_w + rc2 + roa_w + tam_w + c_rec_w + C(Ano) "
                     "+ C(setor)", data=dados).fit()
    resultados_166[grupo] = modelo
    print(f"\nn1 = {grupo}")
    print(modelo.summary())
    with open(f"resultados/modelo_166_n1_{grupo}.txt", "w",
              encoding="utf-8") as arquivo:
        arquivo.write(modelo.summary().as_text())

# Item 167 - Modelo quadrático por n1, apenas empresas com prejuízo
dados_sub = df[df["prej"] == 1].copy()
resultados_167 = {}
for grupo, dados in dados_sub.groupby("n1"):
    modelo = smf.ols("qtobin_w ~ retcaixa_w + rc2 + roa_w + tam_w + c_rec_w + C(Ano) "
                     "+ C(setor)", data=dados).fit()
    resultados_167[grupo] = modelo
    print(f"\nn1 = {grupo}")
    print(modelo.summary())
    with open(f"resultados/modelo_167_n1_{grupo}.txt", "w",
              encoding="utf-8") as arquivo:
        arquivo.write(modelo.summary().as_text())

# =============================================================================
# Parte 7 - Diagnóstico e especificação dos modelos
# =============================================================================

# Item 168 - Modelos com interação com erros-padrão robustos (HC1 = robust Stata)
modelo_168_gov = smf.ols("qtobin_w ~ retcaixa_w + roa_w + tam_w + c_rec_w + prej + "
                         "gov + rc_gov", data=df).fit(cov_type="HC1")
modelo_168_niveis = smf.ols("qtobin_w ~ retcaixa_w + roa_w + tam_w + c_rec_w + prej "
                            "+ n1 + n2 + nm + rc_n1 + rc_n2 + rc_nm",
                            data=df).fit(cov_type="HC1")
print(modelo_168_gov.summary())
print(modelo_168_niveis.summary())
with open("resultados/modelo_168_gov_robusto.txt", "w",
          encoding="utf-8") as arquivo:
    arquivo.write(modelo_168_gov.summary().as_text())
with open("resultados/modelo_168_niveis_robusto.txt", "w",
          encoding="utf-8") as arquivo:
    arquivo.write(modelo_168_niveis.summary().as_text())

# Item 169 - Teste de Breusch-Pagan (modelos estimados SEM correção robusta)
# H0: homocedasticidade  vs  H1: heterocedasticidade
from statsmodels.stats.diagnostic import het_breuschpagan
modelo_169_gov = smf.ols("qtobin_w ~ retcaixa_w + roa_w + tam_w + c_rec_w + prej + "
                         "gov + rc_gov", data=df).fit()
modelo_169_niveis = smf.ols("qtobin_w ~ retcaixa_w + roa_w + tam_w + c_rec_w + prej "
                            "+ n1 + n2 + nm + rc_n1 + rc_n2 + rc_nm", data=df).fit()


def teste_bp(modelo, nome):
    lm, lm_pvalor, f, f_pvalor = het_breuschpagan(modelo.resid, modelo.model.exog)
    return {"Modelo": nome, "LM": lm, "p-valor LM": lm_pvalor, "F": f,
            "p-valor F": f_pvalor}


resultado_169 = pd.DataFrame([
    teste_bp(modelo_169_gov, "Governança agregada"),
    teste_bp(modelo_169_niveis, "Níveis específicos")
])
print(resultado_169)
resultado_169.to_excel("resultados/teste_breusch_pagan.xlsx", index=False)

# Item 170 - Multicolinearidade nos modelos com interação (VIF)
from statsmodels.stats.outliers_influence import variance_inflation_factor


def calcular_vif(modelo):
    X = pd.DataFrame(modelo.model.exog, columns=modelo.model.exog_names)
    vif = pd.DataFrame({
        "Variável": X.columns,
        "VIF": [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
    })
    return vif[vif["Variável"] != "Intercept"].reset_index(drop=True)


vif_170_gov = calcular_vif(modelo_169_gov)
vif_170_niveis = calcular_vif(modelo_169_niveis)
print("\nModelo com governança agregada:")
print(vif_170_gov)
print("\nModelo com níveis específicos:")
print(vif_170_niveis)
with pd.ExcelWriter("resultados/vif_modelos_interacao.xlsx") as writer:
    vif_170_gov.to_excel(writer, sheet_name="Governanca", index=False)
    vif_170_niveis.to_excel(writer, sheet_name="Niveis", index=False)

# Item 171 - VIF nos modelos sem as interações
modelo_171_gov = smf.ols("qtobin_w ~ retcaixa_w + roa_w + tam_w + c_rec_w + prej + "
                         "gov", data=df).fit()
modelo_171_niveis = smf.ols("qtobin_w ~ retcaixa_w + roa_w + tam_w + c_rec_w + prej "
                            "+ n1 + n2 + nm", data=df).fit()
vif_171_gov = calcular_vif(modelo_171_gov)
vif_171_niveis = calcular_vif(modelo_171_niveis)
print("\nModelo sem interação - governança agregada:")
print(vif_171_gov)
print("\nModelo sem interação - níveis específicos:")
print(vif_171_niveis)
with pd.ExcelWriter("resultados/vif_modelos_sem_interacao.xlsx") as writer:
    vif_171_gov.to_excel(writer, sheet_name="Governanca", index=False)
    vif_171_niveis.to_excel(writer, sheet_name="Niveis", index=False)

# Item 172 - RESET de Ramsey com potências dos valores ajustados
# H0: modelo corretamente especificado  vs  H1: indícios de erro de especificação
from statsmodels.stats.diagnostic import linear_reset
reset_172_gov = linear_reset(modelo_171_gov, power=3, test_type="fitted",
                             use_f=True, cov_type="HC1")
reset_172_niveis = linear_reset(modelo_171_niveis, power=3, test_type="fitted",
                                use_f=True, cov_type="HC1")
resultado_172 = pd.DataFrame({
    "Modelo": ["Governança agregada", "Níveis específicos"],
    "Estatística F": [reset_172_gov.fvalue, reset_172_niveis.fvalue],
    "p-valor": [reset_172_gov.pvalue, reset_172_niveis.pvalue]
})
print(resultado_172)
resultado_172.to_excel("resultados/teste_reset_fitted.xlsx", index=False)

# Item 173 - RESET com potências das variáveis explicativas
reset_173_gov = linear_reset(modelo_171_gov, power=3, test_type="exog",
                             use_f=True, cov_type="HC1")
reset_173_niveis = linear_reset(modelo_171_niveis, power=3, test_type="exog",
                                use_f=True, cov_type="HC1")
resultado_173 = pd.DataFrame({
    "Modelo": ["Governança agregada", "Níveis específicos"],
    "Estatística F": [reset_173_gov.fvalue, reset_173_niveis.fvalue],
    "p-valor": [reset_173_gov.pvalue, reset_173_niveis.pvalue]
})
print(resultado_173)
resultado_173.to_excel("resultados/teste_reset_exog.xlsx", index=False)

# Item 174 - RESET passo a passo: inclui yhat² e yhat³ e testa se são nulos
df_reset = df.copy()
base_174_gov = smf.ols("qtobin_w ~ retcaixa_w + roa_w + tam_w + c_rec_w + prej + "
                       "gov", data=df_reset).fit()
df_reset["yhat_gov"] = base_174_gov.fittedvalues
df_reset["yhat_gov2"] = df_reset["yhat_gov"] ** 2
df_reset["yhat_gov3"] = df_reset["yhat_gov"] ** 3
modelo_174_gov = smf.ols("qtobin_w ~ retcaixa_w + roa_w + tam_w + c_rec_w + prej + "
                         "gov + yhat_gov2 + yhat_gov3",
                         data=df_reset).fit(cov_type="HC1")
teste_174_gov = modelo_174_gov.wald_test("yhat_gov2 = 0, yhat_gov3 = 0",
                                         scalar=True)

base_174_niveis = smf.ols("qtobin_w ~ retcaixa_w + roa_w + tam_w + c_rec_w + prej "
                          "+ n1 + n2 + nm", data=df_reset).fit()
df_reset["yhat_niveis"] = base_174_niveis.fittedvalues
df_reset["yhat_niveis2"] = df_reset["yhat_niveis"] ** 2
df_reset["yhat_niveis3"] = df_reset["yhat_niveis"] ** 3
modelo_174_niveis = smf.ols("qtobin_w ~ retcaixa_w + roa_w + tam_w + c_rec_w + prej "
                            "+ n1 + n2 + nm + yhat_niveis2 + yhat_niveis3",
                            data=df_reset).fit(cov_type="HC1")
teste_174_niveis = modelo_174_niveis.wald_test("yhat_niveis2 = 0, yhat_niveis3 = 0",
                                               scalar=True)

resultado_174 = pd.DataFrame({
    "Modelo": ["Governança agregada", "Níveis específicos"],
    "Estatística": [float(teste_174_gov.statistic),
                    float(teste_174_niveis.statistic)],
    "p-valor": [float(teste_174_gov.pvalue), float(teste_174_niveis.pvalue)]
})
print(resultado_174)
resultado_174.to_excel("resultados/teste_reset_manual.xlsx", index=False)

# Item 175 - Correlação serial: teste de Breusch-Godfrey (empresa id 169)
# H0: não há correlação serial dos resíduos  vs  H1: há correlação serial
from statsmodels.stats.diagnostic import acorr_breusch_godfrey
df_169 = df[df["id"] == 169].copy()
df_169 = df_169.sort_values("Ano")
df_169["qtobin_lag"] = df_169["qtobin_w"].shift(1)
dados_175 = df_169[["qtobin_w", "qtobin_lag", "roa_w", "tam_w"]].dropna()
modelo_175 = smf.ols("qtobin_w ~ qtobin_lag + roa_w + tam_w", data=dados_175).fit()
bg_175 = acorr_breusch_godfrey(modelo_175, nlags=1)
resultado_175 = pd.DataFrame({
    "Estatística LM": [bg_175[0]],
    "p-valor LM": [bg_175[1]],
    "Estatística F": [bg_175[2]],
    "p-valor F": [bg_175[3]]
})
print(modelo_175.summary())
print(resultado_175)
with open("resultados/modelo_175_serie_temporal.txt", "w",
          encoding="utf-8") as arquivo:
    arquivo.write(modelo_175.summary().as_text())
resultado_175.to_excel("resultados/teste_breusch_godfrey.xlsx", index=False)

# =============================================================================
# Fechamento da Lista Prática
# =============================================================================

# Item 176 - Tabela final M1-M7, todos com erros-padrão robustos (HC1)
from statsmodels.iolib.summary2 import summary_col
m1 = smf.ols("qtobin_w ~ retcaixa_w", data=df).fit(cov_type="HC1")
m2 = smf.ols("qtobin_w ~ retcaixa_w + roa_w + tam_w + c_rec_w + prej + gov",
             data=df).fit(cov_type="HC1")
m3 = smf.ols("qtobin_w ~ retcaixa_w + roa_w + tam_w + c_rec_w + prej + gov + "
             "C(setor) + C(Ano)", data=df).fit(cov_type="HC1")
m4 = smf.ols("qtobin_w ~ retcaixa_w + roa_w + tam_w + c_rec_w + prej + gov + "
             "rc_gov", data=df).fit(cov_type="HC1")
m5 = smf.ols("qtobin_w ~ retcaixa_w + roa_w + tam_w + c_rec_w + prej + n1 + n2 + "
             "nm + rc_n1 + rc_n2 + rc_nm", data=df).fit(cov_type="HC1")
m6 = smf.ols("qtobin_w ~ retcaixa_w + rc2 + roa_w + tam_w + c_rec_w + prej + gov",
             data=df).fit(cov_type="HC1")
m7 = smf.ols("qtobin_w ~ retcaixa_w + rc2 + roa_w + tam_w + c_rec_w + prej + gov + "
             "rc_gov + rc2_gov + C(setor) + C(Ano)", data=df).fit(cov_type="HC1")
modelos = [m1, m2, m3, m4, m5, m6, m7]
nomes_modelos = ["M1", "M2", "M3", "M4", "M5", "M6", "M7"]
info_dict = {
    "N": lambda x: f"{int(x.nobs)}",
    "R²": lambda x: f"{x.rsquared:.4f}",
    "R² ajustado": lambda x: f"{x.rsquared_adj:.4f}",
    "Estatística F": lambda x: f"{float(x.fvalue):.4f}",
    "p-valor F": lambda x: f"{float(x.f_pvalue):.4f}"
}
tabela_final = summary_col(modelos, stars=True, float_format="%0.4f",
                           model_names=nomes_modelos, info_dict=info_dict,
                           regressor_order=["Intercept", "retcaixa_w", "rc2",
                                            "roa_w", "tam_w", "c_rec_w", "prej",
                                            "gov", "n1", "n2", "nm", "rc_gov",
                                            "rc_n1", "rc_n2", "rc_nm", "rc2_gov"],
                           drop_omitted=True)
print(tabela_final)

tabela_df = tabela_final.tables[0].copy()
tabela_df.loc["Controle de setor"] = ["Não", "Não", "Sim", "Não", "Não", "Não",
                                      "Sim"]
tabela_df.loc["Controle de ano"] = ["Não", "Não", "Sim", "Não", "Não", "Não", "Sim"]
tabela_df.loc["Erros-padrão robustos"] = ["Sim"] * 7
print(tabela_df)
tabela_df.to_excel("resultados/tabela_final_modelos.xlsx")
tabela_df.to_csv("resultados/tabela_final_modelos.csv", encoding="utf-8-sig")
with open("resultados/tabela_final_modelos.txt", "w",
          encoding="utf-8") as arquivo:
    arquivo.write(tabela_df.to_string())

# Item 177 - (resposta ao problema de pesquisa no relatório)

# Item 178 - Salva a base final e encerra a análise
df.to_excel("resultados/base_final_analises.xlsx", index=False)
print("\nRESUMO FINAL DA ANÁLISE")
print("-" * 50)
print("Número de observações:", len(df))
print("Número de empresas:", df["id"].nunique())
print("Período:", df["Ano"].min(), "a", df["Ano"].max())
print("-" * 50)
print("Análise concluída. Verifique as pastas resultados e figuras.")