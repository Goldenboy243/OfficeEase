/* =============================================
   Microsoft Word Help & Learning – script.js
   ============================================= */

document.addEventListener('DOMContentLoaded', () => {

  // ─── Close promo banner ───
  const closeBanner = document.getElementById('close-banner');
  const promoBanner = document.getElementById('promo-banner');

  if (closeBanner && promoBanner) {
    closeBanner.addEventListener('click', () => {
      promoBanner.style.transition = 'max-height 0.3s ease, opacity 0.3s ease, padding 0.3s ease';
      promoBanner.style.overflow = 'hidden';
      promoBanner.style.maxHeight = promoBanner.scrollHeight + 'px';

      requestAnimationFrame(() => {
        promoBanner.style.maxHeight = '0';
        promoBanner.style.opacity = '0';
        promoBanner.style.padding = '0';
      });

      setTimeout(() => promoBanner.remove(), 350);
    });
  }

  // ─── Search on Enter key ───
  const searchInput = document.querySelector('.hero-section input');
  const searchBtn = document.querySelector('.search-arrow');

  const handleSearch = () => {
    const query = searchInput ? searchInput.value.trim() : '';
    if (query) {
      alert(`Searching for: "${query}"\n\n(This is a demo – no real search performed)`);
    }
  };

  if (searchBtn) {
    searchBtn.addEventListener('click', handleSearch);
  }
  if (searchInput) {
    searchInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') handleSearch();
    });
  }

  // ─── Active category nav underline on click ───
  const catItems = document.querySelectorAll('.cat-item');

  catItems.forEach(item => {
    item.addEventListener('click', (e) => {
      e.preventDefault();
      catItems.forEach(i => i.classList.remove('active-cat'));
      item.classList.add('active-cat');
    });
  });

  // ─── Scroll reveal animation ───
  const revealElements = document.querySelectorAll(
    '.explore-card, .editor-section .grid > *, section h2, .trending-col'
  );

  // Add reveal class to target elements
  document.querySelectorAll('.explore-card').forEach(el => el.classList.add('reveal'));
  document.querySelectorAll('#trending-section .grid > div').forEach(el => el.classList.add('reveal'));

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry, i) => {
      if (entry.isIntersecting) {
        // Stagger sibling reveals
        const siblings = Array.from(entry.target.parentElement?.children || []);
        const idx = siblings.indexOf(entry.target);
        setTimeout(() => {
          entry.target.classList.add('visible');
        }, idx * 80);
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12 });

  document.querySelectorAll('.reveal').forEach(el => observer.observe(el));

  // ─── Play button: video placeholder ───
  document.querySelectorAll('.play-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      alert('▶  Video playback would start here.\n\n(Demo only)');
    });
  });

  // ─── Sticky header shadow on scroll ───
  const header = document.querySelector('header');
  window.addEventListener('scroll', () => {
    if (window.scrollY > 10) {
      header.style.boxShadow = '0 2px 8px rgba(0,0,0,0.12)';
    } else {
      header.style.boxShadow = '0 1px 0 #e5e5e5';
    }
  }, { passive: true });

  // ─── Active cat-item style injection ───
  const style = document.createElement('style');
  style.textContent = `
    .active-cat {
      color: #0067b8 !important;
    }
    .active-cat::after {
      transform: scaleX(1) !important;
    }
  `;
  document.head.appendChild(style);

});
