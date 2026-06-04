import os, datetime, requests
from pathlib import Path

SERPAPI_KEY = os.environ.get("SERPAPI_KEY", "")

QUERIES = [
    {"categoria": "Monitoreo y Teleasistencia", "query": "servicio monitoreo alarmas Argentina 2026 central monitoreo"},
    {"categoria": "Alarmas Residenciales y Comerciales", "query": "alarmas residenciales comerciales Argentina 2026 instalacion"},
    {"categoria": "Camaras y Videovigilancia", "query": "camaras seguridad CCTV videovigilancia Argentina 2026"},
    {"categoria": "Mercado y Metricas del Sector", "query": "mercado seguridad electronica Argentina estadisticas crecimiento 2026"},
    {"categoria": "Tecnologia e Innovacion", "query": "tecnologia alarmas monitoreo inteligente IoT Argentina 2026"},
    {"categoria": "Noticias Internacionales del Sector", "query": "security monitoring industry news market 2026 latin america"}
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
            fuente = item.get("source", {})
            if isinstance(fuente, dict):
                fuente = fuente.get("name", "")
            items.append({"titulo": titulo, "snippet": snippet, "link": link, "fecha": fecha, "fuente": fuente})
        return items
    except:
        return []

def generar():
    fecha = datetime.datetime.now().strftime("%d/%m/%Y")
    hora = datetime.datetime.now().strftime("%H:%M")

    tarjetas_html = ""
    for item in QUERIES:
        noticias = buscar(item["query"])
        tarjetas_html += f"""
        <div class="seccion">
          <div class="seccion-header">
            <span class="seccion-icon">●</span>
            <h2>{item['categoria']}</h2>
          </div>
          <div class="grid">
        """
        if noticias:
            for n in noticias:
                tarjetas_html += f"""
            <a href="{n['link']}" target="_blank" class="card">
              <div class="card-meta">
                <span class="fuente">{n['fuente']}</span>
                <span class="fecha-card">{n['fecha']}</span>
              </div>
              <h3>{n['titulo']}</h3>
              <p>{n['snippet']}</p>
              <span class="leer-mas">Leer nota →</span>
            </a>
                """
        else:
            tarjetas_html += "<p class='sin-datos'>Sin noticias disponibles en este momento.</p>"
        tarjetas_html += "</div></div>"

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Security Intelligence — X-28</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

  * {{ box-sizing: border-box; margin: 0; padding: 0; }}

  body {{
    font-family: 'Inter', sans-serif;
    background: #f4f6f9;
    color: #1a1a2e;
  }}

  /* HEADER */
  .header {{
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 60%, #0f3460 100%);
    padding: 48px 40px 40px;
    text-align: center;
  }}
  .header-badge {{
    display: inline-block;
    background: rgba(255,255,255,0.1);
    color: #e94560;
    border: 1px solid rgba(233,69,96,0.3);
    padding: 4px 14px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 16px;
  }}
  .header h1 {{
    color: white;
    font-size: 32px;
    font-weight: 700;
    letter-spacing: -0.5px;
    margin-bottom: 8px;
  }}
  .header h1 span {{ color: #e94560; }}
  .header-sub {{
    color: rgba(255,255,255,0.5);
    font-size: 13px;
    font-weight: 300;
  }}
  .header-date {{
    margin-top: 20px;
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.1);
    padding: 8px 20px;
    border-radius: 30px;
    color: rgba(255,255,255,0.7);
    font-size: 12px;
  }}
  .dot-live {{
    width: 7px; height: 7px;
    background: #2ecc71;
    border-radius: 50%;
    animation: pulse 2s infinite;
  }}
  @keyframes pulse {{
    0%, 100% {{ opacity: 1; }}
    50% {{ opacity: 0.3; }}
  }}

  /* CONTENIDO */
  .container {{
    max-width: 1200px;
    margin: 0 auto;
    padding: 40px 24px;
  }}

  .seccion {{
    margin-bottom: 48px;
  }}
  .seccion-header {{
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 20px;
    padding-bottom: 12px;
    border-bottom: 2px solid #e94560;
  }}
  .seccion-icon {{
    color: #e94560;
    font-size: 10px;
  }}
  .seccion-header h2 {{
    font-size: 16px;
    font-weight: 600;
    color: #1a1a2e;
    text-transform: uppercase;
    letter-spacing: 1px;
  }}

  .grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(270px, 1fr));
    gap: 20px;
  }}

  .card {{
    background: white;
    border-radius: 12px;
    padding: 20px;
    text-decoration: none;
    color: inherit;
    display: flex;
    flex-direction: column;
    gap: 10px;
    border: 1px solid #eaecf0;
    transition: all 0.2s ease;
    position: relative;
    overflow: hidden;
  }}
  .card::before {{
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 100%;
    background: #e94560;
    opacity: 0;
    transition: opacity 0.2s;
  }}
  .card:hover {{
    box-shadow: 0 8px 24px rgba(0,0,0,0.08);
    transform: translateY(-2px);
    border-color: #e94560;
  }}
  .card:hover::before {{ opacity: 1; }}

  .card-meta {{
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}
  .fuente {{
    font-size: 10px;
    font-weight: 600;
    color: #e94560;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }}
  .fecha-card {{
    font-size: 10px;
    color: #aaa;
  }}
  .card h3 {{
    font-size: 14px;
    font-weight: 600;
    color: #1a1a2e;
    line-height: 1.5;
  }}
  .card p {{
    font-size: 12px;
    color: #666;
    line-height: 1.6;
    flex-grow: 1;
  }}
  .leer-mas {{
    font-size: 11px;
    font-weight: 600;
    color: #e94560;
    margin-top: 4px;
  }}

  .sin-datos {{
    color: #bbb;
    font-style: italic;
    font-size: 13px;
    padding: 20px 0;
  }}

  /* FOOTER */
  footer {{
    background: #1a1a2e;
    color: rgba(255,255,255,0.3);
    text-align: center;
    padding: 24px;
    font-size: 11px;
    letter-spacing: 0.5px;
  }}
  footer span {{ color: #e94560; }}
</style>
</head>
<body>

<div class="header">
  <div class="header-badge">Security Intelligence</div>
  <h1>Radar de <span>Seguridad Electrónica</span></h1>
  <p class="header-sub">Monitoreo · Alarmas · Cámaras · Mercado · Tecnología</p>
  <div class="header-date">
    <div class="dot-live"></div>
    Actualizado el {fecha} a las {hora} hs
  </div>
</div>

<div class="container">
  {tarjetas_html}
</div>

<footer>
  Actualizado automáticamente todos los días · <span>Security Intelligence Dashboard</span>
</footer>

</body>
</html>"""

    Path("docs").mkdir(exist_ok=True)
    with open("docs/index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Pagina generada OK")

if __name__ == "__main__":
    generar()
    
