from app import app
from flask import render_template
import plotly.express as px

# 1. Importando TODAS as funções que você criou no ads_model.py
from app.models.ads_model import (
    load_data, 
    ataques_por_ano, 
    prejuizo_por_pais,
    cross_ataque_industria,
    eficiencia_defesa,
    severidade_por_ataque
)

@app.route('/')
def index():
    # Carrega os dados uma vez só
    df = load_data()
    
    # ─── GRÁFICO 1: Barras (Ataques por Ano) ─────────────────────────
    df_grafico1 = ataques_por_ano(df)
    fig1 = px.bar(df_grafico1, x='year', y='total_ataques', title='Total de Ataques por Ano')
    html_grafico1 = fig1.to_html(full_html=False)
    
    # ─── GRÁFICO 2: Barras (Prejuízo por País - Top 10) ──────────────
    df_grafico2 = prejuizo_por_pais(df)
    fig2 = px.bar(df_grafico2.head(10), x='country', y='total', title='Top 10 Países com Maior Prejuízo')
    html_grafico2 = fig2.to_html(full_html=False)

    # ─── GRÁFICO 3: Mapa de Calor (Ataque x Indústria) ───────────────
    # px.imshow é ótimo para mostrar tabelas cruzadas (crosstab)
    df_grafico3 = cross_ataque_industria(df)
    fig3 = px.imshow(df_grafico3, title='Frequência: Tipo de Ataque x Indústria')
    html_grafico3 = fig3.to_html(full_html=False)

    # ─── GRÁFICO 4: Barras (Eficiência da Defesa) ────────────────────
    df_grafico4 = eficiencia_defesa(df)
    fig4 = px.bar(df_grafico4, x='defense_mechanism', y='media_horas', title='Tempo Médio de Resolução (por Defesa)')
    html_grafico4 = fig4.to_html(full_html=False)

    # ─── GRÁFICO 5: Barras Agrupadas (Severidade) ────────────────────
    # Usamos o 'color' para separar as barras por severidade e barmode='group' para colocá-las lado a lado
    df_grafico5 = severidade_por_ataque(df)
    fig5 = px.bar(df_grafico5, x='attack_type', y='quantidade', color='severity', barmode='group', title='Severidade por Tipo de Ataque')
    html_grafico5 = fig5.to_html(full_html=False)

    # 4. Entregar TODOS os 5 gráficos para o dashboard.html
    return render_template(
        'dashboard.html', 
        grafico1=html_grafico1, 
        grafico2=html_grafico2,
        grafico3=html_grafico3,
        grafico4=html_grafico4,
        grafico5=html_grafico5
    )