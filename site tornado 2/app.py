"""Site de tornados: Python (Flask) gera o HTML, sem JavaScript.

Rodar:  python app.py  (abre sozinho em http://127.0.0.1:5000)
"""
import os
import threading
import webbrowser

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# deaths = mortes | width = largura máxima (km)
# damage = prejuízo (milhões de US$, aprox.)
TORNADOS = [
    {
        "name": "Daulatpur–Saturia",
        "year": 1989,
        "country": "Mundo",
        "place": "Bangladesh",
        "rating": "Estimado F4",
        "deaths": 1300,
        "note": (
            "O tornado mais mortal da história, com cerca de 80 mil "
            "desabrigados."
        ),
    },
    {
        "name": "Manikganj",
        "year": 1996,
        "country": "Mundo",
        "place": "Bangladesh",
        "rating": "Estimado F4",
        "deaths": 700,
        "note": (
            "Um dos mais letais já registrados, em região densamente "
            "povoada."
        ),
    },
    {
        "name": "Tri-State",
        "year": 1925,
        "country": "EUA",
        "place": "Missouri, Illinois e Indiana",
        "rating": "F5 (estimado)",
        "deaths": 695,
        "width": 1.2,
        "damage": 1400,
        "note": (
            "O mais mortal dos EUA e o de maior trajetória (cerca de 352 km). "
            "Prejuízo em valores atuais aproximados."
        ),
    },
    {
        "name": "Joplin",
        "year": 2011,
        "country": "EUA",
        "place": "Missouri",
        "rating": "EF5",
        "deaths": 158,
        "width": 1.6,
        "damage": 2800,
        "note": (
            "O mais mortal dos EUA desde que há registros modernos (1950)."
        ),
    },
    {
        "name": "Moore",
        "year": 2013,
        "country": "EUA",
        "place": "Oklahoma",
        "rating": "EF5",
        "deaths": 24,
        "width": 2.1,
        "damage": 2000,
        "note": (
            "Atingiu escolas e causou prejuízos de cerca de US$ 2 bilhões."
        ),
    },
    {
        "name": "Bridge Creek–Moore",
        "year": 1999,
        "country": "EUA",
        "place": "Oklahoma",
        "rating": "F5",
        "deaths": 36,
        "damage": 1000,
        "note": "Registrou o vento mais forte já medido: cerca de 484 km/h.",
    },
    {
        "name": "El Reno",
        "year": 2013,
        "country": "EUA",
        "place": "Oklahoma",
        "rating": "EF3",
        "deaths": 8,
        "width": 4.2,
        "note": (
            "O mais largo já registrado, com 4,2 km. Matou 8 pessoas, "
            "incluindo o pesquisador Tim Samaras."
        ),
    },
    {
        "name": "Hallam",
        "year": 2004,
        "country": "EUA",
        "place": "Nebraska",
        "rating": "F4",
        "deaths": 1,
        "width": 4.0,
        "note": "Segundo mais largo da história, com cerca de 4 km.",
    },
    {
        "name": "Greensburg",
        "year": 2007,
        "country": "EUA",
        "place": "Kansas",
        "rating": "EF5",
        "deaths": 11,
        "width": 2.7,
        "note": "Destruiu cerca de 95% da cidade.",
    },
    {
        "name": "Rio Bonito do Iguaçu",
        "year": 2025,
        "country": "Brasil",
        "place": "Paraná",
        "rating": "Ventos até 250 km/h",
        "deaths": 6,
        "note": "Cerca de 750 feridos e cerca de 90% da cidade destruída.",
    },
    {
        "name": "Xanxerê",
        "year": 2015,
        "country": "Brasil",
        "place": "Santa Catarina",
        "rating": "F2 (alto)",
        "deaths": 3,
        "damage": 34,
        "note": (
            "Mais de R$ 104 milhões em prejuízos (cerca de US$ 34 milhões "
            "na época). Mortes: 2 a 3, conforme a fonte."
        ),
    },
    {
        "name": "Itu",
        "year": 1991,
        "country": "Brasil",
        "place": "São Paulo",
        "rating": "—",
        "deaths": 15,
        "note": (
            "Número de mortes segundo matérias baseadas em dados do Cemaden."
        ),
    },
]

