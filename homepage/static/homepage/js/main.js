// Текущий год в подвале сайта
const yearElement = document.getElementById("current-year");
if (yearElement) {
  yearElement.textContent = new Date().getFullYear();
}

// Подсветка активного пункта меню
document.querySelectorAll(".site-nav .nav-link").forEach((link) => {
  const path = window.location.pathname;
  const href = link.getAttribute("href");
  if (href === path || (href !== "/" && path.startsWith(href))) {
    link.classList.add("active", "fw-bold");
  }
});
