# =============================================================================
# Conteúdo: Parte 1 (preparação e tratamento dos dados)       itens 0  a 37
#           Parte 2 (estatística descritiva e frequências)    itens 38 a 49
#           Parte 3 (correlação e associação)                 itens 50 a 57
#           Parte 4 (testes de hipóteses)                     itens 58 a 75
# Ao final, este script salva "resultados/base_parte1.xlsx", que é o ponto de
# partida do arquivo 2 (lista_pratica_parte2.py)
# =============================================================================

# Parte 1 - Preparação do ambiente e tratamento dos dados
# Item 4 - Criação do arquivo principal

# Item 7 - Importação das bibliotecas
import os
import pandas as pd                      # leitura e tratamento das bases
import numpy as np                       # operações numéricas
import matplotlib.pyplot as plt          # gráficos
import scipy.stats as stats              # testes estatísticos
import statsmodels.api as sm             # modelos e testes (ex.: proporções)
import statsmodels.formula.api as smf    # modelos via fórmula (usado na parte 2)

# Garante que as pastas de saída existam (caso o script rode em outra máquina)
for pasta in ["resultados", "figuras"]:
    os.makedirs(pasta, exist_ok=True)

# -----------------------------------------------------------------------------
# Item 8 - Importação da base de dados original (sem nenhum tratamento manual)
df = pd.read_excel("dados/Base - LP1.xlsx")

# Item 9 - Verifica se a importação funcionou (5 primeiras linhas)
print(df.head())

# Item 10 - Nomes das variáveis exatamente como o Python os reconheceu
print(df.columns.tolist())

# Item 11 - Tipos das variáveis: colunas numéricas com "-" aparecem como object
print(df.dtypes)

# -----------------------------------------------------------------------------
# Item 12 - Converte as variáveis econômico-financeiras para formato numérico.
# errors="coerce" transforma em NaN qualquer valor não numérico (como "-").
vars_num = [
    "Lucro Liquido\n",
    "PtLqCo\n ",
    "EBIT\n",
    "Ativo Tot\n",
    "LPA",
    "PasCir\n  ",
    "AtvCir",
    "Estoques",
    "EstqLP",
    "PasNoCir",
    "CaixaEEqCx",
    "TotEmFiCP",
    "TotEmFiLP",
    "CxOper",
    "Receita",
    "CapGir",
    "Valor Mercado\nda empresa"
]
for v in vars_num:
    df[v] = pd.to_numeric(df[v], errors="coerce")
print(df[vars_num].dtypes)

# -----------------------------------------------------------------------------
# Item 13 - Distribuição das observações por setor (antes das exclusões)
freq_setor = df["Setor Econômico\nBovespa"].value_counts().reset_index()
freq_setor.columns = ["Setor", "Frequência"]
freq_setor["Percentual"] = (
    freq_setor["Frequência"] / freq_setor["Frequência"].sum() * 100
)
print(freq_setor)
freq_setor.to_excel("resultados/frequencia_setores.xlsx", index=False)

# Item 14 - Exclui setores Financeiro, Outros e sem identificação ("-")
# ~ inverte a condição de .isin(): ficam apenas os demais setores
df = df[
    ~df["Setor Econômico\nBovespa"].isin(["Financeiro", "Outros", "-"])
].copy()
print(df["Setor Econômico\nBovespa"].value_counts())

# Item 15 - Exclui a variável CNPJ (não utilizada nas análises)
df = df.drop(columns=["CNPJ"])
print(df.columns.tolist())

# Item 16 - Exclui as colunas duplicadas (sufixo .1 criado pelo pandas)
df = df.drop(columns=["Bolsa / Fonte.1", "Ativo /\nCancelado.1"])
print(df.columns.tolist())

# Item 17 - Delimita o período da amostra: 2010 a 2020
df = df[
    (df["Ano"] >= 2010) &
    (df["Ano"] <= 2020)
].copy()
print(df["Ano"].min())
print(df["Ano"].max())

# Item 18 - Renomeia as principais variáveis com nomes curtos
df = df.rename(columns={
    "ID da\nempresa": "id",
    "Setor Econômico\nBovespa": "setor",
    "Segmento listagem\nBovespa": "governanca",
    "Lucro Liquido\n": "ll",
    "PtLqCo\n ": "pl",
    "Ativo Tot\n": "ativo",
    "Valor Mercado\nda empresa": "vm"
})
print(df.columns.tolist())

# Item 19 - Estrutura da base após os tratamentos
df.info()

