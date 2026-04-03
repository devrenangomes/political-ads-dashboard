from flask import Blueprint, render_template
import plotly.express as px
import plotly.utils
import json

from app.models.ads_model import (
    load_data,
    ataques_por_ano,
    prejuizo_por_pais,
    cross_ataque_industria,
    eficiencia_defesa,
    severidade_por_ataque
)

dashboard_bp = Blueprint('dashboard', __name__)


def _to_json(fig):
    """Converte uma figura Plotly para JSON seguro para o HTML."""
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


@dashboard_bp.route('/')
def index():
    df = load_data()

    # --- Gráfico 1: Linha — Ataques por ano ---
    dados_ano = ataques_por_ano(df)
    fig1 = px.line(
        dados_ano, x='year', y='total_ataques',
        title='Ataques Cibernéticos por Ano (2015–2024)',
        markers=True
    )

    # --- Gráfico 2: Barras — Prejuízo financeiro por país ---
    dados_pais = prejuizo_por_pais(df)
    fig2 = px.bar(
        dados_pais, x='country', y='total',
        title='Prejuízo Financeiro Total por País (USD)',
        color='media'
    )

    # --- Gráfico 3: Heatmap — Tipo de ataque × Indústria ---
    dados_cross = cross_ataque_industria(df)
    fig3 = px.imshow(
        dados_cross,
        title='Frequência de Ataques por Tipo e Indústria',
        color_continuous_scale='Reds',
        aspect='auto'
    )

    # --- Gráfico 4: Barras horizontais — Eficiência de defesa ---
    dados_defesa = eficiencia_defesa(df)
    fig4 = px.bar(
        dados_defesa, x='media_horas', y='defense_mechanism',
        orientation='h',
        title='Tempo Médio de Resposta por Mecanismo de Defesa (horas)'
    )

    # --- Gráfico 5: Histograma — Severidade por tipo de ataque ---
    dados_sev = severidade_por_ataque(df)
    fig5 = px.bar(
        dados_sev, x='attack_type', y='quantidade',
        color='severity',
        title='Distribuição de Severidade por Tipo de Ataque',
        barmode='stack'
    )

    return render_template(
        'dashboard.html',
        grafico1=_to_json(fig1),
        grafico2=_to_json(fig2),
        grafico3=_to_json(fig3),
        grafico4=_to_json(fig4),
        grafico5=_to_json(fig5),
    )