#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador del sitio de producción de Tu Asesoría Inmobiliaria (TuAI).

Por qué existe este script (y no un sitio armado a mano):
- El header, footer, nav y botón flotante de WhatsApp viven UNA sola vez acá.
  Si hay que cambiar el logo, un teléfono o un link, se cambia en un solo
  lugar y se vuelve a correr el script — no hay que tocar 8 archivos HTML.
- Cada propiedad es un bloque de datos independiente en PROPERTIES: agregar,
  quitar o reordenar una propiedad es editar esa lista, nada más (coincide
  con el requisito original de "cada propiedad como módulo independiente").
- La salida son archivos .html planos (sin build step, sin Jekyll/Ruby):
  se suben tal cual a GitHub Pages y funcionan.

Uso:
    python3 build_site.py
Genera (o regenera) todo dentro de tuai-site/.
"""
import os
import re
import urllib.parse

ROOT = os.path.dirname(os.path.abspath(__file__))
PROP_DIR = "propiedades"
WA_PHONE = "56998383991"
EMAIL_DESTINO = "tuasesoriainmobiliariacl@gmail.com"

# ======================================================================
# 1) CATÁLOGO DE PROPIEDADES — orden de publicación acordado con el cliente
# ======================================================================
PROPERTIES = [
    dict(id="p1", slug="casa-tunquen", titulo="Casa en venta — Tunquén",
         comuna="Tunquén", tipo="Venta", tipo_key="venta", tag_class="tag-venta", emoji="🏠"),
    dict(id="p2", slug="depto-san-miguel", titulo="Departamento en venta — San Miguel",
         comuna="San Miguel, Santiago", tipo="Venta", tipo_key="venta", tag_class="tag-venta", emoji="🏢"),
    dict(id="p3", slug="depto-san-bernardo", titulo="Departamento en venta — San Bernardo",
         comuna="San Bernardo, Santiago", tipo="Venta", tipo_key="venta", tag_class="tag-venta", emoji="🏢"),
    dict(id="p4", slug="depto-pucon", titulo="Departamento en venta — Pucón",
         comuna="Pucón", tipo="Venta", tipo_key="venta", tag_class="tag-venta", emoji="🏢"),
    dict(id="p5", slug="estacionamiento-santiago-centro", titulo="Estacionamiento en venta — Santiago Centro",
         comuna="Santiago Centro", tipo="Venta", tipo_key="venta", tag_class="tag-venta", emoji="🚗"),
    dict(id="p6", slug="bodega-tocornal", titulo="Bodega comercial — Tocornal",
         comuna="Tocornal", tipo="Venta", tipo_key="venta", tag_class="tag-venta", emoji="🏭"),
    dict(id="p7", slug="terreno-metro-nuble", titulo="Terreno comercial — Metro Ñuble",
         comuna="Metro Ñuble, Santiago", tipo="Venta", tipo_key="venta", tag_class="tag-venta", emoji="📐"),
]

# Campos pendientes de carga real — nunca se inventan, van en placeholder
# hasta que lleguen los datos reales de cada propiedad.
for p in PROPERTIES:
    p["fotos"] = [None] * 6
    p["specs_text"] = "Detalles y superficie por confirmar"
    p["precio"] = "Precio por confirmar"
    p["uf_precio"] = "UF —"
    p["clp_precio"] = "$ — CLP aprox."
    p["dormitorios"] = "—"
    p["banos"] = "—"
    p["superficie_util"] = "—"
    p["superficie_total"] = "—"
    p["estacionamientos"] = "—"
    p["bodega"] = "—"
    p["resumen"] = "Resumen de la propiedad pendiente de carga."
    p["video_youtube"] = None   # link de YouTube real -> activa el botón "Ver en YouTube"
    p["plano_img"] = None       # ruta a la imagen del plano (se sube por propiedad)
    p["mapa_img"] = None        # ruta a la imagen del mapa (se sube por propiedad)
    p["pie"] = "—"
    p["monto_financiar"] = "—"
    p["dividendo_estimado"] = "—"
    p["wa_link"] = "https://wa.me/%s?text=%s" % (
        WA_PHONE, urllib.parse.quote(f"Hola, quiero coordinar una visita para: {p['titulo']} ({p['comuna']})."))
    p["wa_info_link"] = "https://wa.me/%s?text=%s" % (
        WA_PHONE, urllib.parse.quote(f"Hola, quisiera más información sobre: {p['titulo']} ({p['comuna']})."))

PROPERTIES_BY_ID = {p["id"]: p for p in PROPERTIES}

# ----------------------------------------------------------------------
# Datos reales ya recibidos del cliente (se van completando propiedad
# por propiedad; todo lo que no esté acá sigue en placeholder).
# ----------------------------------------------------------------------
_TUNQUEN_FOTO_DIR = "/assets/propiedades/casa-tunquen"
# Portada confirmada por el cliente: "tunquen-portada.jpg" (su archivo
# "6459_corregida", reenviado directamente ya que el nombre original se
# pierde al subir fotos al chat).
#
# Recorrido pedido por el cliente: portada -> living/comedor -> dormitorios
# 1er piso -> dormitorios 2do piso (+ escaleras, estudio y pasillo) ->
# cocina -> exteriores.
_TUNQUEN_FOTOS = [
    # Living / comedor (primer nivel)
    2, 5, 1, 4, 3, 10, 9, 8,
    # Dormitorios 1er piso (+ baño de visitas)
    25, 20, 17,
    # Dormitorios 2do piso + escaleras + estudio + pasillo
    15, 19, 14, 22, 21, 16, 18, 26, 12,
    # Cocina
    6, 7,
    # Exteriores
    30, 31, 11, 13, 27, 28, 29, 23, 24,
]
PROPERTIES_BY_ID["p1"].update(dict(
    fotos=[f"{_TUNQUEN_FOTO_DIR}/tunquen-portada.jpg"] +
          [f"{_TUNQUEN_FOTO_DIR}/tunquen-{n:02d}.jpg" for n in _TUNQUEN_FOTOS],
    video_youtube="https://www.youtube.com/watch?v=GagnKvKlRk8",
    dormitorios="3 + 1 serv.",
    banos="3 + 1 serv.",
    superficie_util="210 m²",
    superficie_total="5.000 m²",
    estacionamientos="8",
    bodega="1",
    uf_precio="UF 11.599",
    clp_precio="$ 477.815.585 CLP aprox.",
    precio="UF 11.599",
    specs_text="3D + serv. / 3B + serv. · 210 m² útiles · 5.000 m² de terreno",
    mapa_img=f"{_TUNQUEN_FOTO_DIR}/tunquen-mapa.jpg",
    resumen=(
        "<strong>Casa en Tunquén — donde el mar y el bosque se encuentran.</strong><br><br>"
        "Imagina despertar con la brisa marina entrando por la ventana y el verde infinito "
        "del campo como vecino. Esta casa en Tunquén no es solo una propiedad: es una "
        "invitación a vivir distinto, en un condominio que fusiona la calma de la vida "
        "campestre con la energía del océano.<br><br>"
        "<strong>Primer nivel</strong><br>"
        "Un living-comedor de techos con viga a la vista recibe la luz natural a raudales, "
        "mientras los pisos en desnivel juegan sutilmente con los espacios, dándole "
        "personalidad a cada rincón. La chimenea es el corazón del hogar: calidez que se "
        "abre directo a una amplia terraza, ideal para esos atardeceres que no querrás "
        "terminar.<br><br>"
        "La cocina, amplia y funcional, se complementa con una práctica loggia. Hay un "
        "dormitorio de servicio completo, y para quienes trabajan desde casa, un home "
        "office luminoso y espacioso que hace del teletrabajo un placer. Dos dormitorios "
        "—uno en suite— se abren a la terraza con vista al entorno natural, además de un "
        "completo baño de visitas para recibir sin preocupaciones.<br><br>"
        "Afuera, el jardín invita a quedarse: piscina, extensas áreas verdes, juegos "
        "infantiles, un generoso quincho para los asados de fin de semana y amplio "
        "estacionamiento.<br><br>"
        "<strong>Segundo nivel</strong><br>"
        "El dormitorio principal es una suite con walk-in closet y salida a una terraza "
        "con vista privilegiada a la bahía. Una escalera de estilo mediterráneo baja hasta "
        "los jardines, conectando cada nivel con la naturaleza que rodea la casa.<br><br>"
        "Tunquén — vive la costa como siempre la imaginaste."
    ),
))

# Fotos para la rotación del hero de la portada (índice sobre tunquen-NN.jpg),
# elegidas por ser las más vistosas del lote: piscina, dos jardines en flor,
# vista al mar y la fachada.
HOME_HERO_PHOTOS = [f"{_TUNQUEN_FOTO_DIR}/tunquen-{n:02d}.jpg" for n in (30, 11, 13, 24, 27)]

# ======================================================================
# 2) ESTILOS COMPARTIDOS (un solo archivo, assets/styles.css)
# ======================================================================
STYLE_CSS = """
:root{
  --accent:#E8440A;
  --gray-900:#333333;
  --gray-700:#555555;
  --gray-500:#767676;
  --gray-300:#DEDBD8;
  --gray-200:#F4F3F1;
  --gray-100:#FAFAF9;
  --gray-footer-text:#969696;
  --white:#FFFFFF;
  --radius:10px;
  --maxw:1180px;
  --font: -apple-system, 'Helvetica Neue', Helvetica, Arial, sans-serif;
}
*{box-sizing:border-box}
body{margin:0;font-family:var(--font);color:var(--gray-900);background:var(--white);-webkit-font-smoothing:antialiased}
h1,h2,h3,p,ul{margin:0}
ul{padding:0;list-style:none}
a{color:var(--accent);text-decoration:none}
a:hover{text-decoration:underline}
button{font-family:var(--font);cursor:pointer}
img,svg{display:block}
.wrap{max-width:var(--maxw);margin:0 auto;padding-inline:24px}
.eyebrow{font-size:13px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--accent)}
.section-title{font-size:clamp(26px,3.6vw,36px);font-weight:700;color:var(--gray-900);line-height:1.15}
.section-sub{font-size:16px;color:var(--gray-700);line-height:1.6;max-width:640px}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;font-size:15px;font-weight:700;padding:14px 26px;border-radius:999px;border:2px solid transparent;transition:transform .15s ease, opacity .15s ease;white-space:nowrap;cursor:pointer}
.btn:hover{text-decoration:none;transform:translateY(-1px)}
.btn-primary{background:var(--accent);color:#fff}
.btn-primary:hover{opacity:.92}
.btn-outline{background:transparent;border-color:var(--gray-500);color:var(--gray-900)}
.btn-outline:hover{border-color:var(--gray-900)}
.btn-sm{padding:10px 18px;font-size:14px;border-radius:999px}
.card{background:var(--white);border:1px solid var(--gray-300);border-radius:var(--radius)}
.tag{display:inline-flex;align-items:center;font-size:12px;font-weight:700;letter-spacing:.03em;text-transform:uppercase;padding:5px 12px;border-radius:999px}
.tag-venta{background:#FCE8DF;color:#9A3207}
.tag-arriendo{background:var(--gray-200);color:var(--gray-700)}
.tag-pendiente{background:var(--gray-200);color:var(--gray-500)}
.icon-badge{width:46px;height:46px;border-radius:12px;background:var(--gray-200);display:flex;align-items:center;justify-content:center;flex:none}
.ph-image{background:linear-gradient(135deg,#ECEAE8,#D8D5D1);display:flex;align-items:center;justify-content:center;color:var(--gray-500)}
.nav-link{font-size:15px;font-weight:500;color:var(--gray-900);background:none;border:none;font:inherit;cursor:pointer}
.nav-link:hover{color:var(--accent);text-decoration:none}
.filter-pill{border:1.5px solid var(--gray-300);background:var(--white);color:var(--gray-700);font-size:14px;font-weight:600;padding:9px 18px;border-radius:999px}
.filter-pill[aria-pressed="true"]{background:var(--gray-900);border-color:var(--gray-900);color:#fff}
.form-field{display:flex;flex-direction:column;gap:6px}
.form-field label{font-size:13px;font-weight:700;color:var(--gray-900)}
.form-field input,.form-field select,.form-field textarea{font-family:var(--font);font-size:15px;color:var(--gray-900);border:1.5px solid var(--gray-300);border-radius:8px;padding:12px 14px;background:#fff}
.form-field input:focus,.form-field select:focus,.form-field textarea:focus{outline:2px solid var(--accent);outline-offset:1px;border-color:var(--accent)}
.footer-link{color:var(--gray-300);font-size:14px}
.footer-link:hover{color:#fff}
.social-btn{width:40px;height:40px;border-radius:999px;background:#454442;display:flex;align-items:center;justify-content:center;flex:none}
.social-btn:hover{background:var(--accent)}
@keyframes fadeUp{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}
.enter{animation:fadeUp .5s ease both}
.hidden{display:none !important}
.icon-accent svg path, .icon-accent svg rect, .icon-accent svg circle{stroke:var(--accent)}
"""

# ======================================================================
# 3) ÍCONOS SVG COMPARTIDOS (placeholders honestos — nunca fotos inventadas)
# ======================================================================
PLACEHOLDER_ICON = """<svg width="46" height="46" viewBox="0 0 24 24" fill="none" aria-hidden="true">
    <path d="M3 10.5 12 3l9 7.5" stroke="var(--gray-500)" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M5 9.5V20a1 1 0 0 0 1 1h4v-6h4v6h4a1 1 0 0 0 1-1V9.5" stroke="var(--gray-500)" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
  </svg>"""
EXTRA_PHOTO_ICON = """<svg width="16" height="16" viewBox="0 0 24 24" fill="none" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2" stroke="var(--gray-500)" stroke-width="1.6"/><circle cx="9" cy="10" r="1.6" fill="var(--gray-500)"/><path d="m5 17 4.5-5 3 3.2L16 11l3 6" stroke="var(--gray-500)" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>"""
PLANO_PLACEHOLDER_ICON = """<svg width="44" height="44" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M4 4h9v6h7v10H4V4Z" stroke="var(--gray-500)" stroke-width="1.6" stroke-linejoin="round"/><path d="M9 20v-5h4v5" stroke="var(--gray-500)" stroke-width="1.6" stroke-linejoin="round"/></svg>"""
MAPA_PLACEHOLDER_ICON = """<svg width="40" height="40" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M12 21s7-6.1 7-11.2A7 7 0 0 0 5 9.8C5 14.9 12 21 12 21Z" stroke="var(--gray-500)" stroke-width="1.6" stroke-linejoin="round"/><circle cx="12" cy="9.5" r="2.4" stroke="var(--gray-500)" stroke-width="1.6"/></svg>"""
WA_ICON_WHITE = """<svg width="18" height="18" viewBox="0 0 24 24" fill="#fff" aria-hidden="true"><path d="M12 2C6.48 2 2 6.48 2 12c0 1.85.5 3.58 1.38 5.07L2 22l5.09-1.36A9.93 9.93 0 0 0 12 22c5.52 0 10-4.48 10-10S17.52 2 12 2Zm5.17 14.17c-.22.62-1.29 1.22-1.77 1.29-.46.07-.9.26-3.03-.63-2.56-1.06-4.21-3.65-4.34-3.82-.13-.17-1.04-1.38-1.04-2.63 0-1.25.65-1.86.89-2.12.22-.24.49-.3.65-.3h.47c.15 0 .35-.03.54.41.22.5.74 1.8.8 1.93.07.13.11.28.02.45-.49.98-1.02 1.02-.73 1.52.95 1.65 1.91 2.22 3.4 2.94.25.12.4.1.55-.05.18-.18.75-.87.95-1.17.2-.3.4-.25.68-.15.28.1 1.78.84 2.08 1 .3.15.5.23.57.36.08.13.08.75-.15 1.37Z"/></svg>"""
WA_ICON_GREEN = WA_ICON_WHITE.replace('fill="#fff"', 'fill="#25D366"')

# ======================================================================
# 4) BLOQUES COMPARTIDOS: <head>, header, footer, WhatsApp flotante
#    (reciben "prefix": "" si el archivo vive en la raíz, "../" si vive
#    dentro de propiedades/, para que los links y los assets apunten bien)
# ======================================================================
def anchor_href(prefix, anchor):
    return (prefix + "index.html#" + anchor) if prefix else ("#" + anchor)

def home_href(prefix):
    return (prefix + "index.html") if prefix else "#inicio"

def head_html(title, description, prefix):
    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{description}">
<title>{title}</title>
<link rel="stylesheet" href="{prefix}assets/styles.css">
</head>
<body>
<div style="min-height:100%;display:flex;flex-direction:column">
"""

def properties_menu_items_html(prefix):
    items = []
    for p in PROPERTIES:
        href = f"{prefix}{PROP_DIR}/{p['slug']}.html"
        items.append(
            f'<a role="menuitem" href="{href}" '
            f'style="display:flex;align-items:center;gap:10px;padding:9px 10px;border-radius:8px;'
            f'font-size:14px;color:var(--gray-900);text-decoration:none">'
            f'<span style="font-size:16px">{p["emoji"]}</span><span>{p["titulo"]}</span></a>'
        )
    ver_destacadas = (
        f'<div style="border-top:1px solid var(--gray-300);margin-top:6px;padding-top:8px">'
        f'<a href="{anchor_href(prefix, "propiedades")}" style="font-size:13px;font-weight:700">'
        f'Ver destacadas en la portada →</a></div>'
    )
    return "\n".join(items) + "\n" + ver_destacadas

def header_html(prefix):
    menu_items = properties_menu_items_html(prefix)
    return f"""  <!-- ===================== HEADER ===================== -->
  <header style="position:sticky;top:0;z-index:40;background:rgba(255,255,255,.96);backdrop-filter:blur(6px);border-bottom:1px solid var(--gray-300)">
    <div class="wrap" style="display:flex;align-items:center;justify-content:space-between;height:76px;gap:20px">

      <a href="{home_href(prefix)}" aria-label="Tu Asesoría Inmobiliaria — inicio" style="display:inline-flex;align-items:center;text-decoration:none">
        <img src="{prefix}assets/logo.png" alt="Tu Asesoría Inmobiliaria" style="height:54px;width:auto;display:block"/>
      </a>

      <nav aria-label="Navegación principal" style="align-items:center;gap:30px;display:flex">
        <div style="position:relative">
          <button id="propMenuBtnDesktop" aria-haspopup="true" aria-expanded="false" class="nav-link" style="display:flex;align-items:center;gap:5px;padding:0">
            Propiedades
            <svg id="propChevronDesktop" width="14" height="14" viewBox="0 0 24 24" fill="none" aria-hidden="true" style="transition:transform .2s ease"><path d="m6 9 6 6 6-6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
          </button>
          <div id="propMenuDesktop" class="hidden" role="menu" aria-label="Lista de propiedades" style="position:absolute;top:34px;left:-10px;background:#fff;border:1px solid var(--gray-300);border-radius:12px;box-shadow:0 14px 30px rgba(0,0,0,.14);padding:10px;min-width:300px;display:flex;flex-direction:column;gap:2px;z-index:60">
            {menu_items}
          </div>
        </div>
        <a class="nav-link" href="{anchor_href(prefix, 'servicios')}">Servicios</a>
        <a class="nav-link" href="{anchor_href(prefix, 'casos')}">Casos de éxito</a>
        <a class="nav-link" href="{anchor_href(prefix, 'nosotros')}">¿Por qué TuAI?</a>
        <a class="nav-link" href="{anchor_href(prefix, 'contacto')}">Contacto</a>
      </nav>

      <div style="display:flex;align-items:center;gap:14px">
        <button id="menuToggleBtn" aria-label="Abrir menú" aria-expanded="false" style="background:none;border:none;padding:8px;display:flex">
          <svg width="26" height="26" viewBox="0 0 24 24" aria-hidden="true">
            <line x1="3" y1="7" x2="21" y2="7" stroke="var(--gray-900)" stroke-width="2" stroke-linecap="round"/>
            <line x1="3" y1="12" x2="21" y2="12" stroke="var(--gray-900)" stroke-width="2" stroke-linecap="round"/>
            <line x1="3" y1="17" x2="21" y2="17" stroke="var(--gray-900)" stroke-width="2" stroke-linecap="round"/>
          </svg>
        </button>
      </div>
    </div>

    <nav id="mobileNav" class="hidden" aria-label="Navegación móvil" style="border-top:1px solid var(--gray-300);background:#fff;display:flex;flex-direction:column;padding:18px 24px;gap:16px">
      <div style="display:flex;flex-direction:column;gap:12px">
        <button id="propMenuBtnMobile" aria-expanded="false" class="nav-link" style="display:flex;align-items:center;justify-content:space-between;padding:0;width:100%">
          Propiedades
          <svg id="propChevronMobile" width="16" height="16" viewBox="0 0 24 24" fill="none" aria-hidden="true" style="transition:transform .2s ease"><path d="m6 9 6 6 6-6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
        </button>
        <div id="propMenuMobile" class="hidden" style="display:flex;flex-direction:column;gap:2px;padding-left:10px;border-left:2px solid var(--gray-300)">
          {menu_items}
        </div>
      </div>
      <a class="nav-link" href="{anchor_href(prefix, 'servicios')}" data-close-menu>Servicios</a>
      <a class="nav-link" href="{anchor_href(prefix, 'casos')}" data-close-menu>Casos de éxito</a>
      <a class="nav-link" href="{anchor_href(prefix, 'nosotros')}" data-close-menu>¿Por qué TuAI?</a>
      <a class="nav-link" href="{anchor_href(prefix, 'contacto')}" data-close-menu>Contacto</a>
      <a class="btn btn-primary" href="{anchor_href(prefix, 'contacto')}" data-close-menu style="margin-top:4px">Agenda tu visita</a>
    </nav>
  </header>
"""

def footer_html(prefix):
    return f"""  <!-- ===================== FOOTER ===================== -->
  <footer style="background:var(--gray-900);padding-block:48px 24px">
    <div class="wrap" style="display:flex;flex-wrap:wrap;gap:40px;padding-bottom:32px;border-bottom:1px solid #4a4947">
      <div style="flex:1 1 240px;display:flex;flex-direction:column;gap:14px">
        <div style="display:inline-flex;align-items:center">
          <img src="{prefix}assets/logo-negativo.png" alt="Tu Asesoría Inmobiliaria" style="height:32px;width:auto;display:block"/>
        </div>
        <p style="font-size:14px;color:var(--gray-300);line-height:1.6;max-width:260px">Tu asesoría inmobiliaria en Chile. Propiedades, asesoría y gestión en un solo lugar.</p>
        <div style="display:flex;gap:10px;margin-top:6px">
          <a class="social-btn" href="https://instagram.com/tuasesoriainmobiliaria" target="_blank" rel="noopener" aria-label="Instagram">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5" stroke="#fff" stroke-width="1.6"/><circle cx="12" cy="12" r="4" stroke="#fff" stroke-width="1.6"/><circle cx="17.3" cy="6.7" r="1" fill="#fff"/></svg>
          </a>
          <a class="social-btn" href="https://www.tiktok.com/@tuasesoriainmobiliaria" target="_blank" rel="noopener" aria-label="TikTok">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M15 3v10.5a3.5 3.5 0 1 1-3-3.46" stroke="#fff" stroke-width="1.6" stroke-linecap="round"/><path d="M15 3c0 3 2 5 5 5" stroke="#fff" stroke-width="1.6" stroke-linecap="round"/></svg>
          </a>
          <a class="social-btn" href="https://www.youtube.com/@tuasesoriainmobiliaria" target="_blank" rel="noopener" aria-label="YouTube">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true"><rect x="3" y="6" width="18" height="12" rx="3" stroke="#fff" stroke-width="1.6"/><path d="M11 10l3 2-3 2v-4Z" fill="#fff"/></svg>
          </a>
        </div>
      </div>

      <div style="flex:1 1 140px;display:flex;flex-direction:column;gap:10px">
        <p style="font-size:13px;font-weight:700;color:#fff;text-transform:uppercase;letter-spacing:.04em;margin-bottom:4px">Navegación</p>
        <a class="footer-link" href="{anchor_href(prefix, 'propiedades')}">Propiedades</a>
        <a class="footer-link" href="{anchor_href(prefix, 'servicios')}">Servicios</a>
        <a class="footer-link" href="{anchor_href(prefix, 'casos')}">Casos de éxito</a>
        <a class="footer-link" href="{anchor_href(prefix, 'nosotros')}">¿Por qué TuAI?</a>
        <a class="footer-link" href="{anchor_href(prefix, 'contacto')}">Contacto</a>
      </div>

      <div style="flex:1 1 180px;display:flex;flex-direction:column;gap:10px">
        <p style="font-size:13px;font-weight:700;color:#fff;text-transform:uppercase;letter-spacing:.04em;margin-bottom:4px">Contacto</p>
        <a class="footer-link" href="https://wa.me/{WA_PHONE}" target="_blank" rel="noopener">+56 99 8383 991</a>
        <a class="footer-link" href="mailto:hola@tuai.cl">hola@tuai.cl</a>
      </div>
    </div>
    <div class="wrap" style="padding-top:20px">
      <p style="font-size:13px;color:var(--gray-footer-text)">© 2026 Tu Asesoría Inmobiliaria · tuai.cl</p>
    </div>
  </footer>

  <!-- ===================== WHATSAPP FLOTANTE ===================== -->
  <a href="https://wa.me/{WA_PHONE}" target="_blank" rel="noopener" aria-label="Escríbenos por WhatsApp"
     style="position:fixed;bottom:22px;right:22px;width:58px;height:58px;border-radius:999px;background:#25D366;display:flex;align-items:center;justify-content:center;box-shadow:0 8px 20px rgba(0,0,0,.22);z-index:50">
    {WA_ICON_WHITE.replace('width="18" height="18"', 'width="28" height="28"')}
  </a>

</div>
"""

def tail_html(prefix, extra_scripts):
    scripts = "\n".join(f'<script src="{prefix}assets/{s}" defer></script>' for s in extra_scripts)
    return f"""{scripts}
</body>
</html>
"""

# ======================================================================
# 5) JS COMPARTIDO (assets/common.js) — menú móvil + dropdown Propiedades
#    Vive en TODAS las páginas. Sin dependencias de un PROPERTIES en JS:
#    los links del dropdown ya están pre-renderizados por Python.
# ======================================================================
COMMON_JS = """(function(){
  var menuToggleBtn = document.getElementById('menuToggleBtn');
  var mobileNav = document.getElementById('mobileNav');
  if (menuToggleBtn && mobileNav) {
    menuToggleBtn.addEventListener('click', function(){
      var open = mobileNav.classList.toggle('hidden') === false;
      menuToggleBtn.setAttribute('aria-expanded', String(open));
    });
    mobileNav.querySelectorAll('[data-close-menu]').forEach(function(el){
      el.addEventListener('click', function(){
        mobileNav.classList.add('hidden');
        menuToggleBtn.setAttribute('aria-expanded', 'false');
      });
    });
  }

  function closePropMenus(){
    var d = document.getElementById('propMenuDesktop');
    var m = document.getElementById('propMenuMobile');
    var bd = document.getElementById('propMenuBtnDesktop');
    var bm = document.getElementById('propMenuBtnMobile');
    var cd = document.getElementById('propChevronDesktop');
    var cm = document.getElementById('propChevronMobile');
    if (d) d.classList.add('hidden');
    if (m) m.classList.add('hidden');
    if (bd) bd.setAttribute('aria-expanded', 'false');
    if (bm) bm.setAttribute('aria-expanded', 'false');
    if (cd) cd.style.transform = 'rotate(0deg)';
    if (cm) cm.style.transform = 'rotate(0deg)';
  }
  function togglePropMenu(which){
    var menu = document.getElementById(which === 'desktop' ? 'propMenuDesktop' : 'propMenuMobile');
    var btn = document.getElementById(which === 'desktop' ? 'propMenuBtnDesktop' : 'propMenuBtnMobile');
    var chevron = document.getElementById(which === 'desktop' ? 'propChevronDesktop' : 'propChevronMobile');
    var willOpen = menu.classList.contains('hidden');
    closePropMenus();
    if (willOpen){
      menu.classList.remove('hidden');
      btn.setAttribute('aria-expanded', 'true');
      chevron.style.transform = 'rotate(180deg)';
    }
  }
  var btnD = document.getElementById('propMenuBtnDesktop');
  var btnM = document.getElementById('propMenuBtnMobile');
  if (btnD) btnD.addEventListener('click', function(){ togglePropMenu('desktop'); });
  if (btnM) btnM.addEventListener('click', function(){ togglePropMenu('mobile'); });
  document.addEventListener('click', function(e){
    var d = document.getElementById('propMenuDesktop');
    var bd = document.getElementById('propMenuBtnDesktop');
    if (d && !d.classList.contains('hidden') && !d.contains(e.target) && e.target !== bd && !bd.contains(e.target)) {
      closePropMenus();
    }
  });
})();
"""

# ======================================================================
# 6) JS de la portada (assets/home.js) — hero, filtro, miniaturas, formulario
# ======================================================================
HOME_JS = """(function(){
  // ---------- Hero: toggle propietario / buscador ----------
  var heroContent = {
    propietario: {
      eyebrow: 'Para dueños que quieren vender o arrendar',
      titulo: 'Vende o arrienda tu propiedad con una persona, sin perder el tiempo con un chatbot.',
      sub: 'Tasación, difusión, visitas y cierre — coordinados por nuestro equipo de principio a fin.',
      ctaLabel: 'Quiero tasar mi propiedad',
      ctaHref: 'https://wa.me/WA_PHONE?text=' + encodeURIComponent('Hola, quiero vender/arrendar mi propiedad. ¿Me ayudan con la tasación?'),
      ctaTarget: '_blank',
      switchLabel: '¿Buscas una propiedad? Ver para quién buscamos →'
    },
    buscador: {
      eyebrow: 'Para quienes buscan dónde vivir o invertir',
      titulo: 'Encontramos la propiedad que se ajusta a lo que necesitas.',
      sub: 'Departamentos, casas, parcelas y bodegas en Santiago y la Quinta Región, con acompañamiento en cada visita.',
      ctaLabel: 'Ver propiedades disponibles',
      ctaHref: '#propiedades',
      ctaTarget: '_self',
      switchLabel: '¿Quieres vender o arrendar tu propiedad? →'
    }
  };
  var heroMode = 'propietario';
  function renderHero(){
    var h = heroContent[heroMode];
    document.getElementById('heroEyebrow').textContent = h.eyebrow;
    document.getElementById('heroTitulo').textContent = h.titulo;
    document.getElementById('heroSub').textContent = h.sub;
    var cta = document.getElementById('heroCta');
    cta.textContent = h.ctaLabel;
    cta.href = h.ctaHref;
    cta.target = h.ctaTarget;
    document.getElementById('heroSwitchBtn').textContent = h.switchLabel;
    document.getElementById('heroPropietarioBtn').setAttribute('aria-pressed', String(heroMode === 'propietario'));
    document.getElementById('heroBuscadorBtn').setAttribute('aria-pressed', String(heroMode === 'buscador'));
  }
  document.getElementById('heroPropietarioBtn').addEventListener('click', function(){ heroMode = 'propietario'; renderHero(); });
  document.getElementById('heroBuscadorBtn').addEventListener('click', function(){ heroMode = 'buscador'; renderHero(); });
  document.getElementById('heroSwitchBtn').addEventListener('click', function(){ heroMode = heroMode === 'propietario' ? 'buscador' : 'propietario'; renderHero(); });
  renderHero();

  // ---------- Hero: rotación de fotos cada 5s ----------
  var heroPhotos = Array.prototype.slice.call(document.querySelectorAll('#heroPhotoData img')).map(function(img){ return img.getAttribute('src'); });
  var heroPhotoIndex = 0;
  function renderHeroPhoto(){
    if (!heroPhotos.length) return;
    document.getElementById('heroPhoto').src = heroPhotos[heroPhotoIndex];
    var dots = document.getElementById('heroDots');
    dots.innerHTML = '';
    heroPhotos.forEach(function(_, i){
      var dot = document.createElement('span');
      dot.style.cssText = 'width:7px;height:7px;border-radius:999px;background:' + (i === heroPhotoIndex ? '#fff' : 'rgba(255,255,255,.45)');
      dots.appendChild(dot);
    });
  }
  renderHeroPhoto();
  if (heroPhotos.length > 1) {
    setInterval(function(){ heroPhotoIndex = (heroPhotoIndex + 1) % heroPhotos.length; renderHeroPhoto(); }, 5000);
  }

  // ---------- Filtro de propiedades (Todas / Venta / Arriendo) ----------
  function setFilter(f){
    document.getElementById('filterAllBtn').setAttribute('aria-pressed', String(f === 'todas'));
    document.getElementById('filterVentaBtn').setAttribute('aria-pressed', String(f === 'venta'));
    document.getElementById('filterArriendoBtn').setAttribute('aria-pressed', String(f === 'arriendo'));
    document.querySelectorAll('.property-card').forEach(function(card){
      var show = f === 'todas' || card.dataset.tipo === f;
      card.classList.toggle('hidden', !show);
    });
  }
  document.getElementById('filterAllBtn').addEventListener('click', function(){ setFilter('todas'); });
  document.getElementById('filterVentaBtn').addEventListener('click', function(){ setFilter('venta'); });
  document.getElementById('filterArriendoBtn').addEventListener('click', function(){ setFilter('arriendo'); });

  // ---------- Miniaturas de cada tarjeta: clic => se ve en la foto principal ----------
  document.querySelectorAll('.property-card').forEach(function(card){
    var mainPhotoEl = card.querySelector('.card-main-photo');
    var placeholderHtml = mainPhotoEl ? mainPhotoEl.innerHTML : '';
    var thumbBtns = card.querySelectorAll('.thumb-btn');
    thumbBtns.forEach(function(btn){
      btn.addEventListener('click', function(){
        thumbBtns.forEach(function(b){ b.style.borderColor = 'transparent'; });
        btn.style.borderColor = 'var(--accent)';
        var foto = btn.getAttribute('data-foto');
        var tag = mainPhotoEl.querySelector('.tag');
        var tagHtml = tag ? tag.outerHTML : '';
        mainPhotoEl.innerHTML = (foto
          ? '<img src="' + foto + '" alt="" style="width:100%;height:100%;object-fit:cover"/>'
          : placeholderHtml.replace(/<span class="tag[^]*?<\\/span>/, '')) + tagHtml;
      });
    });
  });

  // ---------- Formulario de contacto ----------
  var form = document.getElementById('contactForm');
  if (form) {
    form.addEventListener('submit', function(e){
      e.preventDefault();
      var f = e.target;
      var data = {
        nombre: f.nombre.value,
        telefono: f.telefono.value,
        email: f.email.value,
        interes: f.interes.value,
        mensaje: f.mensaje.value
      };
      var texto = [
        'Hola TuAI, me gustaría conversar sobre una propiedad.',
        'Nombre: ' + data.nombre,
        'Teléfono: ' + data.telefono,
        'Correo: ' + data.email,
        'Interés: ' + data.interes,
        data.mensaje ? ('Mensaje: ' + data.mensaje) : null
      ].filter(Boolean).join('\\n');
      var waUrl = 'https://wa.me/WA_PHONE?text=' + encodeURIComponent(texto);

      var mailSubject = 'Nueva consulta web — ' + data.interes;
      var mailBody = [
        'Nombre: ' + data.nombre,
        'Teléfono: ' + data.telefono,
        'Correo: ' + data.email,
        'Interés: ' + data.interes,
        data.mensaje ? ('Mensaje: ' + data.mensaje) : null
      ].filter(Boolean).join('\\n');
      var mailUrl = 'mailto:EMAIL_DESTINO?subject=' + encodeURIComponent(mailSubject) + '&body=' + encodeURIComponent(mailBody);

      document.getElementById('submittedName').textContent = '¡Gracias, ' + data.nombre + '!';
      document.getElementById('submittedMsg').classList.remove('hidden');
      window.open(waUrl, '_blank', 'noopener');
      window.location.href = mailUrl;
    });
  }
})();
""".replace("WA_PHONE", WA_PHONE).replace("EMAIL_DESTINO", EMAIL_DESTINO)

# ======================================================================
# 7) JS de la ficha de propiedad (assets/ficha.js) — carrusel + "leer más"
#    Genérico: funciona igual en las 7 páginas, los datos ya vienen
#    renderizados en el HTML (cada propiedad es un archivo independiente).
# ======================================================================
FICHA_JS = """(function(){
  var carousel = document.getElementById('fichaCarousel');
  if (carousel) {
    var slides = Array.prototype.slice.call(carousel.querySelectorAll('.ficha-slide'));
    var counter = document.getElementById('fichaCounter');
    var index = 0;
    function render(){
      slides.forEach(function(s, i){ s.classList.toggle('hidden', i !== index); });
      if (counter) counter.textContent = (index + 1) + '/' + slides.length;
    }
    var prevBtn = document.getElementById('fichaPrevBtn');
    var nextBtn = document.getElementById('fichaNextBtn');
    if (prevBtn) prevBtn.addEventListener('click', function(){ index = (index - 1 + slides.length) % slides.length; render(); });
    if (nextBtn) nextBtn.addEventListener('click', function(){ index = (index + 1) % slides.length; render(); });
    render();
  }

  var toggleBtn = document.getElementById('fichaResumenToggle');
  if (toggleBtn) {
    var resumenEl = document.getElementById('fichaResumen');
    var textEl = document.getElementById('fichaResumenToggleText');
    var iconEl = document.getElementById('fichaResumenToggleIcon');
    toggleBtn.addEventListener('click', function(){
      var expanded = resumenEl.style.maxHeight !== '4.95em';
      if (expanded) {
        resumenEl.style.maxHeight = '4.95em';
        textEl.textContent = 'Leer más';
        iconEl.style.transform = 'rotate(0deg)';
      } else {
        resumenEl.style.maxHeight = resumenEl.scrollHeight + 'px';
        textEl.textContent = 'Leer menos';
        iconEl.style.transform = 'rotate(180deg)';
      }
    });
  }
})();
"""

# ======================================================================
# 8) Tarjeta de propiedad para la grilla de la portada
# ======================================================================
def thumb_btn_html(foto, index, active):
    border = "var(--accent)" if active else "transparent"
    inner = f'<img src="{foto}" style="width:100%;height:100%;object-fit:cover"/>' if foto else EXTRA_PHOTO_ICON
    data_foto = foto or ""
    return (f'<button class="thumb-btn" data-index="{index}" data-foto="{data_foto}" '
            f'aria-label="Ver foto {index+1}" style="width:40px;height:40px;border-radius:7px;overflow:hidden;'
            f'padding:0;border:2px solid {border};background:var(--gray-200);cursor:pointer;'
            f'display:flex;align-items:center;justify-content:center">{inner}</button>')

def property_card_html(p):
    fotos = p["fotos"]
    thumbs_top = "".join(thumb_btn_html(fotos[i], i, i == 0) for i in range(4))
    thumbs_bottom = "".join(thumb_btn_html(fotos[i], i, False) for i in range(4, 6))
    return f"""<article class="card property-card" data-tipo="{p['tipo_key']}" style="overflow:hidden;display:flex;flex-direction:column">
  <div class="card-main-photo" style="height:170px;position:relative;overflow:hidden">
    <div class="ph-image" style="width:100%;height:100%">{PLACEHOLDER_ICON}</div>
    <span class="tag {p['tag_class']}" style="position:absolute;top:12px;left:12px">{p['tipo']}</span>
  </div>
  <div style="padding:18px;display:flex;flex-direction:column;gap:10px;flex:1">
    <div>
      <h3 style="font-size:17px;font-weight:700;color:var(--gray-900)">{p['titulo']}</h3>
      <p style="font-size:13px;color:var(--gray-500);margin-top:2px">{p['comuna']}</p>
    </div>
    <div style="display:flex;gap:14px;align-items:flex-start;justify-content:space-between">
      <div style="display:flex;flex-direction:column;gap:8px;min-width:0">
        <span style="font-size:13px;color:var(--gray-700)">{p['specs_text']}</span>
        <span style="font-size:18px;font-weight:700;color:var(--gray-900)">{p['precio']}</span>
      </div>
      <div role="group" aria-label="Fotos de la propiedad" style="display:grid;grid-template-columns:repeat(2,40px);grid-template-rows:repeat(2,40px);gap:7px;flex:none">
        {thumbs_top}
      </div>
    </div>
    <div style="display:flex;align-items:center;justify-content:space-between;gap:14px;margin-top:auto">
      <a class="btn btn-outline btn-sm" href="{p['wa_info_link']}" target="_blank" rel="noopener">Más info</a>
      <div role="group" aria-label="Más fotos de la propiedad" style="display:flex;gap:7px;flex:none">
        {thumbs_bottom}
      </div>
    </div>
  </div>
</article>"""

# ======================================================================
# 9) Página de ficha individual (propiedades/<slug>.html)
# ======================================================================
def ficha_slide_html(foto, index):
    hidden = "" if index == 0 else " hidden"
    loading = "eager" if index == 0 else "lazy"
    if foto:
        inner = f'<img src="{foto}" alt="" loading="{loading}" style="width:100%;height:100%;object-fit:cover"/>'
    else:
        inner = f'{PLACEHOLDER_ICON}<span style="font-size:14px;color:var(--gray-500)">Foto de la propiedad</span>'
    return f'<div class="ficha-slide{hidden}" data-index="{index}" style="width:100%;height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:8px;position:absolute;inset:0">{inner}</div>'

def ficha_video_block_html(p):
    if p["video_youtube"]:
        right = (f'<a href="{p["video_youtube"]}" target="_blank" rel="noopener" '
                 f'style="display:flex;align-items:center;gap:5px;font-size:14px;font-weight:700">Ver en YouTube'
                 f'<svg width="14" height="14" viewBox="0 0 24 24" fill="none" aria-hidden="true">'
                 f'<path d="M7 17 17 7M9 7h8v8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></a>')
    else:
        right = '<span style="font-size:13px;color:var(--gray-500)">Pendiente de carga</span>'
    return f"""<div class="card" style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:10px;padding:14px 18px;border-width:2px;border-color:var(--accent)">
      <span style="display:flex;align-items:center;gap:10px;font-weight:700;color:var(--gray-900)">
        <span class="icon-badge icon-accent" style="width:32px;height:32px;border-radius:999px">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="var(--accent)" aria-hidden="true"><path d="M8 5v14l11-7-11-7Z"/></svg>
        </span>
        Video de la propiedad
      </span>
      {right}
    </div>"""

def ficha_image_block_html(img_src, placeholder_icon, placeholder_text, alt):
    if img_src:
        return f'<img src="{img_src}" alt="{alt}" style="width:100%;height:100%;object-fit:contain"/>'
    return f'{placeholder_icon}<span style="font-size:13px;color:var(--gray-500)">{placeholder_text}</span>'

CARACTERISTICAS = [
    ("fichaDormitorios", "Dormitorios", "dormitorios",
     '<path d="M3 18v-6a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v6M3 18v2M21 18v2M3 12V8a1 1 0 0 1 1-1h6v5" stroke="var(--gray-500)" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>'),
    ("fichaBanos", "Baños", "banos",
     '<path d="M4 12h15a1 1 0 0 1 1 1v2a4 4 0 0 1-4 4H7a4 4 0 0 1-4-4v-3Z" stroke="var(--gray-500)" stroke-width="1.6" stroke-linejoin="round"/><path d="M7 12V6a2 2 0 0 1 3.46-1.37M3 12v0M19 20l-1 2M7 20l-1 2" stroke="var(--gray-500)" stroke-width="1.6" stroke-linecap="round"/>'),
    ("fichaSupUtil", "Superficie útil", "superficie_util",
     '<path d="M20 4 13 11M9 4H4v5M20 20l-7-7M4 15v5h5" stroke="var(--gray-500)" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>'),
    ("fichaSupTotal", "Superficie total", "superficie_total",
     '<rect x="4" y="4" width="16" height="16" rx="2" stroke="var(--gray-500)" stroke-width="1.6" stroke-dasharray="3 3"/>'),
    ("fichaEstac", "Estacionamientos", "estacionamientos",
     '<path d="M5 11l1.5-4.5A2 2 0 0 1 8.4 5h7.2a2 2 0 0 1 1.9 1.5L19 11M5 11h14a1 1 0 0 1 1 1v4a1 1 0 0 1-1 1h-1v2h-2v-2H8v2H6v-2H5a1 1 0 0 1-1-1v-4a1 1 0 0 1 1-1Z" stroke="var(--gray-500)" stroke-width="1.6" stroke-linejoin="round"/><circle cx="7.5" cy="14.5" r="1" fill="var(--gray-500)"/><circle cx="16.5" cy="14.5" r="1" fill="var(--gray-500)"/>'),
    ("fichaBodega", "Bodega", "bodega",
     '<path d="M3 10.5 12 3l9 7.5" stroke="var(--gray-500)" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/><path d="M5 9.5V20a1 1 0 0 0 1 1h4v-6h4v6h4a1 1 0 0 0 1-1V9.5" stroke="var(--gray-500)" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>'),
]

def caracteristicas_grid_html(p):
    items = []
    for elem_id, label, field, svg_path in CARACTERISTICAS:
        items.append(f"""<div style="display:flex;align-items:center;gap:14px">
      <span class="icon-badge"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" aria-hidden="true">{svg_path}</svg></span>
      <span><p style="font-size:13px;color:var(--gray-500)">{label}</p><p id="{elem_id}" style="font-size:15px;font-weight:700;color:var(--gray-900)">{p[field]}</p></span>
    </div>""")
    return "\n    ".join(items)

def ficha_page_html(p):
    prefix = "../"
    slides = "".join(ficha_slide_html(f, i) for i, f in enumerate(p["fotos"]))
    total = len(p["fotos"])
    title = f"{p['titulo']} | Tu Asesoría Inmobiliaria"
    description = f"{p['titulo']} en {p['comuna']}. {p['specs_text']}."
    html = head_html(title, description, prefix)
    html += header_html(prefix)
    html += f"""  <main style="flex:1">
    <section style="padding-block:40px 80px">
      <div class="wrap" style="display:flex;flex-direction:column;gap:36px;max-width:720px">
        <a href="{anchor_href(prefix, 'propiedades')}" style="display:flex;align-items:center;gap:6px;font-size:14px;font-weight:700;color:var(--gray-700);width:fit-content">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M15 6 9 12l6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
          Volver a propiedades
        </a>

        <!-- Carrusel de fotos -->
        <div id="fichaCarousel" class="ph-image" style="position:relative;width:100%;aspect-ratio:16/10;border-radius:14px;overflow:hidden">
          {slides}
          <button id="fichaPrevBtn" aria-label="Foto anterior" style="position:absolute;left:14px;top:50%;transform:translateY(-50%);width:38px;height:38px;border-radius:999px;background:#fff;border:none;display:flex;align-items:center;justify-content:center;box-shadow:0 2px 8px rgba(0,0,0,.18);cursor:pointer;z-index:2">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="m15 6-6 6 6 6" stroke="var(--gray-900)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
          </button>
          <button id="fichaNextBtn" aria-label="Foto siguiente" style="position:absolute;right:14px;top:50%;transform:translateY(-50%);width:38px;height:38px;border-radius:999px;background:#fff;border:none;display:flex;align-items:center;justify-content:center;box-shadow:0 2px 8px rgba(0,0,0,.18);cursor:pointer;z-index:2">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="m9 6 6 6-6 6" stroke="var(--gray-900)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
          </button>
          <span id="fichaCounter" style="position:absolute;bottom:12px;right:14px;background:rgba(0,0,0,.6);color:#fff;font-size:12px;font-weight:700;padding:4px 10px;border-radius:999px;z-index:2">1/{total}</span>
        </div>

        <!-- Video de la propiedad -->
        {ficha_video_block_html(p)}

        <!-- Título y precio -->
        <div style="display:flex;flex-direction:column;gap:8px">
          <span class="tag {p['tag_class']}" style="align-self:flex-start">{p['tipo']}</span>
          <h1 style="font-size:clamp(24px,3.4vw,32px);font-weight:700;color:var(--gray-900);line-height:1.2">{p['titulo']}</h1>
          <p style="font-size:15px;color:var(--gray-500)">{p['comuna']}</p>
          <div style="display:flex;align-items:baseline;gap:12px;flex-wrap:wrap;padding-top:8px;margin-top:4px;border-top:1px solid var(--gray-300)">
            <span style="font-size:26px;font-weight:700;color:var(--gray-900)">{p['uf_precio']}</span>
            <span style="font-size:14px;color:var(--gray-500)">{p['clp_precio']}</span>
          </div>
        </div>

        <!-- Características técnicas -->
        <div style="display:flex;flex-direction:column;gap:18px">
          <h2 style="font-size:19px;font-weight:700;color:var(--gray-900)">Características técnicas</h2>
          <div style="display:grid;grid-template-columns:repeat(auto-fit, minmax(200px,1fr));gap:22px 28px">
            {caracteristicas_grid_html(p)}
          </div>
        </div>

        <!-- Resumen -->
        <div style="display:flex;flex-direction:column;gap:12px">
          <h2 style="font-size:19px;font-weight:700;color:var(--gray-900)">Resumen</h2>
          <p id="fichaResumen" style="font-size:15px;color:var(--gray-700);line-height:1.65;max-height:4.95em;overflow:hidden;transition:max-height .3s ease">{p['resumen']}</p>
          <button id="fichaResumenToggle" style="background:none;border:none;padding:0;color:var(--accent);font-weight:700;font-size:14px;display:flex;align-items:center;gap:4px;width:fit-content">
            <span id="fichaResumenToggleText">Leer más</span>
            <svg id="fichaResumenToggleIcon" width="14" height="14" viewBox="0 0 24 24" fill="none" aria-hidden="true" style="transition:transform .2s ease"><path d="m6 9 6 6 6-6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
          </button>
        </div>

        <!-- Plano -->
        <div style="display:flex;flex-direction:column;gap:12px">
          <h2 style="font-size:19px;font-weight:700;color:var(--gray-900)">Plano de la propiedad</h2>
          <div class="ph-image" style="width:100%;min-height:190px;border-radius:14px;flex-direction:column;gap:8px">
            {ficha_image_block_html(p['plano_img'], PLANO_PLACEHOLDER_ICON, 'Plano pendiente de carga', f"Plano de {p['titulo']}")}
          </div>
        </div>

        <!-- Mapa -->
        <div style="display:flex;flex-direction:column;gap:12px">
          <h2 style="font-size:19px;font-weight:700;color:var(--gray-900)">Mapa</h2>
          <div class="ph-image" style="width:100%;min-height:190px;border-radius:14px;flex-direction:column;gap:8px">
            {ficha_image_block_html(p['mapa_img'], MAPA_PLACEHOLDER_ICON, 'Mapa pendiente de carga', f"Ubicación de {p['titulo']}")}
          </div>
        </div>

        <!-- Información económica -->
        <div style="display:flex;flex-direction:column;gap:12px">
          <h2 style="font-size:19px;font-weight:700;color:var(--gray-900)">Información económica</h2>
          <div class="card" style="padding:20px;display:flex;flex-direction:column;gap:2px">
            <p style="font-size:14px;font-weight:700;color:var(--gray-900);padding-bottom:12px">Simulación de crédito a 30 años</p>
            <div style="display:flex;justify-content:space-between;padding:10px 0;border-top:1px dashed var(--gray-300)"><span style="font-size:14px;color:var(--gray-700)">Pie</span><span style="font-size:14px;font-weight:700;color:var(--gray-900)">{p['pie']}</span></div>
            <div style="display:flex;justify-content:space-between;padding:10px 0;border-top:1px dashed var(--gray-300)"><span style="font-size:14px;color:var(--gray-700)">Monto a financiar</span><span style="font-size:14px;font-weight:700;color:var(--gray-900)">{p['monto_financiar']}</span></div>
            <div style="display:flex;justify-content:space-between;padding:10px 0;border-top:1px dashed var(--gray-300)"><span style="font-size:14px;color:var(--gray-700)">Dividendo estimado</span><span style="font-size:14px;font-weight:700;color:var(--gray-900)">{p['dividendo_estimado']}</span></div>
            <p style="font-size:11px;color:var(--gray-500);padding-top:10px">Pie 10% · Información referencial al día de hoy. Si deseas más información puedes consultar el <a href="https://servicios.cmfchile.cl/simuladorhipotecario/aplicacion?indice=101.2.1" target="_blank" rel="noopener" style="color:var(--gray-500);text-decoration:underline">simulador hipotecario de la CMF</a>.</p>
          </div>
        </div>

        <!-- CTA -->
        <div style="display:flex;flex-direction:column;align-items:center;gap:14px;text-align:center;padding-top:8px">
          <p style="font-size:17px;font-weight:700;color:var(--gray-900)">¿Quieres visitar esta propiedad?</p>
          <a href="{p['wa_link']}" target="_blank" rel="noopener" class="btn" style="background:#25D366;color:#fff;width:100%;max-width:420px">
            {WA_ICON_WHITE}
            Agenda tu visita por WhatsApp
          </a>
        </div>
      </div>
    </section>
  </main>
"""
    html += footer_html(prefix)
    html += tail_html(prefix, ["common.js", "ficha.js"])
    return html

# ======================================================================
# 10) Página principal (index.html)
# ======================================================================
def home_page_html():
    prefix = ""
    cards_html = "\n".join(property_card_html(p) for p in PROPERTIES)
    title = "Tu Asesoría Inmobiliaria — Venta y Arriendo de Propiedades"
    description = "Venta y arriendo de propiedades en Santiago y la Quinta Región. Tasación, difusión, visitas y cierre acompañados por nuestro equipo."
    html = head_html(title, description, prefix)
    html += header_html(prefix)
    html += f"""  <main style="flex:1">

    <!-- ===================== HERO ===================== -->
    <section id="inicio" style="background:var(--gray-100);border-bottom:1px solid var(--gray-300)">
      <div class="wrap" style="padding-block:28px 56px">

        <div role="group" aria-label="¿Qué necesitas?" style="display:flex;gap:8px;margin-bottom:28px;max-width:560px">
          <button class="filter-pill" id="heroPropietarioBtn" aria-pressed="true" style="flex:1;text-align:center;padding:14px 10px;font-size:13.5px;min-height:48px">Vender o arrendar mi propiedad</button>
          <button class="filter-pill" id="heroBuscadorBtn" aria-pressed="false" style="flex:1;text-align:center;padding:14px 10px;font-size:13.5px;min-height:48px">Busco una propiedad</button>
        </div>

        <div style="display:flex;flex-wrap:wrap;align-items:center;gap:48px">
          <div style="flex:1 1 460px;min-width:0;display:flex;flex-direction:column;gap:18px">
            <span class="eyebrow" id="heroEyebrow">Para dueños que quieren vender o arrendar</span>
            <h1 id="heroTitulo" style="font-size:clamp(30px,5vw,48px);font-weight:700;line-height:1.12;color:var(--gray-900)">Vende o arrienda tu propiedad con una persona, sin perder el tiempo con un chatbot.</h1>
            <p class="section-sub" id="heroSub" style="font-size:17px;max-width:500px">Tasación, difusión, visitas y cierre — coordinados por nuestro equipo de principio a fin.</p>
            <a class="btn btn-primary" id="heroCta" href="#" target="_blank" rel="noopener" style="width:100%;max-width:360px;justify-content:center;margin-top:2px">Quiero tasar mi propiedad</a>
            <button id="heroSwitchBtn" style="background:none;border:none;padding:0;text-align:left;font-size:14px;color:var(--gray-500);text-decoration:underline;width:fit-content;cursor:pointer">¿Buscas una propiedad? Ver para quién buscamos →</button>
          </div>

          <div style="flex:1 1 360px;min-width:280px;display:flex;flex-direction:column;gap:14px">
            <div class="card enter" style="height:260px;border-radius:14px;overflow:hidden;padding:0;position:relative">
              <img id="heroPhoto" src="{HOME_HERO_PHOTOS[0]}" alt="Propiedad gestionada por TuAI" style="width:100%;height:100%;object-fit:cover;transition:opacity .4s ease"/>
              <span style="position:absolute;top:12px;right:12px;display:flex;align-items:center;gap:5px;background:rgba(0,0,0,.55);color:#fff;font-size:11px;font-weight:600;padding:5px 10px 5px 8px;border-radius:999px;backdrop-filter:blur(2px)">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5" stroke="#fff" stroke-width="1.8"/><circle cx="12" cy="12" r="4" stroke="#fff" stroke-width="1.8"/><circle cx="17.2" cy="6.8" r="1" fill="#fff"/></svg>
                Novedades en Instagram
              </span>
              <div id="heroDots" role="group" aria-label="Fotos destacadas" style="position:absolute;bottom:12px;left:12px;display:flex;gap:6px"></div>
            </div>
            <div id="heroPhotoData" class="hidden" aria-hidden="true">
              {"".join(f'<img src="{src}"/>' for src in HOME_HERO_PHOTOS)}
            </div>
            <div style="display:flex;align-items:center;gap:10px">
              <div style="display:flex">
                <span style="width:28px;height:28px;border-radius:999px;background:var(--gray-900);color:#fff;font-size:11px;font-weight:700;display:flex;align-items:center;justify-content:center;border:2px solid var(--gray-100)">P</span>
                <span style="width:28px;height:28px;border-radius:999px;background:var(--accent);color:#fff;font-size:11px;font-weight:700;display:flex;align-items:center;justify-content:center;border:2px solid var(--gray-100);margin-left:-8px">A</span>
              </div>
              <span style="font-size:13px;color:var(--gray-700)">Respondemos por WhatsApp, normalmente en minutos</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ===================== PROPIEDADES DESTACADAS ===================== -->
    <section id="propiedades" style="padding-block:72px">
      <div class="wrap" style="display:flex;flex-direction:column;gap:32px">
        <div style="display:flex;flex-wrap:wrap;justify-content:space-between;align-items:flex-end;gap:20px">
          <div style="display:flex;flex-direction:column;gap:12px;max-width:620px">
            <span class="eyebrow">Propiedades destacadas</span>
            <h2 class="section-title">Cada propiedad, con ficha propia</h2>
            <p class="section-sub">Departamentos, casas, bodegas, parcelas, sitios y estacionamientos. Escríbenos directo por cada una, o revisa el detalle completo desde el menú Propiedades.</p>
          </div>
          <div role="group" aria-label="Filtrar propiedades" style="display:flex;gap:10px;flex-wrap:wrap">
            <button class="filter-pill" id="filterAllBtn" aria-pressed="true">Todas</button>
            <button class="filter-pill" id="filterVentaBtn" aria-pressed="false">Venta</button>
            <button class="filter-pill" id="filterArriendoBtn" aria-pressed="false">Arriendo</button>
          </div>
        </div>

        <div id="propertiesGrid" style="display:grid;grid-template-columns:repeat(auto-fit, minmax(270px, 1fr));gap:22px">
          {cards_html}
        </div>

        <p style="font-size:13px;color:var(--gray-500);border-top:1px dashed var(--gray-300);padding-top:16px">
          Fotos, specs y precios quedan pendientes de carga — cada propiedad vive en su propio archivo, independiente del resto, para poder publicar o retirar una sin afectar las demás.
        </p>
      </div>
    </section>

    <!-- ===================== HISTORIAS EXITOSAS ===================== -->
    <section id="casos" style="background:var(--gray-100);padding-block:72px;border-top:1px solid var(--gray-300);border-bottom:1px solid var(--gray-300)">
      <div class="wrap" style="display:flex;flex-direction:column;gap:32px">
        <div style="display:flex;flex-direction:column;gap:12px;max-width:620px">
          <span class="eyebrow">Historias de éxito</span>
          <h2 class="section-title">Clientes que ya encontraron lo suyo</h2>
          <p class="section-sub">Procesos de compra, venta y arriendo acompañados de principio a fin por nuestro equipo.</p>
        </div>

        <div style="display:grid;grid-template-columns:repeat(auto-fit, minmax(280px, 1fr));gap:22px">
          <article class="card" style="overflow:hidden;display:flex;flex-direction:column">
            <div class="ph-image" style="height:160px">
              <svg width="42" height="42" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                <circle cx="12" cy="8" r="3.4" stroke="var(--gray-500)" stroke-width="1.6"/>
                <path d="M5 20c0-3.5 3-6 7-6s7 2.5 7 6" stroke="var(--gray-500)" stroke-width="1.6" stroke-linecap="round"/>
              </svg>
            </div>
            <div style="padding:20px;display:flex;flex-direction:column;gap:12px">
              <span class="tag tag-arriendo" style="align-self:flex-start">Arriendo concretado</span>
              <p style="font-size:15px;color:var(--gray-700);line-height:1.55;font-style:italic">"Encontramos el departamento en menos de dos semanas. Patricia nos acompañó en cada visita y en la firma del contrato."</p>
              <p style="font-size:14px;font-weight:700;color:var(--gray-900)">Daniela R. · Arrendataria</p>
            </div>
          </article>
          <article class="card" style="overflow:hidden;display:flex;flex-direction:column">
            <div class="ph-image" style="height:160px">
              <svg width="42" height="42" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                <circle cx="12" cy="8" r="3.4" stroke="var(--gray-500)" stroke-width="1.6"/>
                <path d="M5 20c0-3.5 3-6 7-6s7 2.5 7 6" stroke="var(--gray-500)" stroke-width="1.6" stroke-linecap="round"/>
              </svg>
            </div>
            <div style="padding:20px;display:flex;flex-direction:column;gap:12px">
              <span class="tag tag-venta" style="align-self:flex-start">Venta concretada</span>
              <p style="font-size:15px;color:var(--gray-700);line-height:1.55;font-style:italic">"Vendí mi casa en Ñuñoa sin complicaciones. Álvaro se encargó de la tasación, la difusión y el cierre con el banco."</p>
              <p style="font-size:14px;font-weight:700;color:var(--gray-900)">Jorge M. · Vendedor</p>
            </div>
          </article>
          <article class="card" style="overflow:hidden;display:flex;flex-direction:column">
            <div class="ph-image" style="height:160px">
              <svg width="42" height="42" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                <circle cx="12" cy="8" r="3.4" stroke="var(--gray-500)" stroke-width="1.6"/>
                <path d="M5 20c0-3.5 3-6 7-6s7 2.5 7 6" stroke="var(--gray-500)" stroke-width="1.6" stroke-linecap="round"/>
              </svg>
            </div>
            <div style="padding:20px;display:flex;flex-direction:column;gap:12px">
              <span class="tag tag-venta" style="align-self:flex-start">Compra concretada</span>
              <p style="font-size:15px;color:var(--gray-700);line-height:1.55;font-style:italic">"Buscábamos algo específico para la familia y nos mostraron solo propiedades que realmente calzaban. Proceso directo y sin presión."</p>
              <p style="font-size:14px;font-weight:700;color:var(--gray-900)">Familia Contreras · Compradores</p>
            </div>
          </article>
        </div>

        <p style="font-size:13px;color:var(--gray-500);border-top:1px dashed var(--gray-300);padding-top:16px">
          Casos ilustrativos — se reemplazan por testimonios y fotografías reales de clientes a medida que estén disponibles.
        </p>
      </div>
    </section>

    <!-- ===================== SERVICIOS ===================== -->
    <section id="servicios" style="padding-block:72px">
      <div class="wrap" style="display:flex;flex-direction:column;gap:32px">
        <div style="display:flex;flex-direction:column;gap:12px;max-width:620px">
          <span class="eyebrow">Servicios</span>
          <h2 class="section-title">Todo lo que necesitas, en un solo lugar</h2>
        </div>

        <div style="display:grid;grid-template-columns:repeat(auto-fit, minmax(240px, 1fr));gap:22px">
          <div class="card" style="padding:26px;display:flex;flex-direction:column;gap:14px">
            <div class="icon-badge icon-accent">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M12 3 4 9v12h16V9l-8-6Z" stroke-width="1.6" stroke-linejoin="round"/><path d="M9 21v-6h6v6" stroke-width="1.6"/></svg>
            </div>
            <h3 style="font-size:18px;font-weight:700">Venta de propiedades</h3>
            <p style="font-size:14px;color:var(--gray-700);line-height:1.55">Tasación, difusión y cierre de la operación con acompañamiento legal en cada etapa.</p>
          </div>

          <div class="card" style="padding:26px;display:flex;flex-direction:column;gap:14px">
            <div class="icon-badge icon-accent">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" aria-hidden="true"><rect x="4" y="10" width="16" height="10" rx="1.4" stroke-width="1.6"/><path d="M8 10V7a4 4 0 0 1 8 0v3" stroke-width="1.6"/></svg>
            </div>
            <h3 style="font-size:18px;font-weight:700">Arriendo de propiedades</h3>
            <p style="font-size:14px;color:var(--gray-700);line-height:1.55">Búsqueda de arrendatarios, contratos y gestión de la relación entre las partes.</p>
          </div>

          <div class="card" style="padding:26px;display:flex;flex-direction:column;gap:14px">
            <div class="icon-badge icon-accent">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M12 21s-7-4.4-9-9.4C1.3 7.6 4 4.5 7.3 4.5c2 0 3.6 1 4.7 2.6 1.1-1.6 2.7-2.6 4.7-2.6 3.3 0 6 3.1 4.3 7.1C19 16.6 12 21 12 21Z" stroke-width="1.6" stroke-linejoin="round"/></svg>
            </div>
            <h3 style="font-size:18px;font-weight:700">Asesoría integral</h3>
            <p style="font-size:14px;color:var(--gray-700);line-height:1.55">Orientación legal y financiera para comprar, vender o arrendar con decisiones informadas.</p>
          </div>

          <div class="card" style="padding:26px;display:flex;flex-direction:column;gap:14px">
            <div class="icon-badge icon-accent">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5" stroke-width="1.6"/><circle cx="12" cy="12" r="4" stroke-width="1.6"/><circle cx="17.3" cy="6.7" r="1" fill="var(--accent)"/></svg>
            </div>
            <h3 style="font-size:18px;font-weight:700">Marketing inmobiliario</h3>
            <p style="font-size:14px;color:var(--gray-700);line-height:1.55">Fotografía, video y presencia activa en Instagram y TikTok para cada propiedad en cartera.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- ===================== POR QUÉ TUAI ===================== -->
    <section id="nosotros" style="background:var(--gray-900);padding-block:72px">
      <div class="wrap" style="display:flex;flex-wrap:wrap;gap:48px">
        <div style="flex:1 1 360px;min-width:0;display:flex;flex-direction:column;gap:16px">
          <span class="eyebrow">¿Por qué TuAI?</span>
          <h2 class="section-title" style="color:#fff">El "Tu" va primero, siempre</h2>
          <p style="font-size:16px;color:var(--gray-300);line-height:1.65;max-width:460px">
            Nuestro nombre lo dice todo: antes que la propiedad, está la persona. Un equipo acotado, con experiencia en banca y finanzas, que conoce el mercado y acompaña cada decisión de cerca.
          </p>
        </div>

        <div style="flex:1 1 420px;min-width:280px;display:grid;grid-template-columns:repeat(auto-fit, minmax(190px, 1fr));gap:20px">
          <div style="display:flex;flex-direction:column;gap:10px">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M20 6 9 17l-5-5" stroke="var(--accent)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
            <h3 style="font-size:16px;font-weight:700;color:#fff">Equipo especializado</h3>
            <p style="font-size:14px;color:var(--gray-300);line-height:1.5">Broker, abogado, tasador y experto tributario, con dedicación directa a cada cliente.</p>
          </div>
          <div style="display:flex;flex-direction:column;gap:10px">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M20 6 9 17l-5-5" stroke="var(--accent)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
            <h3 style="font-size:16px;font-weight:700;color:#fff">Visión financiera</h3>
            <p style="font-size:14px;color:var(--gray-300);line-height:1.5">Trayectoria en banca y retail finance aplicada a cada operación inmobiliaria.</p>
          </div>
          <div style="display:flex;flex-direction:column;gap:10px">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M20 6 9 17l-5-5" stroke="var(--accent)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
            <h3 style="font-size:16px;font-weight:700;color:#fff">Presencia digital activa</h3>
            <p style="font-size:14px;color:var(--gray-300);line-height:1.5">Contenido constante en Instagram y TikTok mostrando cada propiedad en detalle.</p>
          </div>
          <div style="display:flex;flex-direction:column;gap:10px">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M20 6 9 17l-5-5" stroke="var(--accent)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
            <h3 style="font-size:16px;font-weight:700;color:#fff">Comunicación directa</h3>
            <p style="font-size:14px;color:var(--gray-300);line-height:1.5">Respuesta por WhatsApp, sin intermediarios ni esperas innecesarias.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- ===================== NUESTRO EQUIPO ===================== -->
    <section id="equipo" style="padding-block:72px">
      <div class="wrap" style="display:flex;flex-direction:column;gap:32px">
        <div style="display:flex;flex-direction:column;gap:12px;max-width:620px">
          <span class="eyebrow">Nuestro equipo</span>
          <h2 class="section-title">Un especialista para cada parte del proceso</h2>
          <p class="section-sub">Venta, arriendo, aspectos legales, tasación y temas tributarios — cada etapa la lleva quien sabe de eso.</p>
        </div>

        <div style="display:grid;grid-template-columns:repeat(auto-fit, minmax(190px, 1fr));gap:20px">
          <div class="card" style="padding:22px;display:flex;flex-direction:column;gap:10px;text-align:center;align-items:center">
            <span style="font-size:30px;line-height:1">🏠</span>
            <h3 style="font-size:16px;font-weight:700;color:var(--gray-900)">Patricia</h3>
            <p style="font-size:13px;color:var(--gray-500);line-height:1.4">Broker Inmobiliario</p>
          </div>
          <div class="card" style="padding:22px;display:flex;flex-direction:column;gap:10px;text-align:center;align-items:center">
            <span style="font-size:30px;line-height:1">📱</span>
            <h3 style="font-size:16px;font-weight:700;color:var(--gray-900)">Álvaro</h3>
            <p style="font-size:13px;color:var(--gray-500);line-height:1.4">Marketing Inmobiliario y RRSS</p>
          </div>
          <div class="card" style="padding:22px;display:flex;flex-direction:column;gap:10px;text-align:center;align-items:center">
            <span style="font-size:30px;line-height:1">⚖️</span>
            <h3 style="font-size:16px;font-weight:700;color:var(--gray-900)">Rodolfo</h3>
            <p style="font-size:13px;color:var(--gray-500);line-height:1.4">Abogado especialista en el Mercado Inmobiliario</p>
          </div>
          <div class="card" style="padding:22px;display:flex;flex-direction:column;gap:10px;text-align:center;align-items:center">
            <span style="font-size:30px;line-height:1">🏦</span>
            <h3 style="font-size:16px;font-weight:700;color:var(--gray-900)">Silvio</h3>
            <p style="font-size:13px;color:var(--gray-500);line-height:1.4">Especialista en tasaciones bancarias</p>
          </div>
          <div class="card" style="padding:22px;display:flex;flex-direction:column;gap:10px;text-align:center;align-items:center">
            <span style="font-size:30px;line-height:1">🧾</span>
            <h3 style="font-size:16px;font-weight:700;color:var(--gray-900)">Marcos</h3>
            <p style="font-size:13px;color:var(--gray-500);line-height:1.4">Experto Tributario</p>
          </div>
        </div>
      </div>
    </section>

    <!-- ===================== CONTACTO ===================== -->
    <section id="contacto" style="padding-block:72px">
      <div class="wrap" style="display:flex;flex-wrap:wrap;gap:48px">

        <div style="flex:1 1 420px;min-width:0;display:flex;flex-direction:column;gap:20px">
          <span class="eyebrow">Contáctanos</span>
          <h2 class="section-title">Cuéntanos qué necesitas</h2>
          <p class="section-sub">Déjanos tus datos y te contactamos para coordinar una visita o responder tus dudas.</p>

          <div id="submittedMsg" class="hidden card" style="padding:20px;border-color:var(--accent);background:#FFF6F2;display:flex;flex-direction:column;gap:6px">
            <strong style="color:var(--gray-900)" id="submittedName">¡Gracias!</strong>
            <span style="font-size:14px;color:var(--gray-700)">Vas a abrir WhatsApp para enviarnos tu consulta. También puedes escribirnos directo cuando quieras.</span>
          </div>

          <form id="contactForm" style="display:flex;flex-direction:column;gap:16px;margin-top:4px">
            <div style="display:flex;gap:16px;flex-wrap:wrap">
              <div class="form-field" style="flex:1 1 200px">
                <label for="nombre">Nombre</label>
                <input id="nombre" name="nombre" type="text" required placeholder="Tu nombre"/>
              </div>
              <div class="form-field" style="flex:1 1 200px">
                <label for="telefono">Teléfono</label>
                <input id="telefono" name="telefono" type="tel" required placeholder="+56 9 ____ ____"/>
              </div>
            </div>
            <div class="form-field">
              <label for="email">Correo</label>
              <input id="email" name="email" type="email" required placeholder="tu@correo.cl"/>
            </div>
            <div class="form-field">
              <label for="interes">Me interesa</label>
              <select id="interes" name="interes">
                <option>Comprar una propiedad</option>
                <option>Vender mi propiedad</option>
                <option>Arrendar una propiedad</option>
                <option>Arrendar mi propiedad</option>
                <option>Otra consulta</option>
              </select>
            </div>
            <div class="form-field">
              <label for="mensaje">Mensaje</label>
              <textarea id="mensaje" name="mensaje" rows="3" placeholder="Cuéntanos brevemente qué buscas"></textarea>
            </div>
            <button type="submit" class="btn btn-primary" style="align-self:flex-start;border:none">Enviar y continuar en WhatsApp</button>
          </form>
        </div>

        <div style="flex:1 1 320px;min-width:260px;display:flex;flex-direction:column;gap:16px">
          <div class="card" style="padding:26px;display:flex;flex-direction:column;gap:18px">
            <h3 style="font-size:16px;font-weight:700;color:var(--gray-900)">Habla directo con nosotros</h3>

            <a href="https://wa.me/{WA_PHONE}" target="_blank" rel="noopener" style="display:flex;align-items:center;gap:12px;text-decoration:none">
              <span class="icon-badge" style="background:#E8F8EE">{WA_ICON_GREEN.replace('width="18" height="18"', 'width="20" height="20"')}</span>
              <span>
                <p style="font-size:14px;color:var(--gray-500)">WhatsApp</p>
                <p style="font-size:15px;font-weight:700;color:var(--gray-900)">+56 99 8383 991</p>
              </span>
            </a>

            <a href="mailto:hola@tuai.cl" style="display:flex;align-items:center;gap:12px;text-decoration:none">
              <span class="icon-badge icon-accent"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2" stroke-width="1.6"/><path d="m4 7 8 6 8-6" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg></span>
              <span>
                <p style="font-size:14px;color:var(--gray-500)">Correo</p>
                <p style="font-size:15px;font-weight:700;color:var(--gray-900)">hola@tuai.cl</p>
              </span>
            </a>

            <div style="border-top:1px solid var(--gray-300);padding-top:16px">
              <a href="#equipo">Conoce a todo el equipo →</a>
            </div>
          </div>

          <div class="card ph-image" style="height:180px;border-radius:10px;flex-direction:column;gap:8px">
            <svg width="30" height="30" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M12 21s-6.5-5.8-6.5-11A6.5 6.5 0 0 1 18.5 10c0 5.2-6.5 11-6.5 11Z" stroke="var(--gray-500)" stroke-width="1.6" stroke-linejoin="round"/><circle cx="12" cy="10" r="2.4" stroke="var(--gray-500)" stroke-width="1.6"/></svg>
            <span style="font-size:13px;color:var(--gray-500);font-weight:600">Zona de cobertura</span>
            <span style="font-size:12px;color:var(--gray-500)">Santiago y la Quinta Región</span>
          </div>
        </div>
      </div>
    </section>

  </main>
"""
    html += footer_html(prefix)
    html += tail_html(prefix, ["common.js", "home.js"])
    return html

# ======================================================================
# 11) Escritura de todos los archivos
# ======================================================================
def write_file(rel_path, content):
    full_path = os.path.join(ROOT, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("  ->", rel_path, f"({len(content)} bytes)")

def main():
    print("Generando sitio...")
    write_file("assets/styles.css", STYLE_CSS)
    write_file("assets/common.js", COMMON_JS)
    write_file("assets/home.js", HOME_JS)
    write_file("assets/ficha.js", FICHA_JS)
    write_file("index.html", home_page_html())
    for p in PROPERTIES:
        write_file(f"{PROP_DIR}/{p['slug']}.html", ficha_page_html(p))
    print("Listo:", len(PROPERTIES), "fichas +", "index.html")

if __name__ == "__main__":
    main()

