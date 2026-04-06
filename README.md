# 🛡️ Global Cybersecurity Threats Dashboard

Dashboard interativo de ameaças cibernéticas globais (2015–2024), construído com Flask e Plotly.
O projeto encontra-se **finalizado**, contendo a estruturação completa de análise de dados (EDA) e a interface visual web.

---

## 📚 Stack utilizada

### 🐍 Python 3
Linguagem principal do projeto. É o padrão da indústria para análise de dados e desenvolvimento web com foco em dados.

### 🐼 Pandas
Biblioteca de manipulação de dados. Usada para carregar o CSV, limpar os dados e gerar os DataFrames prontos para cada gráfico.

### 🌐 Flask
Framework web minimalista para Python. Responsável por:
- Servir a página principal e o roteamento da aplicação.
- Passar os parâmetros do model diretamente para a renderização visual.
- Renderizar os templates HTML com os gráficos dinâmicos.

### 📊 Plotly
Biblioteca de visualizações **interativas**. Os gráficos são montados no backend utilizando `plotly.express` e entregues de forma otimizada para o layout do HTML, preservando as habilidades de zoom e hover na interação com o usuário.

---

## 🗂️ Estrutura do projeto (MVC)

```text
political-ads-dashboard/
│
├── data/                          ← arquivos CSV brutos
│   └── Global_Cybersecurity_Threats_2015-2024.csv
│
├── app/
│   ├── __init__.py
│   ├── models/
│   │   └── ads_model.py           ← ⭐ MODEL: funções de negócio, processamento e análise
│   ├── controllers/
│   │   └── routes.py              ← CONTROLLER: rotas da web e formatação de gráficos Plotly
│   └── templates/
│       └── dashboard.html         ← VIEW: Layout final do dashboard interativo
│
├── static/                        ← arquivos estáticos da web (se aplicáveis)
│
├── notebooks/
│   └── eda_fase2.ipynb            ← análise exploratória (documentação/prototipação)
│
├── run.py                         ← ponto de entrada da aplicação
├── requirements.txt               ← dependências do projeto
└── README.md                      ← você está aqui
```

### O que cada camada faz

| Camada | Arquivo | Responsabilidade |
|---|---|---|
| **Model** | `ads_model.py` | Carrega CSV, limpa dados, define lógicas analíticas e retorna DataFrames manipulados |
| **Controller** | `routes.py` | Instancia os modelos, produz as visualizações em HTML via Plotly, e entrega-as para renderização da view |
| **View** | `dashboard.html` | Renderiza os cartões dos gráficos na interface responsiva |

> **Regra de ouro aplicada no projeto:** o controller não manipula os dados pesadamente ou faz agrupamentos (delega isso para o model). O model só cuida de dados e não lida com envio ou requisições web. Cada camada tem uma única responsabilidade.

---

## ⚙️ Como configurar e rodar o projeto

Faça os seguintes passos no terminal para visualizar o Dashboard interativo localmente:

```bash
# 1. Configurar um ambiente virtual limpo no sistema
python3 -m venv .venv

# 2. Ativar o respectivo ambiente virtual
source .venv/bin/activate      # Mac/Linux
# .venv\Scripts\activate       # Windows

# 3. Instalar o registro exato das dependências 
pip install -r requirements.txt

# 4. Rodar o servidor de desenvolvimento web
python run.py
```

Acesse no navegador: **http://localhost:5000**

---

## 📊 Gráficos e Insights Apresentados

O dashboard materializa os seguintes insights através de Plotly:
1. **Total de Ataques por Ano:** Gráfico de barras com a volumetria de vulnerabilidades no decorrer dos anos. 
2. **Top 10 Países com Maior Prejuízo:** Gráfico de barras hierárquico destacando os líderes de perdas econômicas no setor.
3. **Frequência: Tipo de Ataque x Indústria:** Gráfico de mapa de calor (Heatmap) cruzando e evidenciando a incidência peculiar de ataques para setores da economia.
4. **Tempo Médio de Resolução:** Mostra e compara as médias exigidas para contornar ameaças, dependendo dos mecanismos de defesa usados.
5. **Severidade por Tipo de Ataque:** Um comparativo minucioso de barras agrupadas para validar o grau de destrutividade na variação de classes de ataques.

---

## 🤝 Status do Projeto

O dashboard e os scripts associados alcançaram maturidade final e encontram-se integralmente consolidados em um protótipo final.

| Parte | Status |
|---|---|
| EDA + tratamento de dados | ✅ Concluído e Otimizado |
| Model (`ads_model.py`) | ✅ Concluído |
| Controller (`routes.py`) | ✅ Concluído |
| Interface (`dashboard.html`) | ✅ Concluído |