# -----------------------------------------------------------------------------
# Item 20 - Retenção de caixa: caixa e equivalentes / ativo total
df["retcaixa"] = df["CaixaEEqCx"] / df["ativo"]
print(df[["CaixaEEqCx", "ativo", "retcaixa"]].head())

# Item 21 - Q de Tobin: (valor de mercado + passivo circulante + passivo
# não circulante) / ativo total -> proxy do valor de mercado da empresa
df["qtobin"] = (
    df["vm"] + df["PasCir\n  "] + df["PasNoCir"]
) / df["ativo"]
print(df[["vm", "PasCir\n  ", "PasNoCir", "ativo", "qtobin"]].head())

# Item 22 - Tamanho: logaritmo natural do ativo total
df["tam"] = np.log(df["ativo"])
print(df[["ativo", "tam"]].head())

# Item 23 - Organiza como painel (empresa x ano), necessário para defasagens
df = df.sort_values(["id", "Ano"]).reset_index(drop=True)
print(df[["id", "Ano"]].head(15))

# Item 24 - ROA = lucro líquido(t) / ativo total(t-1)
# groupby("id") garante que a defasagem é feita dentro de cada empresa
df["ativo_lag"] = df.groupby("id")["ativo"].shift(1)
df["roa"] = df["ll"] / df["ativo_lag"]
print(df[["id", "Ano", "ll", "ativo", "ativo_lag", "roa"]].head(15))

# -----------------------------------------------------------------------------
# Item 25 - Distribuição das observações entre segmentos de governança
freq_gov = df["governanca"].value_counts().reset_index()
freq_gov.columns = ["Segmento", "Frequência"]
freq_gov["Percentual"] = (
    freq_gov["Frequência"] / freq_gov["Frequência"].sum() * 100
)
print(freq_gov)
freq_gov.to_excel("resultados/frequencia_governanca.xlsx", index=False)

# Item 26 - Dummies de governança corporativa (segmentos da B3)
df["gov"] = np.where(
    df["governanca"].isin(["Nível 1", "Nível 2", "Novo Mercado"]),
    1, 0
)
df["n1"] = np.where(df["governanca"] == "Nível 1", 1, 0)
df["n2"] = np.where(df["governanca"] == "Nível 2", 1, 0)
df["nm"] = np.where(df["governanca"] == "Novo Mercado", 1, 0)
print(df[["governanca", "gov", "n1", "n2", "nm"]].head(20))

# Item 27 - Demais variáveis
# Dummy de prejuízo (mantém NaN quando o lucro é ausente)
df["prej"] = np.where(
    df["ll"].isna(),
    np.nan,
    np.where(df["ll"] < 0, 1, 0)
)
# Crescimento da receita em relação ao ano anterior da mesma empresa
df["receita_lag"] = df.groupby("id")["Receita"].shift(1)
df["c_rec"] = (
    (df["Receita"] - df["receita_lag"]) /
    df["receita_lag"]
)
# Dummy de crescimento da receita (mantém NaN quando c_rec é ausente)
df["d_crescrec"] = np.where(
    df["c_rec"].isna(),
    np.nan,
    np.where(df["c_rec"] > 0, 1, 0)
)
# Dummy do setor de petróleo, gás e biocombustíveis
df["petgas"] = np.where(
    df["setor"] == "Petróleo gás e biocombustíveis",
    1,
    0
)
print(df[["id", "Ano", "prej", "c_rec", "d_crescrec", "petgas"]].head(15))

# Item 28 - Exclui patrimônio líquido não positivo (mantém os ausentes)
df = df[
    (df["pl"] > 0) | (df["pl"].isna())
].copy()
print(df["pl"].describe())

# Item 29 - Dummy de empresas SEM retenção de caixa (retcaixa = 0)
df["d_retcaixa"] = np.where(
    df["retcaixa"].isna(),
    np.nan,
    np.where(df["retcaixa"] == 0, 1, 0)
)

