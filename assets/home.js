(function(){
  // ---------- Hero: toggle propietario / buscador ----------
  var heroContent = {
    propietario: {
      eyebrow: 'Para dueños que quieren vender o arrendar',
      titulo: 'Vende o arrienda tu propiedad con una persona, sin perder el tiempo con un chatbot.',
      sub: 'Tasación, difusión, visitas y cierre — coordinados por nuestro equipo de principio a fin.',
      ctaLabel: 'Quiero arrendar mi propiedad',
      ctaHref: 'https://wa.me/56998383991?text=' + encodeURIComponent('Hola, quiero vender/arrendar mi propiedad. ¿Me ayudan con la tasación?'),
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
          : placeholderHtml.replace(/<span class="tag[^]*?<\/span>/, '')) + tagHtml;
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
      ].filter(Boolean).join('\n');
      var waUrl = 'https://wa.me/56998383991?text=' + encodeURIComponent(texto);

      var mailSubject = 'Nueva consulta web — ' + data.interes;
      var mailBody = [
        'Nombre: ' + data.nombre,
        'Teléfono: ' + data.telefono,
        'Correo: ' + data.email,
        'Interés: ' + data.interes,
        data.mensaje ? ('Mensaje: ' + data.mensaje) : null
      ].filter(Boolean).join('\n');
      var mailUrl = 'mailto:tuasesoriainmobiliariacl@gmail.com?subject=' + encodeURIComponent(mailSubject) + '&body=' + encodeURIComponent(mailBody);

      document.getElementById('submittedName').textContent = '¡Gracias, ' + data.nombre + '!';
      document.getElementById('submittedMsg').classList.remove('hidden');
      window.open(waUrl, '_blank', 'noopener');
      window.location.href = mailUrl;
    });
  }
})();
