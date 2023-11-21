// -------------------------- start --------------------------
$(document).ready(function() {
  const mobileMenu = document.getElementById('css-mobile-menu');
  const navList = document.querySelector('.css-nav-list');
  // const homeButton = document.getElementById('css-home-button');

  mobileMenu.addEventListener('click', () => {
    mobileMenu.classList.toggle('css-show');
    navList.classList.toggle('css-show');
    // homeButton.classList.toggle('uiSearchItemInvisible');
  });
});
// -------------------------- end --------------------------
