from app import app
from flask import render_template, request
import plotly.express as px


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
    
    # --- PREPARANDO AS OPÇÕES PARA OS FILTROS ---
    # Pegamos valores únicos globais para preencher os <select> no HTML
    anos_disp = sorted(df['year'].dropna().unique())
    inds_disp = sorted(df['target_industry'].dropna().unique())
    sevs_disp = ['baixo', 'médio', 'alto'] # já categorizado no model
    atks_disp = sorted(df['attack_type'].dropna().unique())

    # --- CAPTURANDO PARÂMETROS ESPECÍFICOS DE CADA GRÁFICO ---
    g1_ind = request.args.get('g1_ind')
    g2_ano = request.args.get('g2_ano')
    g3_sev = request.args.get('g3_sev')
    g4_atk = request.args.get('g4_atk')
    g5_ind = request.args.get('g5_ind')

    # --- FUNÇÃO AUXILIAR DE ESTILIZAÇÃO DO PLOTLY ---
    def style_and_convert(fig):
        fig.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter, sans-serif", color="#cbd5e1"),
            margin=dict(t=50, l=20, r=20, b=20)
        )
        return fig.to_html(full_html=False, config={'displaylogo': False})

    # ─── GRÁFICO 1: Ataques por Ano (Filtro: Indústria) ─────────────────
    df1 = df.copy()
    if g1_ind: df1 = df1[df1['target_industry'] == g1_ind]
    fig1 = px.bar(ataques_por_ano(df1), x='year', y='total_ataques', title='Total de Ataques por Ano', color_discrete_sequence=['#0ea5e9'])
    html_grafico1 = style_and_convert(fig1)
    
    # ─── GRÁFICO 2: Top 10 Países (Filtro: Ano) ─────────────────────────
    df2 = df.copy()
    if g2_ano: df2 = df2[df2['year'] == int(g2_ano)]
    fig2 = px.bar(prejuizo_por_pais(df2).head(10), x='country', y='total', title='Top 10 Países com Maior Prejuízo', color_discrete_sequence=['#f43f5e'])
    html_grafico2 = style_and_convert(fig2)

    # ─── GRÁFICO 3: Frequência Ataque x Indústria (Filtro: Severidade) ──
    df3 = df.copy()
    if g3_sev: df3 = df3[df3['severity'] == g3_sev]
    fig3 = px.imshow(cross_ataque_industria(df3), title='Frequência: Tipo de Ataque x Indústria', color_continuous_scale='Tealgrn')
    html_grafico3 = style_and_convert(fig3)

    # ─── GRÁFICO 4: Eficiência da Defesa (Filtro: Tipo de Ataque) ───────
    df4 = df.copy()
    if g4_atk: df4 = df4[df4['attack_type'] == g4_atk]
    fig4 = px.bar(eficiencia_defesa(df4), x='defense_mechanism', y='media_horas', title='Tempo Médio de Resolução', color_discrete_sequence=['#10b981'])
    html_grafico4 = style_and_convert(fig4)

    # ─── GRÁFICO 5: Severidade por Ataque (Filtro: Indústria) ───────────
    df5 = df.copy()
    if g5_ind: df5 = df5[df5['target_industry'] == g5_ind]
    fig5 = px.bar(severidade_por_ataque(df5), x='attack_type', y='quantidade', color='severity', barmode='group', title='Severidade por Tipo de Ataque', color_discrete_map={'baixo': '#3b82f6', 'médio': '#eab308', 'alto': '#ef4444'})
    html_grafico5 = style_and_convert(fig5)

    # Entregar ao template HTML as opções de dropdowns e valores selecionados
    return render_template(
        'dashboard.html', 
        grafico1=html_grafico1, 
        grafico2=html_grafico2,
        grafico3=html_grafico3,
        grafico4=html_grafico4,
        grafico5=html_grafico5,
        anos=anos_disp,
        industrias=inds_disp,
        severidades=sevs_disp,
        ataques=atks_disp,
        g1_ind=g1_ind,
        g2_ano=g2_ano,
        g3_sev=g3_sev,
        g4_atk=g4_atk,
        g5_ind=g5_ind
    )