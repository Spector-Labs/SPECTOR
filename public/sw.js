/* Spector service worker — offline shell for installed PWA rehearsal */
const CACHE = 'spector-v4';
const ORIGIN = self.location.origin;

function assetUrl(path) {
    if (path.startsWith('http')) return path;
    const normalized = path.startsWith('/') ? path : '/' + path.replace(/^\.\//, '');
    return ORIGIN + normalized;
}

const ASSETS = [
    '/index.html',
    '/app.html',
    '/style.css',
    '/manifest.json',
    '/verify-sw.html',
    '/sw-prime.html',
];

self.addEventListener('install', (e) => {
    e.waitUntil(
        caches.open(CACHE).then(async (cache) => {
            for (const path of ASSETS) {
                try {
                    await cache.add(assetUrl(path));
                } catch (_) { /* best-effort per asset */ }
            }
        }).then(() => self.skipWaiting())
    );
});

self.addEventListener('activate', (e) => {
    e.waitUntil(
        caches.keys()
            .then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
            .then(() => self.clients.claim())
    );
});

function shellPathFor(pathname) {
    if (pathname.endsWith('app.html')) return '/app.html';
    if (pathname.endsWith('index.html') || pathname === '/' || pathname.endsWith('/')) return '/index.html';
    return null;
}

async function matchCached(path) {
    const abs = assetUrl(path);
    return (await caches.match(abs))
        || (await caches.match(path))
        || (await caches.match('./' + path.replace(/^\//, '')));
}

/** HTML shells: network-first when online so copy updates (e.g. landing text) propagate. */
async function networkFirstShell(request, shellPath) {
    try {
        const res = await fetch(request);
        if (res && res.status === 200 && res.type !== 'opaque') {
            const clone = res.clone();
            caches.open(CACHE).then((c) => c.put(request, clone));
        }
        return res;
    } catch (err) {
        const fallback = await matchCached(shellPath);
        if (fallback) return fallback;
        return new Response('Offline — open Spector while online first.', { status: 503, statusText: 'Offline' });
    }
}

self.addEventListener('fetch', (e) => {
    if (e.request.method !== 'GET') return;
    const url = new URL(e.request.url);
    const shellPath = shellPathFor(url.pathname);

    e.respondWith((async () => {
        if (shellPath) {
            return networkFirstShell(e.request, shellPath);
        }

        const exact = await caches.match(e.request);
        if (exact) return exact;

        try {
            const res = await fetch(e.request);
            if (res && res.status === 200 && res.type !== 'opaque') {
                const clone = res.clone();
                caches.open(CACHE).then((c) => c.put(e.request, clone));
            }
            return res;
        } catch (err) {
            return new Response('Offline — open Spector while online first.', { status: 503, statusText: 'Offline' });
        }
    })());
});