# Item 30 - Variáveis construídas a partir de várias observações
# Lucro máximo da amostra e diferença em relação a ele
df["lmax"] = df["ll"].max()
df["diflucro"] = df["ll"] - df["lmax"]
# Lucro médio da amostra e diferença em relação a ele
df["lmedio"] = df["ll"].mean()
df["diflucrom"] = df["ll"] - df["lmedio"]
# Lucro máximo do setor e diferença (transform devolve o valor em cada linha)
df["lmaxs"] = df.groupby("setor")["ll"].transform("max")
df["diflucros"] = df["ll"] - df["lmaxs"]
# Lucro médio do setor e diferença
df["lmedios"] = df.groupby("setor")["ll"].transform("mean")
df["diflucroms"] = df["ll"] - df["lmedios"]
# Risco1: amplitude do ROA no setor
df["roamax"] = df.groupby("setor")["roa"].transform("max")
df["roamin"] = df.groupby("setor")["roa"].transform("min")
df["risco1"] = df["roamax"] - df["roamin"]
# Risco2: coeficiente de variação do ROA no setor
df["dproa"] = df.groupby("setor")["roa"].transform("std")
df["mediaroa"] = df.groupby("setor")["roa"].transform("mean")
df["risco2"] = df["dproa"] / df["mediaroa"]
# Market share: participação do valor de mercado da empresa no setor
df["vm_setor"] = df.groupby("setor")["vm"].transform("sum")
df["marketshare"] = df["vm"] / df["vm_setor"]

# Item 31 - Substitui valores infinitos (divisão por zero, log(0)) por NaN
df = df.replace([np.inf, -np.inf], np.nan)

# Item 32 - Mantém apenas observações completas nas variáveis da pesquisa
vars_pesquisa = [
    "qtobin", "retcaixa", "gov", "n1", "n2",
    "nm", "tam", "roa", "c_rec", "prej"
]
df = df.dropna(subset=vars_pesquisa).copy()
print(df.shape)

# -----------------------------------------------------------------------------
# Item 33 - Box-Plots das variáveis contínuas (antes da winsorização)
vars_continuas = ["qtobin", "retcaixa", "tam", "roa", "c_rec"]
for v in vars_continuas:
    plt.figure()
    plt.boxplot(df[v].dropna())
    plt.title(f"Box-Plot - {v}")
    plt.ylabel(v)
    plt.tight_layout()
    plt.savefig(f"figuras/boxplot_{v}.png", dpi=300, bbox_inches="tight")
    plt.show()

# Item 34 - Box-Plot do lucro líquido por segmento de governança
plt.figure(figsize=(10, 6))
df.boxplot(column="ll", by="governanca")
plt.title("Lucro líquido por segmento de governança")
plt.suptitle("")
plt.xlabel("Segmento de governança")
plt.ylabel("Lucro líquido")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("figuras/boxplot_ll_governanca.png", dpi=300, bbox_inches="tight")
plt.show()

# Box-Plot do lucro líquido por governança e crescimento da receita
plt.figure(figsize=(12, 6))
df.boxplot(column="ll", by=["governanca", "d_crescrec"])
plt.title("Lucro líquido por governança e crescimento da receita")
plt.suptitle("")
plt.xlabel("Governança e crescimento da receita")
plt.ylabel("Lucro líquido")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("figuras/boxplot_ll_governanca_crescrec.png", dpi=300,
            bbox_inches="tight")
plt.show()

# Item 35 - Winsorização a 1% e 99% (cria variáveis com sufixo _w)
vars_winsor = ["qtobin", "retcaixa", "tam", "roa", "c_rec"]
for v in vars_winsor:
    p1 = df[v].quantile(0.01)
    p99 = df[v].quantile(0.99)
    df[v + "_w"] = df[v].clip(lower=p1, upper=p99)

# Item 36 - Mantém apenas as variáveis usadas nas etapas seguintes
vars_finais = [
    "id", "Ano", "setor", "governanca",
    "ll", "pl",
    "qtobin_w", "retcaixa_w",
    "d_retcaixa",
    "gov", "n1", "n2", "nm",
    "tam_w", "roa_w", "c_rec_w",
    "prej", "d_crescrec"
]
df = df[vars_finais].copy()
df.info()

# Item 37 - Salva a base tratada
df.to_excel("resultados/base_tratada.xlsx", index=False)

# =============================================================================
# Parte 2 - Estatística descritiva e tabelas de frequência
# =============================================================================

# Item 38 - Frequência absoluta e relativa de d_retcaixa
freq_retcaixa = pd.DataFrame({
    "Frequência": df["d_retcaixa"].value_counts().sort_index(),
    "Percentual": df["d_retcaixa"].value_counts(normalize=True).sort_index() * 100
})
print(freq_retcaixa)
freq_retcaixa.to_excel("resultados/frequencia_d_retcaixa.xlsx")

# Item 39 - Frequência conjunta governança x setor
freq_gov_setor = pd.crosstab(df["governanca"], df["setor"])
print(freq_gov_setor)
freq_gov_setor.to_excel("resultados/frequencia_governanca_setor.xlsx")

