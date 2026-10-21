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
    var shortEl = document.getElementById('fichaResumenShort');
    var fullEl = document.getElementById('fichaResumenFull');
    var textEl = document.getElementById('fichaResumenToggleText');
    var iconEl = document.getElementById('fichaResumenToggleIcon');
    toggleBtn.addEventListener('click', function(){
      var expanded = fullEl.style.display !== 'none';
      if (expanded) {
        fullEl.style.display = 'none';
        shortEl.style.display = '-webkit-box';
        textEl.textContent = 'Leer más';
        iconEl.style.transform = 'rotate(0deg)';
      } else {
        shortEl.style.display = 'none';
        fullEl.style.display = 'block';
        textEl.textContent = 'Leer menos';
        iconEl.style.transform = 'rotate(180deg)';
      }
    });
  }
})();
