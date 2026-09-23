(() => {

gsap.registerPlugin(ScrollTrigger);

const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

const menuToggle = document.querySelector('[data-menu-toggle]');
const mobileNav = document.querySelector('[data-mobile-nav]');

menuToggle?.addEventListener('click', () => {
  const open = menuToggle.getAttribute('aria-expanded') === 'true';
  menuToggle.setAttribute('aria-expanded', String(!open));
  mobileNav?.classList.toggle('is-open', !open);
});

mobileNav?.querySelectorAll('a').forEach((link) => {
  link.addEventListener('click', () => {
    menuToggle?.setAttribute('aria-expanded', 'false');
    mobileNav?.classList.remove('is-open');
  });
});

if (!reduceMotion) {
  const lenis = new Lenis({ duration: 1.05, smoothWheel: true, wheelMultiplier: 0.9 });
  lenis.on('scroll', ScrollTrigger.update);
  gsap.ticker.add((time) => lenis.raf(time * 1000));
  gsap.ticker.lagSmoothing(0);

  const heroTl = gsap.timeline({
    scrollTrigger: {
      trigger: '[data-hero]',
      start: 'top top',
      end: '+=150%',
      scrub: 1,
      pin: true,
      anticipatePin: 1
    }
  });

  heroTl
    .to('[data-frame="a"]', { xPercent: -24, yPercent: 10, scale: 0.72, ease: 'none' }, 0)
    .to('[data-frame="b"]', { xPercent: 0, yPercent: -6, scale: 0.58, ease: 'none' }, 0)
    .to('[data-frame="c"]', { xPercent: 27, yPercent: 12, scale: 0.72, ease: 'none' }, 0)
    .to('[data-hero-title]', { scale: 1.18, yPercent: -6, ease: 'none' }, 0)
    .to('.hero-intro', { opacity: 0.15, y: 35, ease: 'none' }, 0.15)
    .to('.hero-bottom', { opacity: 0, ease: 'none' }, 0.45);

  gsap.from('[data-frame="a"], [data-frame="c"]', {
    opacity: 0,
    y: 50,
    duration: 1,
    stagger: 0.12,
    ease: 'power3.out'
  });

  gsap.from('[data-frame="b"]', {
    opacity: 0,
    scale: 0.75,
    duration: 1.25,
    ease: 'power3.out'
  });

  gsap.from('.hero-title-wrap > *', {
    opacity: 0,
    y: 35,
    duration: 0.95,
    stagger: 0.08,
    ease: 'power3.out'
  });

  const marquee = document.querySelector('[data-marquee]');
  if (marquee) {
    gsap.to(marquee, { xPercent: -50, duration: 24, repeat: -1, ease: 'none' });
  }

  gsap.utils.toArray('[data-reveal]').forEach((element) => {
    gsap.from(element, {
      opacity: 0,
      y: 50,
      duration: 0.9,
      ease: 'power3.out',
      scrollTrigger: { trigger: element, start: 'top 86%' }
    });
  });

  gsap.utils.toArray('[data-project-card]').forEach((card, index) => {
    const media = card.querySelector('.project-media');
    gsap.from(card, {
      opacity: 0,
      y: index % 2 === 0 ? 70 : 100,
      duration: 1,
      ease: 'power3.out',
      scrollTrigger: { trigger: card, start: 'top 88%' }
    });
    if (media) {
      gsap.to(media, {
        scale: 1.06,
        yPercent: -5,
        ease: 'none',
        scrollTrigger: { trigger: card, start: 'top bottom', end: 'bottom top', scrub: 1 }
      });
    }
  });

  const serviceFigure = document.querySelector('[data-service-figure]');
  const serviceRows = document.querySelectorAll('[data-service-row]');

  serviceRows.forEach((row) => {
    row.addEventListener('mouseenter', () => {
      const index = Number(row.dataset.serviceIndex || 0);
      serviceFigure?.setAttribute('data-active', String(index + 1));
      serviceRows.forEach((r) => r.classList.toggle('is-active', r === row));
    });
  });

  gsap.to('.china-orbit', {
    rotate: 360,
    ease: 'none',
    scrollTrigger: { trigger: '.china', start: 'top bottom', end: 'bottom top', scrub: 1.2 }
  });

  gsap.utils.toArray('.china-window').forEach((windowEl, index) => {
    gsap.fromTo(windowEl,
      { y: 120 + index * 25, opacity: 0.2, rotate: index % 2 === 0 ? -6 : 6 },
      {
        y: -40 - index * 12,
        opacity: 1,
        rotate: index % 2 === 0 ? 2 : -2,
        ease: 'none',
        scrollTrigger: { trigger: '.china', start: 'top 85%', end: 'bottom 15%', scrub: 1.1 }
      }
    );
  });

  gsap.utils.toArray('[data-process-card]').forEach((card, index) => {
    gsap.from(card, {
      opacity: 0,
      y: 55,
      rotate: index % 2 === 0 ? -1.5 : 1.5,
      duration: 0.85,
      ease: 'power3.out',
      scrollTrigger: { trigger: card, start: 'top 90%' }
    });
  });
}

})();