# Item 40 - Frequência relativa conjunta (% do total de observações)
freq_rel_gov_setor = pd.crosstab(
    df["governanca"], df["setor"], normalize="all"
) * 100
print(freq_rel_gov_setor)
freq_rel_gov_setor.to_excel("resultados/frequencia_relativa_governanca_setor.xlsx")

# Item 41 - Frequência relativa governança x setor para prej = 0 e prej = 1
for grupo, dados in df.groupby("prej"):
    tabela = pd.crosstab(
        dados["governanca"], dados["setor"], normalize="all"
    ) * 100
    print(f"\nPrejuízo = {grupo}")
    print(tabela)
    tabela.to_excel(f"resultados/frequencia_governanca_setor_prej_{grupo}.xlsx")

# Item 42 - Estatísticas descritivas das variáveis da pesquisa
vars_desc = [
    "qtobin_w", "retcaixa_w",
    "gov", "n1", "n2", "nm",
    "tam_w", "roa_w", "c_rec_w", "prej"
]
descritiva = df[vars_desc].describe().T
print(descritiva)
descritiva.to_excel("resultados/estatistica_descritiva.xlsx")

# Item 43 - Descritiva com coeficiente de variação (CV = desvio padrão / média)
descritiva_cv = pd.DataFrame({
    "N": df[vars_desc].count(),
    "Média": df[vars_desc].mean(),
    "CV": df[vars_desc].std() / df[vars_desc].mean(),
    "Mínimo": df[vars_desc].min(),
    "Q1": df[vars_desc].quantile(0.25),
    "Mediana": df[vars_desc].median(),
    "Q3": df[vars_desc].quantile(0.75),
    "Máximo": df[vars_desc].max()
})
print(descritiva_cv)
descritiva_cv.to_excel("resultados/estatistica_descritiva_cv.xlsx")

# Item 44 - Mesma tabela separada por gov = 0 e gov = 1 (uma aba por grupo)
with pd.ExcelWriter("resultados/descritiva_por_governanca.xlsx") as writer:
    for grupo, dados in df.groupby("gov"):
        tabela = pd.DataFrame({
            "N": dados[vars_desc].count(),
            "Média": dados[vars_desc].mean(),
            "CV": dados[vars_desc].std() / dados[vars_desc].mean(),
            "Mínimo": dados[vars_desc].min(),
            "Q1": dados[vars_desc].quantile(0.25),
            "Mediana": dados[vars_desc].median(),
            "Q3": dados[vars_desc].quantile(0.75),
            "Máximo": dados[vars_desc].max()
        })
        print(f"\nGovernança = {grupo}")
        print(tabela)
        tabela.to_excel(writer, sheet_name=f"gov_{grupo}")

# Item 45 - Descritiva apenas das empresas com governança diferenciada
df_gov = df[df["gov"] == 1]
desc_gov = df_gov[vars_desc].describe().T
print(desc_gov)
desc_gov.to_excel("resultados/descritiva_empresas_governanca.xlsx")

# Item 46 - Descritiva do setor de Consumo cíclico
df_consumo = df[df["setor"] == "Consumo cíclico"]
desc_consumo = df_consumo[vars_desc].describe().T
print(desc_consumo)
desc_consumo.to_excel("resultados/descritiva_consumo_ciclico.xlsx")

# Item 47 - Descritiva de empresas com lucro (ll > 0) e com prejuízo (ll < 0)
df_lucro = df[df["ll"] > 0]
df_prejuizo = df[df["ll"] < 0]
desc_lucro = df_lucro[vars_desc].describe().T
desc_prejuizo = df_prejuizo[vars_desc].describe().T
print("\nEmpresas com lucro:")
print(desc_lucro)
print("\nEmpresas com prejuízo:")
print(desc_prejuizo)
with pd.ExcelWriter("resultados/descritiva_lucro_prejuizo.xlsx") as writer:
    desc_lucro.to_excel(writer, sheet_name="Lucro")
    desc_prejuizo.to_excel(writer, sheet_name="Prejuizo")

# Item 48 - Empresas com prejuízo, separadas por governança
df_prejuizo = df[df["ll"] < 0]
with pd.ExcelWriter("resultados/descritiva_prejuizo_por_governanca.xlsx") as writer:
    for grupo, dados in df_prejuizo.groupby("gov"):
        tabela = dados[vars_desc].describe().T
        print(f"\nPrejuízo - Governança = {grupo}")
        print(tabela)
        tabela.to_excel(writer, sheet_name=f"gov_{grupo}")

