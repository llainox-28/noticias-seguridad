import os, datetime, requests
from pathlib import Path

SERPAPI_KEY = os.environ.get("SERPAPI_KEY", "")

QUERIES = [
    "seguridad electronica Argentina noticias 2025",
    "alarmas hogares Argentina novedades 2025",
    "seguridad privada Argentina tecnologia 2025",
    "CCTV camaras seguridad Argentina 2025",
    "seguridad electronica mundo noticias 2025",
    "smart home seguridad tecnologia 2025"
]

def buscar(query):
    try:
        r = requests.get("https://serpapi.com/search", params={
            "api_key": SERPAPI_KEY,
            "q": query,
            "gl": "ar",
            "hl": "es",
            "num": 4,
            "tbm": "nws"
        }, timeout=15)
        data = r.json()
        items = []
        for item in data.get("news_results", data.get("organic_results", []))[:4]:
            titulo = item.get("title", "")
            snippet = item.get("snippet", item.get("description", ""))
            link = item.get("link", item.get("url", "#"))
            fecha = item.get("date", "")
            items.append({"titulo": titulo, "snippet": snippet, "link": link, "fecha": fecha})
        return items
    except:
        return []

def generar():
    fecha = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    tarjetas = ""
    categorias = [
        "Seguridad Electronica Argentina",
        "Alarmas y Hogares Argentina",
        "Seguridad Privada Argentina",
        "CCTV y Camaras Argentina",
        "Seguridad Electronica Mundial",
        "Smart Home y Tecnologia"
    ]
    for i, query in enumerate(QUERIES):
        noticias = buscar(query)
        tarjetas += f"<div class='categoria'><h2>{categorias[i]}</h2><div class='grid'>"
        if noticias:
            for n in noticias:
                tarjetas += f"""<a href='{n['link']}' target='_blank' class='tarjeta'>
                <div class='fecha'>{n['fecha']}</div>
                <h3>{n['titulo']}</h3>
                <p>{n['snippet']}</p>
                </a>"""
        else:
            tarjetas += "<p class='sin-datos'>Sin noticias disponibles</p>"
        tarjetas += "</div></div>"

    html = """<!DOCTYPE html>
<html lang='es'>
<head>
<meta charset='UTF-8'>
<meta name='viewport' content='width=device-width, initial-scale=1'>
<title>Noticias Seguridad Electronica</title>
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: Arial, sans-serif; background: #f0f2f5; color: #333; }
header { background: #1a1a2e; color: white; padding: 20px 40px; }
header h1 { font-size: 24px; }
header p { color: #aaa; font-size: 14px; margin-top: 5px; }
.container { max-width: 1200px; margin: 0 auto; padding: 30px 20px; }
.categoria { margin-bottom: 40px; }
.categoria h2 { color: #1a1a2e; border-left: 4px solid #e74c3c; padding-left: 12px; margin-bottom: 16px; font-size: 18px; }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 16px; }
.tarjeta { background: white; border-radius: 8px; padding: 16px; text-decoration: none; color: inherit; display: block; border: 1px solid #e0e0e0; transition: box-shadow 0.2s; }
.tarjeta:hover { box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
.tarjeta h3 { font-size: 15px; color: #1a1a2e; margin: 8px 0; line-height: 1.4; }
.tarjeta p { font-size: 13px; color: #666; line-height: 1.5; }
.fecha { font-size: 11px; color: #e74c3c; font-weight: bold; }
.sin-datos { color: #999; font-style: italic; }
footer { text-align: center; padding: 20px; color: #999; font-size: 12px; }
</style>
</head>
<body>
<header>
<h1>Noticias de Seguridad Electronica</h1>
<p>Actualizado: """ + fecha + """</p>
</header>
<div class='container'>
""" + tarjetas + """
</div>
<footer>Actualizado automaticamente todos los dias</footer>
</body></html>"""

    Path("docs").mkdir(exist_ok=True)
    with open("docs/index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Pagina generada correctamente")

if __name__ == "__main__":
    generar()
