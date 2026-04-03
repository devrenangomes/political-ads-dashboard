# 🛡️ Global Cybersecurity Threats Dashboard

Dashboard interativo de ameaças cibernéticas globais (2015–2024), construído com Flask e Plotly.

---

## 📚 Stack escolhida — e por quê

### 🐍 Python 3
Linguagem principal do projeto. É o padrão da indústria para análise de dados e desenvolvimento web com foco em dados.

### 🐼 Pandas
Biblioteca de manipulação de dados. Usada para carregar o CSV, limpar os dados e gerar os DataFrames prontos para cada gráfico.

```python
# Exemplo: carregar e filtrar dados
import pandas as pd
df = pd.read_csv('data/arquivo.csv')
df[df['country'] == 'Brazil']  # filtrar só Brasil
```

### 🌐 Flask
Framework web minimalista para Python. Responsável por:
- Servir as páginas HTML (rotas)
- Receber filtros do usuário (formulários/parâmetros)
- Chamar o model e passar dados para os templates

```python
# Exemplo de rota Flask
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('dashboard.html')
```

### 📊 Plotly
Biblioteca de visualizações **interativas**. Os gráficos gerados com Plotly permitem zoom, hover e filtros — diferente do Matplotlib que gera imagens estáticas.

```python
# Exemplo: criar um gráfico de barras interativo
import plotly.express as px
fig = px.bar(df, x='country', y='financial_loss')
fig.show()  # no notebook
# No Flask: fig.to_json() → envia para o HTML via JavaScript
```

---

## 🗂️ Estrutura do projeto (MVC)

```
political-ads-dashboard/
│
├── data/                          ← arquivos CSV brutos (não editar!)
│   └── Global_Cybersecurity_Threats_2015-2024.csv
│
├── app/
│   ├── __init__.py
│   ├── models/
│   │   └── ads_model.py           ← ⭐ MODEL: lógica de dados (sua parte)
│   ├── controllers/
│   │   └── dashboard_controller.py ← CONTROLLER: recebe requisições
│   └── templates/
│       └── dashboard.html          ← VIEW: HTML do dashboard
│
├── static/
│   └── js/                        ← arquivos JavaScript (se necessário)
│
├── notebooks/
│   └── eda_fase2.ipynb            ← análise exploratória (documentação)
│
├── run.py                         ← ponto de entrada da aplicação
├── requirements.txt               ← dependências do projeto
└── README.md                      ← você está aqui
```

### O que cada camada faz

| Camada | Arquivo | Responsabilidade |
|---|---|---|
| **Model** | `ads_model.py` | Carrega CSV, limpa dados, retorna DataFrames prontos |
| **Controller** | `dashboard_controller.py` | Recebe a requisição HTTP, chama o model, passa para a view |
| **View** | `dashboard.html` | Renderiza os dados como gráficos na página |

> **Regra de ouro:** o controller **nunca** manipula dados diretamente. O model **nunca** sabe que existe uma página HTML. Cada camada tem uma única responsabilidade.

---

## ⚙️ Como configurar o ambiente (setup inicial)

Faça isso **uma vez** ao clonar o projeto:

```bash
# 1. Criar o ambiente virtual
python3 -m venv .venv

# 2. Ativar o ambiente virtual
source .venv/bin/activate      # Mac/Linux
# .venv\Scripts\activate       # Windows

# 3. Instalar todas as dependências
pip install -r requirements.txt
```

✅ Quando o ambiente está ativo, o terminal mostra `(.venv)` no início da linha.

---

## ▶️ Como rodar o projeto

Com a venv **ativa**:

```bash
python run.py
```

Acesse no navegador: **http://localhost:5000**

---

## 🧩 Como usar o Model (para o time do dashboard)

O `ads_model.py` já entrega os dados prontos para cada gráfico. Você **não precisa** mexer nele — só importar e chamar.

### Passo 1 — Importar as funções