# Item 49 - Q de Tobin (N, média e desvio padrão) por segmento de governança
qtobin_governanca = (
    df.groupby("governanca")["qtobin_w"]
    .agg(N="count", Média="mean", Desvio_Padrão="std")
)
print(qtobin_governanca)
qtobin_governanca.to_excel("resultados/qtobin_por_governanca.xlsx")

# =============================================================================
# Parte 3 - Correlação e associação entre as variáveis
# =============================================================================

# Item 50 - Matriz de correlação de Pearson das variáveis contínuas
vars_corr = ["qtobin_w", "retcaixa_w", "tam_w", "roa_w", "c_rec_w"]
corr = df[vars_corr].corr()
print(corr)
corr.to_excel("resultados/correlacao_variaveis_continuas.xlsx")

# Item 51 - Correlações acompanhadas das médias
corr_media = corr.copy()
corr_media["Média"] = df[vars_corr].mean()
print(corr_media)
corr_media.to_excel("resultados/correlacao_com_medias.xlsx")

# Item 52 - Correlações separadas por gov = 0 e gov = 1
with pd.ExcelWriter("resultados/correlacao_por_governanca.xlsx") as writer:
    for grupo, dados in df.groupby("gov"):
        tabela = dados[vars_corr].corr()
        print(f"\nGovernança = {grupo}")
        print(tabela)
        tabela.to_excel(writer, sheet_name=f"gov_{grupo}")

# Item 53 - Correlações apenas entre empresas com lucro
df_lucro = df[df["ll"] > 0]
corr_lucro = df_lucro[vars_corr].corr()
print(corr_lucro)
corr_lucro.to_excel("resultados/correlacao_empresas_lucro.xlsx")

# Item 54 - Matriz de covariância
cov = df[vars_corr].cov()
print(cov)
cov.to_excel("resultados/covariancia_variaveis_continuas.xlsx")

# Item 55 - Matriz de gráficos de dispersão
pd.plotting.scatter_matrix(df[vars_corr], figsize=(12, 12),
                           diagonal="hist", alpha=0.5)
plt.suptitle("Matriz de dispersão das variáveis contínuas")
plt.tight_layout()
plt.savefig("figuras/matriz_dispersao_variaveis.png", dpi=300,
            bbox_inches="tight")
plt.show()

# Item 56 - Correlações e p-valores (H0: rho = 0  vs  H1: rho != 0)
corr_p = pd.DataFrame(index=vars_corr, columns=vars_corr, dtype=float)
pval = pd.DataFrame(index=vars_corr, columns=vars_corr, dtype=float)
for v1 in vars_corr:
    for v2 in vars_corr:
        r, p = stats.pearsonr(df[v1], df[v2])
        corr_p.loc[v1, v2] = r
        pval.loc[v1, v2] = p
print("\nCorrelações:")
print(corr_p)
print("\nP-valores:")
print(pval)
with pd.ExcelWriter("resultados/correlacao_pvalores.xlsx") as writer:
    corr_p.to_excel(writer, sheet_name="Correlacoes")
    pval.to_excel(writer, sheet_name="P_valores")

# Item 57 - Matriz de correlação com asteriscos de significância
# * 10%  |  ** 5%  |  *** 1%
corr_sig = corr_p.copy().astype(object)
for v1 in vars_corr:
    for v2 in vars_corr:
        valor = corr_p.loc[v1, v2]
        p = pval.loc[v1, v2]
        if p < 0.01:
            estrelas = "***"
        elif p < 0.05:
            estrelas = "**"
        elif p < 0.10:
            estrelas = "*"
        else:
            estrelas = ""
        corr_sig.loc[v1, v2] = f"{valor:.4f}{estrelas}"
print(corr_sig)
corr_sig.to_excel("resultados/correlacao_com_significancia.xlsx")

# =============================================================================
# Parte 4 - Testes de hipóteses
# =============================================================================

# Item 58 - Teste t de uma amostra: H0: mu_LL = 0  vs  H1: mu_LL > 0
teste_58 = stats.ttest_1samp(df["ll"], popmean=0, alternative="greater")
resultado_58 = pd.DataFrame({
    "Estatística t": [teste_58.statistic],
    "p-valor": [teste_58.pvalue],
    "Média amostral": [df["ll"].mean()],
    "N": [df["ll"].count()]
})
print(resultado_58)
resultado_58.to_excel("resultados/teste_lucro_positivo.xlsx", index=False)

