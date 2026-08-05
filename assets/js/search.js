(function () {
  'use strict';

  var overlay = document.getElementById('search-overlay');
  var dialog = document.getElementById('search-dialog');
  var openBtn = document.getElementById('search-toggle');
  var closeBtn = document.getElementById('search-close');
  var input = document.getElementById('search-input');
  var resultsEl = document.getElementById('search-results');
  var statusEl = document.getElementById('search-status');

  if (!overlay || !openBtn || !input || !resultsEl) return;

  var searchDataUrl = overlay.getAttribute('data-search-index');
  var idx = null;
  var docs = null;
  var loadPromise = null;
  var activeIndex = -1;
  var lastFocused = null;
  var debounceTimer = null;

  function escapeHtml(str) {
    return str.replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  function buildDocsFromPage(page) {
    var container = document.createElement('div');
    container.innerHTML = page.html;
    var pageDocs = [];
    var currentHeading = page.title;
    var currentId = '';
    var buffer = [];

    function flush() {
      var text = buffer.join(' ').replace(/\s+/g, ' ').trim();
      if (text) {
        pageDocs.push({
          url: page.url + (currentId ? '#' + currentId : ''),
          title: page.title,
          heading: currentHeading,
          text: text
        });
      }
      buffer = [];
    }

    Array.prototype.forEach.call(container.children, function (el) {
      if (/^H[1-4]$/.test(el.tagName)) {
        flush();
        currentHeading = el.textContent.trim();
        currentId = el.id || '';
      } else {
        var t = el.textContent.trim();
        if (t) buffer.push(t);
      }
    });
    flush();
    return pageDocs;
  }

  function loadIndex() {
    if (loadPromise) return loadPromise;
    loadPromise = fetch(searchDataUrl)
      .then(function (res) { return res.json(); })
      .then(function (pages) {
        docs = [];
        pages.forEach(function (page) {
          buildDocsFromPage(page).forEach(function (d) { docs.push(d); });
        });
        idx = lunr(function () {
          this.ref('id');
          this.field('title', { boost: 10 });
          this.field('heading', { boost: 5 });
          this.field('text');
          docs.forEach(function (doc, i) {
            doc.id = String(i);
            this.add(doc);
          }, this);
        });
      })
      .catch(function (err) {
        statusEl.textContent = 'Search index failed to load.';
        idx = null;
      });
    return loadPromise;
  }

  function renderResults(matches) {
    resultsEl.innerHTML = '';
    activeIndex = -1;

    if (!matches.length) {
      resultsEl.hidden = true;
      statusEl.textContent = input.value.trim() ? 'No results.' : '';
      return;
    }

    matches.slice(0, 20).forEach(function (m) {
      var doc = docs[Number(m.ref)];
      var li = document.createElement('li');
      var a = document.createElement('a');
      a.href = doc.url;
      a.className = 'search-result';
      var snippet = doc.text.length > 140 ? doc.text.slice(0, 140).trim() + '…' : doc.text;
      var headingLine = doc.heading && doc.heading !== doc.title
        ? '<span class="search-result-heading">' + escapeHtml(doc.title) + ' › ' + escapeHtml(doc.heading) + '</span>'
        : '<span class="search-result-heading">' + escapeHtml(doc.title) + '</span>';
      a.innerHTML = headingLine + '<span class="search-result-snippet">' + escapeHtml(snippet) + '</span>';
      li.appendChild(a);
      resultsEl.appendChild(li);
    });

    resultsEl.hidden = false;
    statusEl.textContent = matches.length + ' result' + (matches.length === 1 ? '' : 's') + '.';
  }

  function runSearch(query) {
    if (!idx || !query) {
      renderResults([]);
      return;
    }
    var terms = query.trim().split(/\s+/).filter(Boolean).map(function (t) {
      return t.replace(/[^\w-]/g, '') + (t.length > 2 ? '*' : '');
    }).filter(Boolean);
    if (!terms.length) {
      renderResults([]);
      return;
    }
    var matches = [];
    try {
      matches = idx.search(terms.join(' '));
    } catch (e) {
      matches = [];
    }
    renderResults(matches);
  }

  function onInput() {
    clearTimeout(debounceTimer);
    var value = input.value;
    debounceTimer = setTimeout(function () {
      loadIndex().then(function () { runSearch(value); });
    }, 100);
  }

  function moveActive(delta) {
    var items = resultsEl.querySelectorAll('.search-result');
    if (!items.length) return;
    if (activeIndex === -1 && delta === -1) activeIndex = items.length;
    activeIndex = (activeIndex + delta + items.length) % items.length;
    items.forEach(function (el, i) {
      el.classList.toggle('is-active', i === activeIndex);
      if (i === activeIndex) el.scrollIntoView({ block: 'nearest' });
    });
    items[activeIndex].focus({ preventScroll: true });
  }

  function openSearch() {
    lastFocused = document.activeElement;
    overlay.hidden = false;
    document.body.classList.add('search-open');
    input.value = '';
    resultsEl.innerHTML = '';
    resultsEl.hidden = true;
    statusEl.textContent = '';
    openBtn.setAttribute('aria-expanded', 'true');
    loadIndex();
    input.focus();
    document.addEventListener('keydown', onDialogKeydown, true);
  }

  function closeSearch() {
    overlay.hidden = true;
    document.body.classList.remove('search-open');
    openBtn.setAttribute('aria-expanded', 'false');
    document.removeEventListener('keydown', onDialogKeydown, true);
    if (lastFocused && typeof lastFocused.focus === 'function') lastFocused.focus();
  }

  function onDialogKeydown(e) {
    if (e.key === 'Escape') {
      e.preventDefault();
      closeSearch();
      return;
    }
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      moveActive(1);
      return;
    }
    if (e.key === 'ArrowUp') {
      e.preventDefault();
      moveActive(-1);
      return;
    }
    if (e.key === 'Tab') {
      var focusable = [input].concat(
        Array.prototype.slice.call(resultsEl.querySelectorAll('.search-result'))
      );
      var first = focusable[0];
      var last = focusable[focusable.length - 1];
      if (e.shiftKey && document.activeElement === first) {
        e.preventDefault();
        last.focus();
      } else if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault();
        first.focus();
      }
    }
  }

  openBtn.addEventListener('click', function () {
    if (overlay.hidden) openSearch(); else closeSearch();
  });
  if (closeBtn) closeBtn.addEventListener('click', closeSearch);
  overlay.addEventListener('click', function (e) {
    if (e.target === overlay) closeSearch();
  });
  input.addEventListener('input', onInput);
  input.addEventListener('keydown', function (e) {
    if (e.key === 'Enter' && activeIndex === -1) {
      var first = resultsEl.querySelector('.search-result');
      if (first) window.location.href = first.getAttribute('href');
    }
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === '/' && overlay.hidden) {
      var tag = (document.activeElement && document.activeElement.tagName) || '';
      if (tag === 'INPUT' || tag === 'TEXTAREA' || document.activeElement.isContentEditable) return;
      e.preventDefault();
      openSearch();
    }
  });
})();
