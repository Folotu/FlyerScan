// // This is the "Offline page" service worker

// importScripts('https://storage.googleapis.com/workbox-cdn/releases/5.1.2/workbox-sw.js');

// const CACHE = "pwabuilder-page";

// // TODO: replace the following with the correct offline fallback page i.e.: const offlineFallbackPage = "offline.html";
// const offlineFallbackPage = "/static/offline.html";

// self.addEventListener("message", (event) => {
//   if (event.data && event.data.type === "SKIP_WAITING") {
//     self.skipWaiting();
//   }
// });

// self.addEventListener('install', async (event) => {
//   event.waitUntil(
//     caches.open(CACHE)
//       .then((cache) => cache.add(offlineFallbackPage))
//   );
// });

// if (workbox.navigationPreload.isSupported()) {
//   workbox.navigationPreload.enable();
// }

// self.addEventListener('fetch', (event) => {
//   if (event.request.mode === 'navigate') {
//     event.respondWith((async () => {
//       try {
//         const preloadResp = await event.preloadResponse;

//         if (preloadResp) {
//           return preloadResp;
//         }

//         const networkResp = await fetch(event.request);
//         return networkResp;
//       } catch (error) {

//         const cache = await caches.open(CACHE);
//         const cachedResp = await cache.match(offlineFallbackPage);
//         return cachedResp;
//       }
//     })());
//   }
// });






const cacheName = 'flask-PWA-v3';
const filesToCache = [
    '/',
    '/static/js/index.js',
    // '/static/styles.css',
    // '/static/images/pwa-light.png'
];





self.addEventListener('install', function(e) {
  console.log('[ServiceWorker] Install');
  e.waitUntil(
    caches.open(cacheName).then(function(cache) {
      console.log('[ServiceWorker] Caching app shell');
      return cache.addAll(filesToCache);
    })
  );
});






self.addEventListener('activate', function(e) {
  console.log('[ServiceWorker] Activate');
    e.waitUntil(
    caches.keys().then(function(keyList) {
      return Promise.all(keyList.map(function(key) {
        if (key !== cacheName) {
          console.log('[ServiceWorker] Removing old cache', key);
          return caches.delete(key);
        }
      }));
    })
  );
  return self.clients.claim();
});






self.addEventListener('fetch', function(e) {
  console.log('[ServiceWorker] Fetch', e.request.url);
  e.respondWith(
    caches.match(e.request).then(function(response) {
      return response || fetch(e.request).catch(error => {
          console.log('Fetch failed; returning offline page instead.', error);
          let url = e.request.url;
          let extension = url.split('.').pop();

          if (extension === 'jpg' || extension === 'png') {

              const FALLBACK_IMAGE = `<svg xmlns="http://www.w3.org/2000/svg" width="200" height="180" stroke-linejoin="round">
                <path stroke="#DDD" stroke-width="25" d="M99,18 15,162H183z"/>
                <path stroke-width="17" fill="#FFF" d="M99,18 15,162H183z" stroke="#eee"/>
                <path d="M91,70a9,9 0 0,1 18,0l-5,50a4,4 0 0,1-8,0z" fill="#aaa"/>
                <circle cy="138" r="9" cx="100" fill="#aaa"/>
                </svg>`;

              return Promise.resolve(new Response(FALLBACK_IMAGE, {
                  headers: {
                      'Content-Type': 'image/svg+xml'
                  }
              }));
          }

          return caches.match('offline.html');
      });
    })
  );
});