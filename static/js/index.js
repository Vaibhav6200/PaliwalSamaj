const swiper = new Swiper(".mySwiper", {
  slidesPerView: 3,
  spaceBetween: 24,
  loop: true,
  autoplay: {
    delay: 4000,
    disableOnInteraction: false,
    pauseOnMouseEnter: true,
  },
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
  },
  breakpoints: {
    992: { slidesPerView: 3 },
    768: { slidesPerView: 2 },
    0:   { slidesPerView: 1 },
  },
});

// Active URL
document.addEventListener("DOMContentLoaded", function () {
  const currentUrl = window.location.pathname; // gets path like /en/news_and_events/
  const navLinks = document.querySelectorAll(".nav-item a");

  navLinks.forEach(link => {
    const linkPath = new URL(link.href).pathname;

    if (currentUrl === linkPath || (currentUrl === '/' && linkPath === '/en/')) {
      link.closest('.nav-item').classList.add('active');
    } else {
      link.closest('.nav-item').classList.remove('active');
    }
  });
});

 document.addEventListener("DOMContentLoaded", function () {
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.forEach(function (el) {
      new bootstrap.Popover(el, {
        trigger: 'hover',
        placement: 'top', // or 'auto', 'bottom', etc.
        delay: { "show": 100, "hide": 100 },
      });
    });
  });
