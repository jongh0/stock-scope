/* ============================================================
   sw.js - StockScope Service Worker (PWA)
   ============================================================ */

const CACHE_NAME = 'stock-scope-v1';
const STATIC_ASSETS = [
  './',
  './index.html',
  './manifest.json',
  './css/style.css',
  './js/config.js',
  './js/sparkline.js',
  './js/app.js',
  './icons/icon.svg',
  './icons/icon-192.png',
  './icons/icon-512.png'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(STATIC_ASSETS))
  );
  self.skipWaiting();
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(
        keys
          .filter(key => key !== CACHE_NAME)
          .map(key => caches.delete(key))
      )
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', event => {
  const { request } = event;
  if (request.method !== 'GET') return;

  const url = new URL(request.url);
  if (url.origin !== self.location.origin) return;

  // data/stocks.json: Network-first (최신 데이터 우선, 오프라인 시 캐시 폴백)
  if (url.pathname.endsWith('/data/stocks.json')) {
    const cleanUrl = new URL(url.pathname, url.origin).href;
    event.respondWith(
      fetch(request)
        .then(response => {
          if (response.ok) {
            const clone = response.clone();
            caches.open(CACHE_NAME).then(cache => cache.put(cleanUrl, clone));
          }
          return response;
        })
        .catch(() => caches.match(cleanUrl))
    );
    return;
  }

  // 정적 리소스: Network-first with Cache fallback (항상 최신 UI 유지 및 오프라인 지원)
  event.respondWith(
    fetch(request)
      .then(response => {
        if (response.ok) {
          const clone = response.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(request, clone));
        }
        return response;
      })
      .catch(() => caches.match(request, { ignoreSearch: true }))
  );
});