BRASIL = [
    {
        "when": "7 de novembro de 2025 · Paraná",
        "title": "Rio Bonito do Iguaçu",
        "text": (
            "Considerado um dos maiores já registrados no país. Ventos de até "
            "250 km/h destruíram cerca de 90% da cidade. Foram 6 mortes e "
            "cerca de 750 feridos."
        ),
    },
    {
        "when": "20 de abril de 2015 · Santa Catarina",
        "title": "Xanxerê",
        "text": (
            "Classificado como F2 de alta intensidade em estudos acadêmicos. "
            "De 2 a 3 mortes (conforme a fonte), de 97 a 120 feridos e mais "
            "de R$ 104 milhões em prejuízos."
        ),
    },
    {
        "when": "1991 · São Paulo",
        "title": "Itu",
        "text": (
            "Um dos tornados mais letais do país: segundo matérias baseadas "
            "em dados do Cemaden, matou 15 pessoas."
        ),
    },
]

FUJITA = [
    {
        "level": "EF0",
        "wind": "105–137 km/h",
        "damage": "Danos leves: telhas soltas, galhos quebrados",
    },
    {
        "level": "EF1",
        "wind": "138–177 km/h",
        "damage": "Danos moderados: telhados arrancados, carros movidos",
    },
    {
        "level": "EF2",
        "wind": "178–217 km/h",
        "damage": (
            "Danos consideráveis: casas destelhadas, árvores arrancadas"
        ),
    },
    {
        "level": "EF3",
        "wind": "218–266 km/h",
        "damage": "Danos severos: paredes derrubadas, trens tombados",
    },
    {
        "level": "EF4",
        "wind": "267–322 km/h",
        "damage": "Danos devastadores: casas bem construídas niveladas",
    },
    {
        "level": "EF5",
        "wind": "mais de 322 km/h",
        "damage": "Danos incríveis: estruturas varridas das fundações",
    },
]

METRICAS = {
    "deaths": "Mortes",
    "width": "Largura",
    "damage": "Prejuízo",
}
PAISES = ["Todos", "EUA", "Brasil", "Mundo"]
URL = "http://127.0.0.1:5000"


def calcular_ranking(metric, country):
    """Devolve os tornados ordenados pelo critério e filtrados por país."""
    rows = [
        tornado
        for tornado in TORNADOS
        if tornado.get(metric) is not None
        and (country == "Todos" or tornado["country"] == country)
    ]
    rows.sort(key=lambda t: t[metric], reverse=True)
    return rows


def formatar(metric, valor):
    """Formata o número no padrão brasileiro (1.300 / 4,2)."""
    if metric == "width":
        texto = f"{valor:.1f}".replace(".", ",")
    else:
        texto = f"{int(valor):,}".replace(",", ".")
    if metric == "deaths":
        return f"{texto} mortes"
    if metric == "width":
        return f"{texto} km"
    return f"US$ {texto} mi"


@app.route("/")
def home():
    metric = request.args.get("metric", "deaths")
    country = request.args.get("country", "Todos")
    if metric not in METRICAS:
        metric = "deaths"
    if country not in PAISES:
        country = "Todos"

    rows = calcular_ranking(metric, country)
    maximo = rows[0][metric] if rows else 1
    ranking_itens = [
        {
            **t,
            "valor": formatar(metric, t[metric]),
            "pct": round(t[metric] / maximo * 100),
        }
        for t in rows
    ]
    return render_template(
        "index.html",
        brasil=BRASIL,
        fujita=FUJITA,
        ranking=ranking_itens,
        metricas=METRICAS,
        paises=PAISES,
        metric=metric,
        country=country,
    )


@app.route("/api/ranking")
def api_ranking():
    """Ex.: /api/ranking?metric=deaths&country=Brasil"""
    metric = request.args.get("metric", "deaths")
    country = request.args.get("country", "Todos")
    if metric not in METRICAS or country not in PAISES:
        return jsonify({"error": "metric ou country inválido"}), 400

    rows = calcular_ranking(metric, country)
    return jsonify(
        {
            "metric": metric,
            "country": country,
            "rows": rows,
            "max": rows[0][metric] if rows else 0,
        }
    )


def abrir_navegador():
    """Abre o site no Opera (ou no navegador padrão, se não achar)."""
    candidatos = [
        r"%LOCALAPPDATA%\Programs\Opera GX\opera.exe",
        r"%LOCALAPPDATA%\Programs\Opera\opera.exe",
        r"%PROGRAMFILES%\Opera GX\opera.exe",
        r"%PROGRAMFILES%\Opera\opera.exe",
    ]
    for candidato in candidatos:
        caminho = os.path.expandvars(candidato)
        if os.path.exists(caminho):
            webbrowser.register(
                "opera", None, webbrowser.BackgroundBrowser(caminho)
            )
            webbrowser.get("opera").open(URL)
            return
    webbrowser.open(URL)


if __name__ == "__main__":
    # O reloader do debug roda o arquivo duas vezes; abre só na primeira.
    if os.environ.get("WERKZEUG_RUN_MAIN") != "true":
        threading.Timer(1.0, abrir_navegador).start()
    app.run(debug=True)
