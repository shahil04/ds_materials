function toggleMenu() {
  const nav = document.getElementById("navLinks");
  nav.classList.toggle("show");
}
 
// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(link => {
  link.addEventListener('click', function (e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      target.scrollIntoView({ behavior: 'smooth' });
    }
  });
});
 
// Highlight active nav link
window.addEventListener("scroll", () => {
  const sections = document.querySelectorAll("section");
  const navLinks = document.querySelectorAll(".nav-links a");
  let current = "";
 
  sections.forEach(section => {
    const sectionTop = section.offsetTop;
    const sectionHeight = section.clientHeight;
    if (pageYOffset >= sectionTop - sectionHeight / 3) {
      current = section.getAttribute("id");
    }
  });
 
  navLinks.forEach(link => {
    link.classList.remove("active");
    if (link.getAttribute("href") === `#${current}`) {
      link.classList.add("active");
    }
  });
});
 
// Scroll-to-top button
const scrollBtn = document.getElementById("scrollTopBtn");
 
window.onscroll = function () {
  scrollBtn.style.display = window.scrollY > 400 ? "block" : "none";
};
 
scrollBtn.onclick = function () {
  window.scrollTo({ top: 0, behavior: "smooth" });
};
 
// Toggle hamburger menu
const hamburger = document.getElementById("hamburger");
const navLinks = document.getElementById("navLinks");
 
hamburger.addEventListener("click", () => {
  navLinks.classList.toggle("active");
});
 
 