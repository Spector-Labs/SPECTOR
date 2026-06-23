/* Spector service worker — offline shell for installed PWA rehearsal */
const CACHE = 'spector-v2';
const ASSETS = ['./', './index.html', './app.html', './style.css', './manifest.json'];

self.addEventListener('install', (e) => {
    e.waitUntil(caches.open(CACHE).then(c => c.addAll(ASSETS)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', (e) => {
    e.waitUntil(
        caches.keys().then(keys =>
            Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
        ).then(() => self.clients.claim())
    );
});

function shellForPath(pathname) {
    if (pathname.endsWith('app.html')) return './app.html';
    if (pathname.endsWith('index.html') || pathname === '/' || pathname.endsWith('/')) return './index.html';
    return null;
}

self.addEventListener('fetch', (e) => {
    if (e.request.method !== 'GET') return;
    const url = new URL(e.request.url);

    e.respondWith((async () => {
        const exact = await caches.match(e.request);
        if (exact) return exact;

        const shellKey = shellForPath(url.pathname);
        if (shellKey) {
            const shell = await caches.match(shellKey) || await caches.match('app.html') || await caches.match('index.html');
            if (shell) return shell;
        }

        try {
            const res = await fetch(e.request);
            if (res && res.status === 200 && res.type !== 'opaque') {
                const clone = res.clone();
                caches.open(CACHE).then(c => c.put(e.request, clone));
            }
            return res;
        } catch (err) {
            if (shellKey) {
                const fallback = await caches.match(shellKey);
                if (fallback) return fallback;
            }
            return new Response('Offline — open Spector while online first.', { status: 503, statusText: 'Offline' });
        }
    })());
});