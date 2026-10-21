(function(){
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