# Item 59 - H0: mu_LL = 400.000  vs  H1: mu_LL < 400.000
teste_59 = stats.ttest_1samp(df["ll"], popmean=400000, alternative="less")
resultado_59 = pd.DataFrame({
    "Estatística t": [teste_59.statistic],
    "p-valor": [teste_59.pvalue],
    "Média amostral": [df["ll"].mean()],
    "N": [df["ll"].count()]
})
print(resultado_59)
resultado_59.to_excel("resultados/teste_lucro_menor_400mil.xlsx", index=False)

# Item 60 - Teste z de proporção: H0: p = 0,80  vs  H1: p > 0,80 (gov)
sucessos = int(df["gov"].sum())
n = int(df["gov"].count())
z_60, p_60 = sm.stats.proportions_ztest(count=sucessos, nobs=n, value=0.80,
                                        alternative="larger")
resultado_60 = pd.DataFrame({
    "Proporção amostral": [df["gov"].mean()],
    "Estatística z": [z_60],
    "p-valor": [p_60],
    "N": [n]
})
print(resultado_60)
resultado_60.to_excel("resultados/teste_proporcao_governanca.xlsx", index=False)

# Item 61 - H0: p = 0,40  vs  H1: p > 0,40 (Novo Mercado)
sucessos = int(df["nm"].sum())
n = int(df["nm"].count())
z_61, p_61 = sm.stats.proportions_ztest(count=sucessos, nobs=n, value=0.40,
                                        alternative="larger")
resultado_61 = pd.DataFrame({
    "Proporção amostral": [df["nm"].mean()],
    "Estatística z": [z_61],
    "p-valor": [p_61],
    "N": [n]
})
print(resultado_61)
resultado_61.to_excel("resultados/teste_proporcao_novo_mercado.xlsx", index=False)

# Item 62 - H0: mu_retcaixa = 0,10  vs  H1: mu_retcaixa > 0,10
teste_62 = stats.ttest_1samp(df["retcaixa_w"], popmean=0.10,
                             alternative="greater")
resultado_62 = pd.DataFrame({
    "Média amostral": [df["retcaixa_w"].mean()],
    "Estatística t": [teste_62.statistic],
    "p-valor": [teste_62.pvalue],
    "N": [df["retcaixa_w"].count()]
})
print(resultado_62)
resultado_62.to_excel("resultados/teste_retencao_maior_10.xlsx", index=False)

# Item 63 - Mesmo teste por segmento de governança
resultados_63 = []
for grupo, dados in df.groupby("governanca"):
    teste = stats.ttest_1samp(dados["retcaixa_w"], popmean=0.10,
                              alternative="greater")
    resultados_63.append({
        "Governança": grupo,
        "Média": dados["retcaixa_w"].mean(),
        "Estatística t": teste.statistic,
        "p-valor": teste.pvalue,
        "N": dados["retcaixa_w"].count()
    })
resultado_63 = pd.DataFrame(resultados_63)
print(resultado_63)
resultado_63.to_excel("resultados/teste_retencao_por_governanca.xlsx", index=False)

# Item 64 - Mesmo teste por segmento, só no setor de Consumo cíclico
df_consumo = df[df["setor"] == "Consumo cíclico"]
resultados_64 = []
for grupo, dados in df_consumo.groupby("governanca"):
    teste = stats.ttest_1samp(dados["retcaixa_w"], popmean=0.10,
                              alternative="greater")
    resultados_64.append({
        "Governança": grupo,
        "Média": dados["retcaixa_w"].mean(),
        "Estatística t": teste.statistic,
        "p-valor": teste.pvalue,
        "N": dados["retcaixa_w"].count()
    })
resultado_64 = pd.DataFrame(resultados_64)
print(resultado_64)
resultado_64.to_excel("resultados/teste_retencao_consumo_ciclico.xlsx", index=False)

# Item 65 - ROE = lucro líquido(t) / patrimônio líquido(t-1)
df = df.sort_values(["id", "Ano"]).copy()
df["pl_lag"] = df.groupby("id")["pl"].shift(1)
df["roe"] = df["ll"] / df["pl_lag"]
df["roe"] = df["roe"].replace([np.inf, -np.inf], np.nan)

# Item 66 - Winsorização do ROE a 1% em cada cauda
lim_inf = df["roe"].quantile(0.01)
lim_sup = df["roe"].quantile(0.99)
df["roe_w"] = df["roe"].clip(lower=lim_inf, upper=lim_sup)

