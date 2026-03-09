const CACHE_NAME = 'eg-simulator-v2';
const RUNTIME_CACHE = 'eg-simulator-runtime';
const urlsToCache = [
  '/',
  '/static/manifest.json'
];

// Install event - cache essential files
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('[Service Worker] Caching essential assets');
        return cache.addAll(urlsToCache);
      })
      .then(() => self.skipWaiting())
  );
});

// Activate event - clean up old caches
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME && cacheName !== RUNTIME_CACHE) {
            console.log('[Service Worker] Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// Fetch event - Network first, fallback to cache
self.addEventListener('fetch', event => {
  const { request } = event;
  const url = new URL(request.url);
  
  // Skip non-GET requests
  if (request.method !== 'GET') {
    return;
  }
  
  event.respondWith(
    fetch(request)
      .then(response => {
        // Cache successful responses
        if (response.ok && response.type === 'basic') {
          const responseToCache = response.clone();
          caches.open(RUNTIME_CACHE)
            .then(cache => cache.put(request, responseToCache));
        }
        return response;
      })
      .catch(() => {
        // Fallback to cache when offline
        return caches.match(request)
          .then(cachedResponse => {
            if (cachedResponse) {
              return cachedResponse;
            }
            // Return offline page or empty response
            return new Response('Offline - Page not available', {
              status: 503,
              statusText: 'Service Unavailable',
              headers: new Headers({
                'Content-Type': 'text/plain'
              })
            });
          });
      })
  );
});

// Background sync for future use
self.addEventListener('sync', event => {
  if (event.tag === 'sync-calculations') {
    event.waitUntil(
      // Handle background sync if needed
      Promise.resolve()
    );
  }
});

// Handle push notifications for future use
self.addEventListener('push', event => {
  const data = event.data ? event.data.json() : {};
  const options = {
    body: data.body || 'EG Simulator notification',
    icon: '/static/icon-192.png',
    badge: '/static/icon-192.png',
  };
  event.waitUntil(
    self.registration.showNotification(data.title || 'EG Simulator', options)
  );
});
