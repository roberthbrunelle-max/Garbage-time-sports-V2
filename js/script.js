/**
 * GARBAGE TIME SPORTS — script.js
 * All interactive functionality for the site.
 * ============================================
 */

'use strict';

/* ============================================
   DROPDOWN NAVIGATION
   ============================================ */
function initDropdowns() {
  const dropdowns = document.querySelectorAll('.nav-dropdown');

  dropdowns.forEach(dropdown => {
    const btn = dropdown.querySelector('button');

    // Toggle on click
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const isOpen = dropdown.classList.contains('open');
      // Close all dropdowns first
      dropdowns.forEach(d => d.classList.remove('open'));
      if (!isOpen) dropdown.classList.add('open');
    });
  });

  // Close dropdowns when clicking outside
  document.addEventListener('click', () => {
    dropdowns.forEach(d => d.classList.remove('open'));
  });

  // Close on Escape
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') dropdowns.forEach(d => d.classList.remove('open'));
  });
}

/* ============================================
   MOBILE MENU
   ============================================ */
function initMobileMenu() {
  const hamburger = document.querySelector('.nav-hamburger');
  const mobileMenu = document.querySelector('.mobile-menu');
  if (!hamburger || !mobileMenu) return;

  hamburger.addEventListener('click', () => {
    const isOpen = hamburger.classList.toggle('open');
    mobileMenu.classList.toggle('open', isOpen);
    document.body.style.overflow = isOpen ? 'hidden' : '';
  });

  // Close when clicking a link
  mobileMenu.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
      hamburger.classList.remove('open');
      mobileMenu.classList.remove('open');
      document.body.style.overflow = '';
    });
  });
}

/* ============================================
   SCROLL FADE-IN ANIMATIONS
   ============================================ */
function initFadeIn() {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry, i) => {
        if (entry.isIntersecting) {
          // Stagger delay based on sibling index within grid
          const siblings = entry.target.parentElement?.children;
          let delay = 0;
          if (siblings) {
            const idx = Array.from(siblings).indexOf(entry.target);
            delay = Math.min(idx * 80, 400); // max 400ms stagger
          }
          setTimeout(() => {
            entry.target.classList.add('visible');
          }, delay);
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.1, rootMargin: '0px 0px -40px 0px' }
  );

  document.querySelectorAll('.fade-in').forEach(el => observer.observe(el));
}

/* ============================================
   STICKY NAVBAR — shrink on scroll
   ============================================ */
function initStickyNav() {
  const navbar = document.querySelector('.navbar');
  if (!navbar) return;

  let lastScroll = 0;
  window.addEventListener('scroll', () => {
    const currentScroll = window.scrollY;
    // Add scrolled class for subtle style change
    navbar.classList.toggle('scrolled', currentScroll > 60);
    lastScroll = currentScroll;
  }, { passive: true });
}

/* ============================================
   ARTICLE FILTER BUTTONS
   ============================================ */
function initFilters() {
  const filterBtns = document.querySelectorAll('.filter-btn');
  const cards = document.querySelectorAll('.article-card[data-category]');
  if (!filterBtns.length) return;

  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      // Update active button
      filterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      const filter = btn.dataset.filter;

      cards.forEach(card => {
        if (filter === 'all' || card.dataset.category === filter) {
          card.style.display = '';
          // Re-trigger fade animation
          card.classList.remove('visible');
          setTimeout(() => card.classList.add('visible'), 50);
        } else {
          card.style.display = 'none';
        }
      });
    });
  });
}

/* ============================================
   LOAD MORE BUTTON
   ============================================ */
function initLoadMore() {
  const loadMoreBtn = document.querySelector('.btn-load-more');
  if (!loadMoreBtn) return;

  // All hidden cards start with display:none via JS (added after page load)
  const allCards = document.querySelectorAll('.article-card[data-hidden="true"]');
  allCards.forEach(card => card.style.display = 'none');

  let shown = false;

  loadMoreBtn.addEventListener('click', () => {
    if (!shown) {
      allCards.forEach(card => {
        card.style.display = '';
        card.classList.remove('visible');
        setTimeout(() => card.classList.add('visible'), 100);
      });
      loadMoreBtn.textContent = 'That\'s All, Folks.';
      loadMoreBtn.disabled = true;
      loadMoreBtn.style.opacity = '0.4';
      shown = true;
    }
  });
}

/* ============================================
   NEWS TICKER — duplicate for seamless loop
   ============================================ */
function initTicker() {
  const track = document.querySelector('.ticker-track');
  if (!track) return;
  // Duplicate content for seamless CSS animation loop
  const clone = track.cloneNode(true);
  track.parentElement.appendChild(clone);
}

/* ============================================
   SMOOTH SCROLL for anchor links
   ============================================ */
function initSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', (e) => {
      const target = document.querySelector(anchor.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });
}

/* ============================================
   NEWSLETTER FORM
   ============================================ */
function initNewsletter() {
  document.querySelectorAll('.newsletter-input-row').forEach(form => {
    const btn = form.querySelector('button');
    const input = form.querySelector('input');
    if (!btn || !input) return;

    btn.addEventListener('click', () => {
      const email = input.value.trim();
      if (!email || !email.includes('@')) {
        input.style.borderColor = 'var(--red)';
        input.focus();
        setTimeout(() => (input.style.borderColor = ''), 1500);
        return;
      }
      btn.textContent = '✓ Subscribed!';
      btn.style.background = '#00cc88';
      input.value = '';
      input.disabled = true;
      btn.disabled = true;
    });
  });
}

/* ============================================
   ACTIVE NAV LINK — highlight current page
   ============================================ */
function initActiveNav() {
  const currentPage = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-links a, .dropdown-menu a, .mobile-menu a').forEach(link => {
    const href = link.getAttribute('href');
    if (href && (href === currentPage || (currentPage === '' && href === 'index.html'))) {
      link.classList.add('active');
    }
  });
}

/* ============================================
   INIT ALL
   ============================================ */
document.addEventListener('DOMContentLoaded', () => {
  initDropdowns();
  initMobileMenu();
  initFadeIn();
  initStickyNav();
  initFilters();
  initLoadMore();
  initTicker();
  initSmoothScroll();
  initNewsletter();
  initActiveNav();

  console.log('🗑️ Garbage Time Sports — loaded.');
});
