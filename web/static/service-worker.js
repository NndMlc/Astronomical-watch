const CACHE_NAME = 'astrowatch-shell-v1';
const SHELL_ASSETS = [
  '/',
  '/static/index.html',
  '/static/app.js',
  '/static/manifest.webmanifest',
  '/static/icon-192.png',
  '/static/icon-512.png'
];

self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(SHELL_ASSETS))
  );
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then(keys => Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k))))
  );
});

self.addEventListener('fetch', (e) => {
  const url = new URL(e.request.url);
  if (url.pathname.startsWith('/api/')) {
    // Network first for API
    e.respondWith(
      fetch(e.request).catch(() => new Response(JSON.stringify({
        error: 'offline',
        note: 'No network; showing cached shell only'
      }), { headers: { 'Content-Type': 'application/json' } }))
    );
    return;
  }
  // Cache-first for shell/static
  e.respondWith(
    caches.match(e.request).then(cached => cached || fetch(e.request))
  );
});