# Item 67 - Teste t pareado: H0: mu_ROA - mu_ROE = 0
dados_67 = df[["roa_w", "roe_w"]].dropna()
teste_67 = stats.ttest_rel(dados_67["roa_w"], dados_67["roe_w"])
resultado_67 = pd.DataFrame({
    "Média ROA": [dados_67["roa_w"].mean()],
    "Média ROE": [dados_67["roe_w"].mean()],
    "Diferença média": [dados_67["roa_w"].mean() - dados_67["roe_w"].mean()],
    "Estatística t": [teste_67.statistic],
    "p-valor": [teste_67.pvalue],
    "N": [len(dados_67)]
})
print(resultado_67)
resultado_67.to_excel("resultados/teste_roa_roe.xlsx", index=False)

# Item 68 - Q de Tobin: gov = 0 vs gov = 1
# 1º) Levene testa igualdade de variâncias; 2º) o resultado define se o
# teste t usa variâncias iguais (Student) ou diferentes (Welch)
grupo0 = df.loc[df["gov"] == 0, "qtobin_w"]
grupo1 = df.loc[df["gov"] == 1, "qtobin_w"]
teste_var_68 = stats.levene(grupo0, grupo1)
igual_var_68 = teste_var_68.pvalue >= 0.05
teste_media_68 = stats.ttest_ind(grupo0, grupo1, equal_var=igual_var_68)
resultado_68 = pd.DataFrame({
    "Média grupo 0": [grupo0.mean()],
    "Média grupo 1": [grupo1.mean()],
    "Levene p-valor": [teste_var_68.pvalue],
    "Variâncias iguais": [igual_var_68],
    "Estatística t": [teste_media_68.statistic],
    "p-valor média": [teste_media_68.pvalue]
})
print(resultado_68)
resultado_68.to_excel("resultados/teste_qtobin_governanca.xlsx", index=False)

# Item 69 - Q de Tobin: fora vs dentro do Novo Mercado
grupo0 = df.loc[df["nm"] == 0, "qtobin_w"]
grupo1 = df.loc[df["nm"] == 1, "qtobin_w"]
teste_var_69 = stats.levene(grupo0, grupo1)
igual_var_69 = teste_var_69.pvalue >= 0.05
teste_media_69 = stats.ttest_ind(grupo0, grupo1, equal_var=igual_var_69)
resultado_69 = pd.DataFrame({
    "Média grupo 0": [grupo0.mean()],
    "Média grupo 1": [grupo1.mean()],
    "Levene p-valor": [teste_var_69.pvalue],
    "Variâncias iguais": [igual_var_69],
    "Estatística t": [teste_media_69.statistic],
    "p-valor média": [teste_media_69.pvalue]
})
print(resultado_69)
resultado_69.to_excel("resultados/teste_qtobin_novo_mercado.xlsx", index=False)

# Item 70 - Dummy de retenção de caixa acima da mediana
mediana_retcaixa = df["retcaixa_w"].median()
df["d_rc"] = (df["retcaixa_w"] > mediana_retcaixa).astype(int)
print("Mediana da retenção de caixa:")
print(mediana_retcaixa)
print("\nFrequência de d_rc:")
print(df["d_rc"].value_counts())


# Item 71 - Empresas com retenção acima da mediana têm maior Q de Tobin?
# H0: mu_acima = mu_abaixo  vs  H1: mu_acima > mu_abaixo
# Levene define se o teste t usa variâncias iguais (Student) ou não (Welch)
abaixo = df.loc[df["d_rc"] == 0, "qtobin_w"]
acima = df.loc[df["d_rc"] == 1, "qtobin_w"]
teste_var_71 = stats.levene(abaixo, acima)
igual_var_71 = teste_var_71.pvalue >= 0.05
teste_media_71 = stats.ttest_ind(acima, abaixo, equal_var=igual_var_71,
                                 alternative="greater")
resultado_71 = pd.DataFrame({
    "Média abaixo": [abaixo.mean()],
    "Média acima": [acima.mean()],
    "Levene p-valor": [teste_var_71.pvalue],
    "Variâncias iguais": [igual_var_71],
    "Estatística t": [teste_media_71.statistic],
    "p-valor média": [teste_media_71.pvalue]
})
print(resultado_71)
resultado_71.to_excel("resultados/teste_qtobin_retencao_mediana.xlsx",
                      index=False)

