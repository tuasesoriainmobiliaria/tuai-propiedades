# Sitio de producción — Tu Asesoría Inmobiliaria (TuAI)

Este es el sitio real, listo para publicar en GitHub Pages + el dominio `tuai.cl`.
No depende de ninguna herramienta especial (no Jekyll, no Node, no build step):
son archivos `.html`, `.css` y `.js` planos que cualquier hosting estático
puede servir tal cual.

## Qué hay acá

```
tuai-site/
├── index.html                  ← portada
├── propiedades/
│   ├── casa-tunquen.html
│   ├── depto-san-miguel.html
│   ├── depto-san-bernardo.html
│   ├── depto-pucon.html
│   ├── estacionamiento-santiago-centro.html
│   ├── bodega-tocornal.html
│   └── terreno-metro-nuble.html
├── assets/
│   ├── styles.css              ← estilos compartidos por todas las páginas
│   ├── common.js                ← menú móvil + dropdown "Propiedades"
│   ├── home.js                  ← lógica exclusiva de la portada
│   ├── ficha.js                  ← carrusel y "leer más" de cada ficha
│   ├── logo.png, logo-negativo.png
│   └── hero-1.jpg, hero-2.jpg, hero-3.jpg
└── build_site.py                ← el generador (ver más abajo)
```

Cada propiedad vive en su propio archivo `.html`, con su propio link para
compartir — tal como se acordó en el diseño original.

## Cómo publicarlo (GitHub Pages + tuai.cl)

1. **Crear el repositorio en GitHub** (si no existe todavía): un repo nuevo,
   puede llamarse `tuai-web` o como prefieras.
2. **Subir el contenido de esta carpeta** (`tuai-site/`) a la raíz del repo
   — ya sea arrastrando los archivos en la web de GitHub, o con `git push`
   si alguien del equipo maneja git.
3. En el repo: **Settings → Pages → Build and deployment → Source: "Deploy
   from a branch"**, elegir la rama `main` y la carpeta `/ (root)`.
   GitHub va a publicar el sitio en `https://<usuario>.github.io/<repo>/`
   en un par de minutos.
4. **Conectar el dominio `tuai.cl`**:
   - En el mismo panel de Pages, en "Custom domain" escribe `tuai.cl` (o
     `www.tuai.cl`) y guarda — esto crea automáticamente un archivo
     `CNAME` en el repo.
   - En el proveedor donde está registrado `tuai.cl` (NIC Chile o quien
     administre el DNS), hay que apuntar el dominio a GitHub Pages:
     - Si es el dominio raíz (`tuai.cl`): 4 registros `A` apuntando a
       `185.199.108.153`, `185.199.109.153`, `185.199.110.153` y
       `185.199.111.153`.
     - Si es un subdominio (`www.tuai.cl`): un registro `CNAME` apuntando
       a `<usuario>.github.io`.
   - Esto lo puedo dejar configurado yo mismo si me das acceso al repo de
     GitHub y a la administración DNS del dominio; si no, estos son los
     datos exactos para pasárselos a quien lo administre.

## Cómo se actualiza (cuando lleguen fotos, precios, specs reales)

Todo el contenido de cada propiedad vive en un solo lugar: la lista
`PROPERTIES` dentro de `build_site.py` (al principio del archivo). Cada
propiedad es un bloque independiente — agregar, quitar o editar una no
afecta a las demás.

Para regenerar el sitio después de editar los datos:

```bash
python3 build_site.py
```

Esto reescribe `index.html` y los 7 archivos de `propiedades/` con los
datos actualizados, manteniendo el mismo diseño. No hace falta tocar el
HTML a mano.

**La forma más simple:** envíame las fotos, precios y specs de cada
propiedad (puede ser propiedad por propiedad, no hace falta todo junto) y
yo actualizo `build_site.py` y vuelvo a generar el sitio.

## Pendiente de carga (honesto a propósito)

Todas las propiedades muestran "—" o "pendiente de carga" en vez de datos
inventados: fotos, precio, dormitorios/baños, resumen, plano, mapa, video
de YouTube y la simulación de crédito. Esto se actualiza propiedad por
propiedad a medida que llega la información real.