```python
from app.models.ads_model import (
    load_data,
    ataques_por_ano,
    prejuizo_por_pais,
    cross_ataque_industria,
    eficiencia_defesa,
    severidade_por_ataque
)
```

### Passo 2 — Carregar o DataFrame limpo

```python
df = load_data()
# O df já vem com:
# - colunas renomeadas para snake_case
# - tipos corretos (category, float, int)
# - colunas extras: 'severity' e 'response_speed'
```

### Passo 3 — Usar as funções de análise

Cada função recebe o `df` e retorna um DataFrame pronto para virar gráfico:

```python
# Gráfico 1 — Linha: ataques por ano
dados_ano = ataques_por_ano(df)
# Retorna: DataFrame com colunas ['year', 'total_ataques']

# Gráfico 2 — Barras: prejuízo por país
dados_pais = prejuizo_por_pais(df)
# Retorna: DataFrame com colunas ['country', 'media', 'total', 'qtd_ataques']

# Gráfico 3 — Heatmap: ataque × indústria
dados_cross = cross_ataque_industria(df)
# Retorna: tabela cruzada (6 linhas × 7 colunas)

# Gráfico 4 — Barras horizontais: eficiência de defesa
dados_defesa = eficiencia_defesa(df)
# Retorna: DataFrame com colunas ['defense_mechanism', 'media_horas']

# Gráfico 5 — Histograma: severidade por tipo de ataque
dados_sev = severidade_por_ataque(df)
# Retorna: DataFrame com colunas ['attack_type', 'severity', 'quantidade']
```

### Exemplo completo — Controller + Plotly

```python
# app/controllers/dashboard_controller.py

from flask import Blueprint, render_template
import plotly.express as px
import json
from app.models.ads_model import load_data, ataques_por_ano

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def index():
    df = load_data()

    # Gerar gráfico
    dados = ataques_por_ano(df)
    fig = px.line(dados, x='year', y='total_ataques',
                  title='Ataques por Ano')

    # Converter para JSON (será lido pelo JavaScript no HTML)
    grafico_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('dashboard.html', grafico=grafico_json)
```

```html
<!-- app/templates/dashboard.html -->
<!-- Renderizar o gráfico com Plotly.js -->
<div id="grafico1"></div>
<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
<script>
    var dados = {{ grafico | safe }};
    Plotly.newPlot('grafico1', dados.data, dados.layout);
</script>
```

---

## 📦 Dependências principais

| Biblioteca | Versão | Para que serve |
|---|---|---|
| Flask | 3.1.0 | Servidor web e roteamento |
| Pandas | 2.2.3 | Manipulação de dados |
| NumPy | 2.2.4 | Operações numéricas |
| Plotly | 6.6.0 | Gráficos interativos |
| Gunicorn | 23.0.0 | Servidor de produção |
| python-dotenv | 1.1.0 | Variáveis de ambiente |

Para instalar tudo de uma vez:
```bash
pip install -r requirements.txt
```

Para adicionar uma nova biblioteca:
```bash
pip install nome-da-biblioteca
pip freeze | grep nome-da-biblioteca >> requirements.txt
```

---

## 🌿 Boas práticas de Git para o time

```bash
# Sempre antes de começar a trabalhar:
git pull origin main

# Depois de fazer alterações:
git add arquivo_modificado.py
git commit -m "tipo: descrição curta do que foi feito"
git push origin main
```

**Tipos de commit:**
- `feat:` → nova funcionalidade
- `fix:` → correção de bug
- `docs:` → alteração em documentação
- `style:` → formatação sem mudar lógica

---

## 🤝 Divisão do projeto

| Parte | Responsável |
|---|---|
| EDA + tratamento de dados (`notebooks/`) | ✅ Concluído |
| Model (`app/models/ads_model.py`) | ✅ Concluído |
| Controller (`app/controllers/`) | 🔨 Time do dashboard |
| Templates HTML (`app/templates/`) | 🔨 Time do dashboard |
| Estilização CSS (`static/`) | 🔨 Time do dashboard |
