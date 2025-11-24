(() => {
  const anchorMap = {
    'gallery/01_basic_plots/index': '#basic-plots',
    'gallery/02_statistical_plots/index': '#statistical-plots',
    'gallery/03_bar_charts/index': '#bar-charts',
    'gallery/04_scientific_plots/index': '#scientific-plots',
    'gallery/05_time_series/index': '#time-series',
    'gallery/06_specialized_plots/index': '#specialized-plots',
    'gallery/07_layout_styling/index': '#layout-styling',
    'gallery/08_colors_images/index': '#colors-images',
  };

  const normalizeHref = (href) => {
    try {
      const url = new URL(href, window.location);
      let path = url.pathname.replace(/^\//, '');
      if (path.endsWith('/')) path = path.slice(0, -1);
      if (path.endsWith('.html')) path = path.slice(0, -5);
      return path;
    } catch (error) {
      return '';
    }
  };

  const scrollToAnchor = (anchor) => {
    const targetId = anchor.startsWith('#') ? anchor.slice(1) : anchor;
    const targetElement = document.getElementById(targetId);
    if (!targetElement) return false;

    targetElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
    history.replaceState(null, '', `#${targetId}`);
    return true;
  };

  const wireGallerySidebar = () => {
    const path = window.location.pathname;
    const isGalleryPage = path.endsWith('examples_gallery.html') || path.endsWith('examples_gallery/') || path.endsWith('examples_gallery');
    if (!isGalleryPage) return;

  const removeColorsImagesToggle = () => {
    const sidebar = document.querySelector('.globaltoc');
    if (!sidebar) return;

    const colorsLink =
      sidebar.querySelector('a.reference.internal[href="#colors-images"]') ||
      sidebar.querySelector('a.reference.internal[href$="gallery/08_colors_images/index.html"]');
    if (!colorsLink) return;

    const parentItem = colorsLink.closest('li');
    if (!parentItem) return;

    // Remove duplicated child tree so the theme stops rendering an expand/collapse control.
    const childList = Array.from(parentItem.children).find((node) => node.tagName === 'UL');
    if (childList) {
      childList.remove();
    }

    const toggleButtons = parentItem.querySelectorAll('button, .toctree-toggle');
    toggleButtons.forEach((button) => {
      if (button.closest('li') === parentItem) {
        button.remove();
      }
    });

    parentItem.removeAttribute('data-has-children');
    parentItem.classList.remove('has-children');
  };

    const links = document.querySelectorAll('.globaltoc a.reference.internal');
    links.forEach((link) => {
      const href = link.getAttribute('href');
      if (!href) return;

      const normalized = normalizeHref(href);
      const anchor = anchorMap[normalized];
      if (!anchor) return;

      link.setAttribute('href', anchor);
      link.addEventListener('click', (event) => {
        if (scrollToAnchor(anchor)) {
          event.preventDefault();
        }
      });
    });

    if (window.location.hash) {
      scrollToAnchor(window.location.hash);
    }

  removeColorsImagesToggle();
  };

  document.addEventListener('DOMContentLoaded', wireGallerySidebar);
})();
