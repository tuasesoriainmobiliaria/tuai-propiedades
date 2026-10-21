(function(){
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
