// サービスワーカー：一度開いたら、電波がなくてもアプリを開けるようにする仕組み。
// 中身（index.html や data.js）を更新したら、CACHE_NAME の番号を1つ上げてください。
// 番号が変わると、古い保存データが捨てられて新しい中身に入れ替わります。
const CACHE_NAME = "bttf88-v3";

// 最初に保存しておくファイル
const APP_FILES = [
  "./",
  "./index.html",
  "./data.js",
  "./manifest.webmanifest",
  "./icons/icon-192.png",
  "./icons/icon-512.png",
  "./icons/apple-touch-icon.png",
];

// インストール時：ファイルをまとめて保存する
self.addEventListener("install", event => {
  event.waitUntil(caches.open(CACHE_NAME).then(cache => cache.addAll(APP_FILES)));
  self.skipWaiting();
});

// 更新時：古い番号の保存データを削除する
self.addEventListener("activate", event => {
  event.waitUntil(
    caches.keys().then(keys => Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k))))
  );
  self.clients.claim();
});

// 読み込み時：まず保存データを返し、裏でネットから最新版を取ってきて保存し直す
// （Google Fonts のフォントも同じように保存するので、オフラインでもフォントが崩れない）
self.addEventListener("fetch", event => {
  if (event.request.method !== "GET") return;
  event.respondWith(
    caches.open(CACHE_NAME).then(async cache => {
      const cached = await cache.match(event.request, { ignoreSearch: true });
      const fromNetwork = fetch(event.request)
        .then(res => {
          if (res.ok || res.type === "opaque") cache.put(event.request, res.clone());
          return res;
        })
        .catch(() => cached);
      return cached || fromNetwork;
    })
  );
});
