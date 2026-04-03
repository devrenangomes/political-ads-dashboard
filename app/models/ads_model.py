# app/models/ads_model.py

import pandas as pd

# ─────────────────────────────────────────
# CARGA E LIMPEZA
# ─────────────────────────────────────────

def load_data():
    """Carrega e prepara o dataset de ameaças cibernéticas."""
    df = pd.read_csv('data/Global_Cybersecurity_Threats_2015-2024.csv').copy()

    df = df.rename(columns={
        'Country': 'country',
        'Year': 'year',
        'Attack Type': 'attack_type',
        'Target Industry': 'target_industry',
        'Financial Loss (in Million $)': 'financial_loss',
        'Number of Affected Users': 'affected_users',
        'Attack Source': 'attack_source',
        'Security Vulnerability Type': 'vulnerability_type',
        'Defense Mechanism Used': 'defense_mechanism',
        'Incident Resolution Time (in Hours)': 'resolution_time_hours'
    })

    cat_cols = ['country', 'attack_type', 'target_industry',
                'attack_source', 'vulnerability_type', 'defense_mechanism']
    for col in cat_cols:
        df[col] = df[col].astype('category')

    df['severity'] = pd.qcut(
        df['financial_loss'], q=3, labels=['baixo', 'médio', 'alto']
    )
    df['response_speed'] = pd.cut(
        df['resolution_time_hours'],
        bins=[0, 24, 48, 72],
        labels=['rápido', 'médio', 'lento']
    )

    return df


# ─────────────────────────────────────────
# FUNÇÕES DE ANÁLISE (para os gráficos)
# ─────────────────────────────────────────

def ataques_por_ano(df):
    """Gráfico 1 — Total de ataques por ano."""
    return df.groupby('year').size().reset_index(name='total_ataques')


def prejuizo_por_pais(df):
    """Gráfico 2 — Prejuízo total e médio por país."""
    return (
        df.groupby('country')['financial_loss']
        .agg(['mean', 'sum', 'count'])
        .reset_index()
        .rename(columns={'mean': 'media', 'sum': 'total', 'count': 'qtd_ataques'})
        .sort_values('total', ascending=False)
    )


def cross_ataque_industria(df):
    """Gráfico 3 — Heatmap: frequência de ataque por tipo e indústria."""
    return pd.crosstab(df['attack_type'], df['target_industry'])


def eficiencia_defesa(df):
    """Gráfico 4 — Tempo médio de resolução por mecanismo de defesa."""
    return (
        df.groupby('defense_mechanism')['resolution_time_hours']
        .mean()
        .reset_index()
        .rename(columns={'resolution_time_hours': 'media_horas'})
        .sort_values('media_horas')
    )


def severidade_por_ataque(df):
    """Gráfico 5 — Distribuição de severidade por tipo de ataque."""
    return (
        df.groupby(['attack_type', 'severity'], observed=True)
        .size()
        .reset_index(name='quantidade')
    )
