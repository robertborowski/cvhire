// -------------------------- start --------------------------
$(document).ready(function() {
  const mobileMenu = document.getElementById('custom-mobile-menu');
  const navList = document.querySelector('.custom-nav-list');
  const homeButton = document.getElementById('custom-home-button');

  mobileMenu.addEventListener('click', () => {
    mobileMenu.classList.toggle('custom-show');
    navList.classList.toggle('custom-show');
    homeButton.classList.toggle('uiSearchItemInvisible');
  });
});
// -------------------------- end --------------------------
