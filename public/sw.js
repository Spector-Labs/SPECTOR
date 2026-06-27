/* Spector service worker — offline shell for installed PWA rehearsal */
const CACHE = 'spector-v6';
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

/* Stable-URL, mutable-content assets (style.css, manifest.json, any js) must stay
   in lock-step with the freshly-fetched HTML, so serve them network-first too.
   Otherwise a fresh HTML page can paint against a stale cached stylesheet (FOUC). */
function isNetworkFirstAsset(pathname) {
    return /\.(css|js|json)$/.test(pathname);
}

async function matchCached(path) {
    const abs = assetUrl(path);
    return (await caches.match(abs))
        || (await caches.match(path))
        || (await caches.match('./' + path.replace(/^\//, '')));
}

/** Network-first with cache fallback. Used for HTML shells AND css/js/json so
   copy + style updates always propagate together and never skew (FOUC fix).
   `fallbackPath` lets shells fall back to their cached app shell when offline. */
async function networkFirst(request, fallbackPath) {
    try {
        const res = await fetch(request);
        if (res && res.status === 200 && res.type !== 'opaque') {
            const clone = res.clone();
            caches.open(CACHE).then((c) => c.put(request, clone));
        }
        return res;
    } catch (err) {
        const fallback = (await caches.match(request)) || (fallbackPath && await matchCached(fallbackPath));
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
            return networkFirst(e.request, shellPath);
        }

        // style.css / js / json: network-first so they never skew against fresh HTML
        if (url.origin === ORIGIN && isNetworkFirstAsset(url.pathname)) {
            return networkFirst(e.request, null);
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
