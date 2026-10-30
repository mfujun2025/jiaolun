// ========== Header scroll effect ==========
const header = document.getElementById('header');
const backTop = document.getElementById('backTop');

window.addEventListener('scroll', () => {
  if (window.scrollY > 30) {
    header.classList.add('scrolled');
    backTop.classList.add('show');
  } else {
    header.classList.remove('scrolled');
    backTop.classList.remove('show');
  }
});

// ========== Mobile nav toggle ==========
const navToggle = document.getElementById('navToggle');
const navMenu = document.getElementById('navMenu');

navToggle.addEventListener('click', () => {
  navMenu.classList.toggle('open');
  // change icon
  navToggle.innerHTML = navMenu.classList.contains('open') ? '&#10005;' : '&#9776;';
});

// Close mobile nav when clicking a link
navMenu.querySelectorAll('a').forEach(link => {
  link.addEventListener('click', () => {
    navMenu.classList.remove('open');
    navToggle.innerHTML = '&#9776;';
  });
});

// ========== Back to top ==========
backTop.addEventListener('click', () => {
  window.scrollTo({ top: 0, behavior: 'smooth' });
});

// ========== Contact form ==========
const contactForm = document.getElementById('contactForm');
const formMsg = document.getElementById('formMsg');

if (contactForm) {
  contactForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const name = document.getElementById('name').value.trim();
    const phone = document.getElementById('phone').value.trim();
    const message = document.getElementById('message').value.trim();

    if (!name || !phone || !message) {
      alert('请填写必填项（姓名、电话、需求描述）');
      return;
    }

    // Simulate form submission (since this is a static site)
    formMsg.classList.add('show');
    contactForm.reset();

    setTimeout(() => {
      formMsg.classList.remove('show');
    }, 5000);
  });
}

// ========== Smooth scroll for anchor links ==========
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });
});