# Item 72 - Mesmo teste separado para gov = 0 e gov = 1
resultados_72 = []
for grupo, dados in df.groupby("gov"):
    abaixo = dados.loc[dados["d_rc"] == 0, "qtobin_w"]
    acima = dados.loc[dados["d_rc"] == 1, "qtobin_w"]
    teste_var = stats.levene(abaixo, acima)
    igual_var = teste_var.pvalue >= 0.05
    teste_media = stats.ttest_ind(acima, abaixo, equal_var=igual_var,
                                  alternative="greater")
    resultados_72.append({
        "gov": grupo,
        "Média abaixo": abaixo.mean(),
        "Média acima": acima.mean(),
        "Levene p-valor": teste_var.pvalue,
        "Variâncias iguais": igual_var,
        "Estatística t": teste_media.statistic,
        "p-valor média": teste_media.pvalue
    })
resultado_72 = pd.DataFrame(resultados_72)
print(resultado_72)
resultado_72.to_excel("resultados/teste_retencao_por_gov.xlsx", index=False)

# Item 73 - Mesmo teste apenas para empresas do Nível 1
dados_grupo = df[df["n1"] == 1]
abaixo = dados_grupo.loc[dados_grupo["d_rc"] == 0, "qtobin_w"]
acima = dados_grupo.loc[dados_grupo["d_rc"] == 1, "qtobin_w"]
teste_var_73 = stats.levene(abaixo, acima)
igual_var_73 = teste_var_73.pvalue >= 0.05
teste_media_73 = stats.ttest_ind(acima, abaixo, equal_var=igual_var_73,
                                 alternative="greater")
resultado_73 = pd.DataFrame({
    "Média abaixo": [abaixo.mean()],
    "Média acima": [acima.mean()],
    "Levene p-valor": [teste_var_73.pvalue],
    "Variâncias iguais": [igual_var_73],
    "Estatística t": [teste_media_73.statistic],
    "p-valor média": [teste_media_73.pvalue]
})
print(resultado_73)
resultado_73.to_excel("resultados/teste_retencao_n1.xlsx", index=False)

# Item 74 - Mesmo teste apenas para empresas do Nível 2
dados_grupo = df[df["n2"] == 1]
abaixo = dados_grupo.loc[dados_grupo["d_rc"] == 0, "qtobin_w"]
acima = dados_grupo.loc[dados_grupo["d_rc"] == 1, "qtobin_w"]
teste_var_74 = stats.levene(abaixo, acima)
igual_var_74 = teste_var_74.pvalue >= 0.05
teste_media_74 = stats.ttest_ind(acima, abaixo, equal_var=igual_var_74,
                                 alternative="greater")
resultado_74 = pd.DataFrame({
    "Média abaixo": [abaixo.mean()],
    "Média acima": [acima.mean()],
    "Levene p-valor": [teste_var_74.pvalue],
    "Variâncias iguais": [igual_var_74],
    "Estatística t": [teste_media_74.statistic],
    "p-valor média": [teste_media_74.pvalue]
})
print(resultado_74)
resultado_74.to_excel("resultados/teste_retencao_n2.xlsx", index=False)

# Item 75 - Mesmo teste apenas para empresas do Novo Mercado
dados_grupo = df[df["nm"] == 1]
abaixo = dados_grupo.loc[dados_grupo["d_rc"] == 0, "qtobin_w"]
acima = dados_grupo.loc[dados_grupo["d_rc"] == 1, "qtobin_w"]
teste_var_75 = stats.levene(abaixo, acima)
igual_var_75 = teste_var_75.pvalue >= 0.05
teste_media_75 = stats.ttest_ind(acima, abaixo, equal_var=igual_var_75,
                                 alternative="greater")
resultado_75 = pd.DataFrame({
    "Média abaixo": [abaixo.mean()],
    "Média acima": [acima.mean()],
    "Levene p-valor": [teste_var_75.pvalue],
    "Variâncias iguais": [igual_var_75],
    "Estatística t": [teste_media_75.statistic],
    "p-valor média": [teste_media_75.pvalue]
})
print(resultado_75)
resultado_75.to_excel("resultados/teste_retencao_nm.xlsx", index=False)

# -----------------------------------------------------------------------------
# Continuação da lista na parte 2 (lista_pratica_parte2.py)
# Salva a base com as variáveis criadas nas Partes 1-4 (inclui roe, roe_w,
# pl_lag e d_rc). O arquivo lista_pratica_parte2.py começa lendo esta base.
df.to_excel("resultados/base_parte1.xlsx", index=False)
print("\nParte 1 concluída. Base salva em resultados/base_parte1.xlsx")
print("Observações:", len(df), "| Empresas:", df["id"].nunique())