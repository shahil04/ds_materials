const VIDEO_SRC_PATTERNS = /\.(mp4|webm|mkv|ogg|ogv|avi|mov|flv|ts|m3u8)(\?|$)/i;

function getTitleFromUrl(url) {
    try {
        const segments = new URL(url).pathname.split('/').filter(Boolean);
        return decodeURIComponent((segments[segments.length - 1] || 'video').split('?')[0]);
    } catch { return 'video'; }
}

function scanMedia() {
    const pageTitle = document.title || 'media';
    const seen = new Set();
    let mediaItems = [];

    // ── IMAGES ──────────────────────────────────────────────────────────────
    document.querySelectorAll('img').forEach(img => {
        const src = img.src || img.getAttribute('data-src') || img.getAttribute('data-lazy-src');
        if (src && src.startsWith('http') && !seen.has(src)) {
            seen.add(src);
            mediaItems.push({
                type: 'image',
                url: src,
                title: (img.title || img.alt || 'image_' + pageTitle).trim()
            });
        }
    });

    // ── VIDEO TAGS ───────────────────────────────────────────────────────────
    document.querySelectorAll('video').forEach(video => {
        // Collect all possible sources: src attribute + all <source> children
        const srcs = [];
        if (video.src && !video.src.startsWith('blob:')) srcs.push(video.src);
        video.querySelectorAll('source').forEach(s => {
            if (s.src && !s.src.startsWith('blob:')) srcs.push(s.src);
        });
        // Also check data attributes
        ['data-src','data-video-src','data-url'].forEach(attr => {
            const v = video.getAttribute(attr);
            if (v && v.startsWith('http')) srcs.push(v);
        });

        let title = video.title || video.getAttribute('aria-label') || video.getAttribute('data-title');
        if (!title) {
            const heading = video.closest('section, article, div')?.querySelector('h1,h2,h3,h4');
            title = heading ? heading.innerText.trim() : 'video_' + pageTitle;
        }

        srcs.forEach(src => {
            if (src && src.startsWith('http') && !seen.has(src)) {
                seen.add(src);
                mediaItems.push({ type: 'video', url: src, title: title.trim() });
            }
        });
    });

    // ── ANCHOR LINKS POINTING DIRECTLY TO VIDEO FILES ────────────────────────
    document.querySelectorAll('a[href]').forEach(a => {
        const href = a.href;
        if (href && VIDEO_SRC_PATTERNS.test(href) && !seen.has(href)) {
            seen.add(href);
            const title = a.title || a.textContent.trim() || getTitleFromUrl(href);
            mediaItems.push({ type: 'video', url: href, title: title.trim() });
        }
    });

    return mediaItems;
}

// Guard against multiple injections
if (!window.__mediaDownloaderListener) {
    window.__mediaDownloaderListener = true;
    chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
        if (request.action === 'scan_page') {
            sendResponse({ items: scanMedia() });
        }
    });
}
