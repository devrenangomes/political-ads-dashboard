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


