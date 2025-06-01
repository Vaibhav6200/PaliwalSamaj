const swiper = new Swiper(".mySwiper", {
  slidesPerView: 3,
  spaceBetween: 20,
  loop: true,
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
  },
  breakpoints: {
    992: { slidesPerView: 3 }, // Desktop
    768: { slidesPerView: 2 }, // Tablet
    0: { slidesPerView: 1 },   // Mobile
  },
});
