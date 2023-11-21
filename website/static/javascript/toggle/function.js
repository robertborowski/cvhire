// -------------------------- start --------------------------
$(document).ready(function() {
  const mobileMenu = document.getElementById('css-mobile-menu');
  const navList = document.querySelector('.css-nav-list');

  mobileMenu.addEventListener('click', () => {
    mobileMenu.classList.toggle('css-show');
    navList.classList.toggle('css-show');
  });
});
// -------------------------- end --------------------------
